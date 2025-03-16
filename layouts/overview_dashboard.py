from dash import html, dcc
import dash_bootstrap_components as dbc

from components.summary_stats import create_summary_stats
from components.charts import (
    create_revenue_expense_chart,
    create_category_pie_chart,
    create_cash_flow_chart
)

def create_overview_layout():
    """
    Create financial overview layout for dashboard
    
    Returns:
    - Dash layout displaying financial overview
    """
    return html.Div([
        # Header
        html.Div([
            html.H1("Financial Overview", className="dashboard-title"),
            html.P("Real-time financial data display", className="dashboard-subtitle")
        ], className="dashboard-header"),
        
        # Filters
        html.Div([
            html.H3("Filters", className="filter-title"),
            html.Div([
                html.Div([
                    html.Label("Date Range:"),
                    dcc.DatePickerRange(
                        id='date-range-filter',
                        start_date_placeholder_text="Start Date",
                        end_date_placeholder_text="End Date",
                        className="date-picker"
                    )
                ], className="filter-item"),
                
                html.Div([
                    html.Label("Transaction Type:"),
                    dcc.Dropdown(
                        id='transaction-type-filter',
                        multi=True,
                        placeholder="Select transaction types",
                        className="filter-dropdown"
                    )
                ], className="filter-item"),
                
                html.Div([
                    html.Label("Category:"),
                    dcc.Dropdown(
                        id='category-filter',
                        multi=True,
                        placeholder="Select categories",
                        className="filter-dropdown"
                    )
                ], className="filter-item")
            ], className="filter-container")
        ], className="filter-section"),
        
        # Summary Statistics
        html.Div([
            html.H3("Summary Statistics", className="section-title"),
            html.Div(id="summary-stats-container", className="summary-stats-section")
        ], className="dashboard-section"),
        
        # Analysis Charts
        html.Div([
            html.Div([
                html.H3("Revenue & Expenses", className="chart-title"),
                html.Div([
                    html.Label("View by:"),
                    dcc.RadioItems(
                        id='time-period-selector',
                        options=[
                            {'label': 'Day', 'value': 'day'},
                            {'label': 'Week', 'value': 'week'},
                            {'label': 'Month', 'value': 'month'},
                            {'label': 'Quarter', 'value': 'quarter'},
                            {'label': 'Year', 'value': 'year'}
                        ],
                        value='month',
                        inline=True,
                        className="radio-items"
                    )
                ], className="chart-controls"),
                dcc.Graph(id='revenue-expense-chart', className="chart")
            ], className="chart-container"),
            
            html.Div([
                html.H3("Category Analysis", className="chart-title"),
                html.Div([
                    html.Label("Display:"),
                    dcc.RadioItems(
                        id='category-value-selector',
                        options=[
                            {'label': 'Expenses', 'value': 'Debit'},
                            {'label': 'Revenue', 'value': 'Credit'}
                        ],
                        value='Debit',
                        inline=True,
                        className="radio-items"
                    )
                ], className="chart-controls"),
                dcc.Graph(id='category-pie-chart', className="chart")
            ], className="chart-container")
        ], className="charts-row"),
        
        # Cash Flow Chart
        html.Div([
            html.H3("Cash Flow Analysis", className="section-title"),
            dcc.Graph(id='cash-flow-chart', className="full-width-chart")
        ], className="dashboard-section"),
        
        # Update Time
        html.Div([
            html.P(id="last-update-time", className="update-time"),
            dcc.Interval(
                id='interval-component',
                interval=60*1000,  # update every minute (60,000 ms)
                n_intervals=0
            )
        ], className="update-info")
    ], className="overview-dashboard")