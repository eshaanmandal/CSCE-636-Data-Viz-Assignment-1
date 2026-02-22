import pandas as pd
import plotly.graph_objects as go


def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"], errors="raise")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    return df


def filter_years(df: pd.DataFrame, start_year: int = 2008, end_year: int = 2017) -> pd.DataFrame:
    mask = (df["year"] >= start_year) & (df["year"] <= end_year)
    return df.loc[mask].copy()


def compute_monthly_stats(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["year", "month"])
        .agg(
            monthly_max=("max_temperature", "max"),
            monthly_min=("min_temperature", "min"),
        )
        .reset_index()
    )
    return grouped


def build_heatmap_traces(monthly_stats: pd.DataFrame):
    years = sorted(monthly_stats["year"].unique())
    months = list(range(1, 13))

    z_max, z_min = [], []
    for m in months:
        row_max, row_min = [], []
        for y in years:
            sub = monthly_stats[(monthly_stats["year"] == y) &
                                (monthly_stats["month"] == m)]
            if not sub.empty:
                row_max.append(sub["monthly_max"].iloc[0])
                row_min.append(sub["monthly_min"].iloc[0])
            else:
                row_max.append(None)
                row_min.append(None)
        z_max.append(row_max)
        z_min.append(row_min)

    zmin = float(monthly_stats["monthly_min"].min())
    zmax = float(monthly_stats["monthly_max"].max())

    heatmap_max = go.Heatmap(
        x=years,
        y=months,
        z=z_max,
        colorscale="Turbo",
        colorbar=dict(title="°C"),
        zmin=zmin,
        zmax=zmax,
        opacity=0.8,
        visible=True,
        name="Monthly max",
        xgap=2,
        ygap=2,
    )

    heatmap_min = go.Heatmap(
        x=years,
        y=months,
        z=z_min,
        colorscale="Turbo",
        colorbar=dict(title="°C"),
        zmin=zmin,
        zmax=zmax,
        opacity=0.8,
        visible=False,
        name="Monthly min",
        xgap=2,
        ygap=2,
    )

    return heatmap_max, heatmap_min, years, months


def build_daily_lines(df: pd.DataFrame):
    traces = []

    for (year, month), sub in df.groupby(["year", "month"]):
        sub_sorted = sub.sort_values("date")
        if sub_sorted.empty:
            continue

        days = sub_sorted["day"]
        x_norm = (days - days.min()) / (days.max() - days.min() + 1e-6)
        x_vals = year + (x_norm - 0.5) * 0.9

        temp_max = sub_sorted["max_temperature"]
        t_norm_max = (temp_max - temp_max.min()) / (temp_max.max() - temp_max.min() + 1e-6)
        y_max = month + 0.05 + t_norm_max * 0.30

        custom_max = sub_sorted[["date", "max_temperature"]]
        traces.append(
            go.Scatter(
                x=x_vals,
                y=y_max,
                mode="lines",
                line=dict(color="rgba(0, 150, 0, 0.95)", width=2),
                customdata=custom_max,
                hovertemplate=(
                    "Date %{customdata[0]|%Y-%m-%d}"
                    "<br>Max %{customdata[1]} °C"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

        temp_min = sub_sorted["min_temperature"]
        t_norm_min = (temp_min - temp_min.min()) / (temp_min.max() - temp_min.min() + 1e-6)
        y_min = month - 0.35 + t_norm_min * 0.30

        custom_min = sub_sorted[["date", "min_temperature"]]
        traces.append(
            go.Scatter(
                x=x_vals,
                y=y_min,
                mode="lines",
                line=dict(color="rgba(200, 200, 200, 0.95)", width=2),
                customdata=custom_min,
                hovertemplate=(
                    "Date %{customdata[0]|%Y-%m-%d}"
                    "<br>Min %{customdata[1]} °C"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    return traces


def build_figure(df_all: pd.DataFrame) -> go.Figure:
    df = filter_years(df_all)
    monthly_stats = compute_monthly_stats(df)

    heatmap_max, heatmap_min, years, months = build_heatmap_traces(monthly_stats)
    daily_traces = build_daily_lines(df)

    fig = go.Figure()
    fig.add_trace(heatmap_max)
    fig.add_trace(heatmap_min)
    for tr in daily_traces:
        fig.add_trace(tr)

    n_daily = len(daily_traces)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig.update_layout(
        title="Hong Kong Temperatures 2008–2017",
        xaxis_title="Year",
        yaxis_title="Month",
        xaxis=dict(
            tickmode="array",
            tickvals=years,
            ticktext=[str(y) for y in years],
        ),
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=month_names,
            range=[0.5, 12.5],
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1.0,
                y=1.25,
                xanchor="right",
                yanchor="top",
                showactive=True,
                buttons=[
                    dict(
                        label="Monthly max",
                        method="update",
                        args=[{"visible": [True, False] + [True] * n_daily}],
                    ),
                    dict(
                        label="Monthly min",
                        method="update",
                        args=[{"visible": [False, True] + [True] * n_daily}],
                    ),
                ],
            )
        ],
        margin=dict(l=80, r=140, t=100, b=80),
        height=600,
        width=1000,
    )

    return fig


if __name__ == "__main__":
    df = load_data("temperature_daily.csv")
    fig = build_figure(df)
    fig.write_html("hong_kong_temps_grid.html", auto_open=True)
