import dash
import dash_bootstrap_components as dbc
from dash import html

from utils.data_processing import load_financial_data
from layouts.overview_dashboard import create_overview_layout
from callbacks.overview_callbacks import register_overview_callbacks

# Function to get data
def get_data():
    return load_financial_data()

# Initialize Dash app
app = dash.Dash(
    __name__, 
    title="Accounting Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Set layout
app.layout = html.Div([
    create_overview_layout()
], className="app-container")

# Register callbacks
register_overview_callbacks(app, get_data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)