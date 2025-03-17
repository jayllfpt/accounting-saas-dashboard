import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

from utils.data_processing import load_financial_data
from components.header import create_header
from layouts.overview_dashboard import create_overview_layout
from layouts.transactions import create_transactions_layout
from callbacks.overview_callbacks import register_overview_callbacks
from callbacks.transactions_callbacks import register_transactions_callbacks

# Function to get data
def get_data():
    return load_financial_data()

# Initialize Dash app
app = dash.Dash(
    __name__, 
    title="Accounting Dashboard",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ],
    suppress_callback_exceptions=True  # Important for multi-page apps
)
server = app.server 

# Define app layout with URL routing
app.layout = html.Div([
    # URL Location component for page routing
    dcc.Location(id='url', refresh=False),
    
    # Header component
    create_header(),
    
    # Content container - will be filled based on URL
    html.Div(id='page-content', className="content-container")
], className="app-container")

# Callback to handle page routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/transactions':
        return create_transactions_layout()
    else:
        # Default to overview dashboard
        return create_overview_layout()

# Register callbacks
register_overview_callbacks(app, get_data)
register_transactions_callbacks(app, get_data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)