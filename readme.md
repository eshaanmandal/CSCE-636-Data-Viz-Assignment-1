# Hong Kong Temperature Grid (2008–2017)

Interactive visualization of daily minimum and maximum temperatures in Hong Kong from 2008–2017.

The project reads a CSV file (`temperature_daily.csv`), aggregates it with Pandas, and builds an interactive Plotly grid where:

- X‑axis: year (2008–2017)  
- Y‑axis: month (Jan–Dec)  
- Cell color: monthly **max** or **min** temperature (selectable)  
- Lines inside each cell: daily **max** (green) and **min** (gray) temperatures  

The main entry point is `main.py`.

---

## 1. Prerequisites

- Python 3.9+ installed  
- Git (optional, if you want to clone the repository)

---

## 2. Setup using `venv`

From the project folder (the folder containing `main.py`, `requirements.txt`, and `temperature_daily.csv`):

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# On macOS / Linux
source .venv/bin/activate

# On Windows (PowerShell)
.venv\Scripts\Activate.ps1


pip install -r requirements.txt

python3 main.py

```

This will:

1. Read temperature_daily.csv.

2. Filter the data to 2008–2017.

3. Build the interactive heatmap + per‑cell line plots using Plotly.

4. Write an HTML file hong_kong_temps_grid.html.

5. Open hong_kong_temps_grid.html in your default web browser.

6. If the HTML file does not open automatically, you can open it manually by double‑clicking hong_kong_temps_grid.html or dragging it into a browser window.

