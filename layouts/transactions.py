from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def create_transactions_layout():
    """
    Create transactions page layout
    
    Returns:
    - Dash layout for transactions page
    """
    return html.Div([
        # Header section
        html.Div([
            html.H1("Transactions", className="page-title"),
            html.P("Search, filter and manage financial transactions", className="page-subtitle")
        ], className="page-header"),
        
        # Filters section
        html.Div([
            html.H3("Search & Filters", className="section-title"),
            
            # Search and filter controls
            html.Div([
                # First row of filters
                html.Div([
                    # Date range filter
                    html.Div([
                        html.Label("Date Range:"),
                        dcc.DatePickerRange(
                            id='transactions-date-filter',
                            start_date_placeholder_text="Start Date",
                            end_date_placeholder_text="End Date",
                            className="date-picker"
                        )
                    ], className="filter-item"),
                    
                    # Amount range filter
                    html.Div([
                        html.Label("Amount Range:"),
                        # In layouts/transactions.py
                        # Find the RangeSlider component and ensure min, max, and step are integers:

                        dcc.RangeSlider(
                            id='amount-range-slider',
                            min=0,
                            max=1000,  # This will be updated by the callback
                            step=50,
                            marks={0: '0', 250: '250', 500: '500', 750: '750', 1000: '1000'},
                            value=[0, 1000]
                        )
                    ], className="filter-item"),
                ], className="filter-row"),
                
                # Second row of filters
                html.Div([
                    # Transaction type filter
                    html.Div([
                        html.Label("Transaction Type:"),
                        dcc.Dropdown(
                            id='transactions-type-filter',
                            multi=True,
                            placeholder="Select transaction types",
                            className="filter-dropdown"
                        )
                    ], className="filter-item"),
                    
                    # Category filter
                    html.Div([
                        html.Label("Category:"),
                        dcc.Dropdown(
                            id='transactions-category-filter',
                            multi=True,
                            placeholder="Select categories",
                            className="filter-dropdown"
                        )
                    ], className="filter-item"),
                    
                    # Account filter
                    html.Div([
                        html.Label("Account:"),
                        dcc.Dropdown(
                            id='transactions-account-filter',
                            multi=True,
                            placeholder="Select accounts",
                            className="filter-dropdown"
                        )
                    ], className="filter-item"),
                ], className="filter-row"),
                
                # Search box
                html.Div([
                    html.Label("Search:"),
                    dcc.Input(
                        id="transactions-search",
                        type="text",
                        placeholder="Search by description, reference, vendor...",
                        className="search-input"
                    )
                ], className="search-container"),
                
                # Action buttons
                html.Div([
                    html.Button("Apply Filters", id="apply-filters-btn", className="btn btn-primary"),
                    html.Button("Reset Filters", id="reset-filters-btn", className="btn btn-secondary")
                ], className="filter-actions")
            ], className="filters-container")
        ], className="filters-section"),
        
        # Transactions table section
        html.Div([
            html.Div([
                html.H3("Transaction List", className="section-title"),
                html.Div([
                    html.Button("Export CSV", id="export-csv-btn", className="btn btn-outline-primary"),
                    html.Button("Export PDF", id="export-pdf-btn", className="btn btn-outline-primary"),
                ], className="table-actions")
            ], className="table-header"),
            
            # Transactions table
            dash_table.DataTable(
                id='transactions-table',
                columns=[
                    {"name": "Date", "id": "Date", "type": "datetime"},
                    {"name": "Account", "id": "Account"},
                    {"name": "Description", "id": "Description"},
                    {"name": "Category", "id": "Category"},
                    {"name": "Transaction Type", "id": "Transaction_Type"},
                    {"name": "Customer/Vendor", "id": "Customer_Vendor"},
                    {"name": "Debit", "id": "Debit", "type": "numeric", "format": {"specifier": ",.2f"}},
                    {"name": "Credit", "id": "Credit", "type": "numeric", "format": {"specifier": ",.2f"}},
                    {"name": "Payment Method", "id": "Payment_Method"},
                    {"name": "Reference", "id": "Reference"}
                ],
                page_size=15,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '100px',
                    'maxWidth': '300px',
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_as_list_view=True,
            ),
            
            # Pagination info
            html.Div([
                html.Span("Showing ", className="pagination-text"),
                html.Span(id="pagination-info", className="pagination-info"),
                html.Span(" entries", className="pagination-text"),
            ], className="pagination-container")
        ], className="transactions-table-section")
    ], className="transactions-container") 