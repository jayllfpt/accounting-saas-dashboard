from dash import html, dcc
import dash_bootstrap_components as dbc

def create_header():
    """
    Create a header component with navigation
    
    Returns:
    - Dash component for header with navigation
    """
    return html.Div([
        # Logo and title
        html.Div([
            html.Img(src="/assets/images/logo.png", className="logo", height="40px"),
            html.H2("Accounting Dashboard", className="header-title")
        ], className="header-brand"),
        
        # Navigation
        html.Div([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Overview", href="/", active="exact", className="nav-link")),
                dbc.NavItem(dbc.NavLink("Transactions", href="/transactions", active="exact", className="nav-link"))
            ], className="header-nav", pills=True)
        ], className="header-menu"),
        
        # User info / settings
        html.Div([
            html.Span("Admin", className="user-name"),
            html.I(className="fas fa-user-circle user-icon")
        ], className="header-user")
    ], className="header-container") 