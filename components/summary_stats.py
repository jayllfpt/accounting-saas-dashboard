from dash import html

def create_summary_card(title, value, color="#007BFF"):
    """
    Create a card displaying summary information
    
    Parameters:
    - title: Card title
    - value: Value to display
    - color: Card color
    
    Returns:
    - Dash component displaying summary information
    """
    return html.Div([
        html.H4(title, className="summary-card-title"),
        html.H2(value, className="summary-card-value", style={"color": color})
    ], className="summary-card")

def create_summary_stats(total_debit, total_credit, transaction_count, net_cash_flow):
    """
    Create a dashboard with key financial metrics
    
    Parameters:
    - total_debit: Total debit
    - total_credit: Total credit
    - transaction_count: Number of transactions
    - net_cash_flow: Net cash flow
    
    Returns:
    - Dash component displaying summary information
    """
    # Determine color for net cash flow (green if positive, red if negative)
    cash_flow_color = "#28a745" if net_cash_flow >= 0 else "#dc3545"
    
    return html.Div([
        create_summary_card("Total Debit", f"{total_debit:,.2f}", "#007BFF"),
        create_summary_card("Total Credit", f"{total_credit:,.2f}", "#fd7e14"),
        create_summary_card("Transaction Count", f"{transaction_count}", "#6c757d"),
        create_summary_card("Net Cash Flow", f"{net_cash_flow:,.2f}", cash_flow_color)
    ], className="summary-stats-container")