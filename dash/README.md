# SpaceX Dash Application

This folder contains the interactive Plotly Dash application for analyzing SpaceX launch data.

## Running the Application

1. Open your terminal or command prompt.
2. Navigate to this directory (`dash`).
3. Ensure you have the required packages installed (you may need `dash`, `pandas`, `plotly`):
   ```bash
   pip install dash pandas plotly
   ```
4. Run the application script:
   ```bash
   python spacex_dash_app.py
   ```
5. Open your web browser and navigate to the address shown in the terminal (usually `http://127.0.0.1:8050/`).

## Files
- `spacex_dash_app.py`: The main Dash application script containing the layout and callback logic.
- `spacex_launch_dash.csv`: The clean dataset used exclusively by this dashboard to render the charts and tables.
