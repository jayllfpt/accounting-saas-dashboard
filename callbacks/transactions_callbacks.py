from dash.dependencies import Input, Output, State
import pandas as pd
import dash

def register_transactions_callbacks(app, df_function):
    """
    Register callbacks for transactions page
    
    Parameters:
    - app: Dash app instance
    - df_function: Function returning financial data DataFrame
    """
    
    @app.callback(
        [Output('transactions-table', 'data'),
         Output('pagination-info', 'children'),
         Output('transactions-type-filter', 'options'),
         Output('transactions-category-filter', 'options'),
         Output('transactions-account-filter', 'options'),
         Output('amount-range-slider', 'max'),
         Output('amount-range-slider', 'marks')],
        [Input('apply-filters-btn', 'n_clicks'),
         Input('reset-filters-btn', 'n_clicks')],
        [State('transactions-date-filter', 'start_date'),
         State('transactions-date-filter', 'end_date'),
         State('amount-range-slider', 'value'),
         State('transactions-type-filter', 'value'),
         State('transactions-category-filter', 'value'),
         State('transactions-account-filter', 'value'),
         State('transactions-search', 'value')]
    )
    def update_transactions_table(apply_clicks, reset_clicks, 
                                 start_date, end_date, amount_range,
                                 transaction_types, categories, accounts, search_term):
        """
        Update transactions table based on filters
        """
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
        
        # Get data
        df = df_function()
        
        # If reset button clicked, clear all filters
        if button_id == 'reset-filters-btn':
            filtered_df = df.copy()
        else:
            # Apply filters
            filtered_df = filter_transactions(df, start_date, end_date, amount_range,
                                            transaction_types, categories, accounts, search_term)
        
        # Get dropdown options
        transaction_type_options = [
            {'label': t, 'value': t} for t in sorted(df['Transaction_Type'].unique())
        ]
        
        category_options = [
            {'label': c, 'value': c} for c in sorted(df['Category'].unique())
        ]
        
        account_options = [
            {'label': a, 'value': a} for a in sorted(df['Account'].unique())
        ]
        
        # Calculate max amount for slider
        max_amount = max(df['Debit'].max(), df['Credit'].max())
        max_amount = int(round(max_amount + 100, -2))  # Round up to nearest 100 and convert to int

        # Create marks for slider with proper integer conversion
        step = max(1, int(max_amount // 5))  # Ensure step is at least 1 and an integer
        marks = {int(i): f'{i:,}' for i in range(0, max_amount + 1, step)}
        
        # Pagination info
        pagination_info = f"1-{min(15, len(filtered_df))} of {len(filtered_df)}"
        
        return (filtered_df.to_dict('records'), pagination_info, 
                transaction_type_options, category_options, account_options,
                max_amount, marks)
    
    @app.callback(
        Output('transactions-search', 'value'),
        [Input('reset-filters-btn', 'n_clicks')]
    )
    def reset_search(n_clicks):
        """Reset search box when reset button is clicked"""
        if n_clicks:
            return ""
        return dash.no_update

def filter_transactions(df, start_date, end_date, amount_range,
                      transaction_types, categories, accounts, search_term):
    """
    Filter transactions based on criteria
    
    Parameters:
    - df: DataFrame with transaction data
    - start_date: Start date for filtering
    - end_date: End date for filtering
    - amount_range: Min and max amount for filtering
    - transaction_types: List of transaction types to include
    - categories: List of categories to include
    - accounts: List of accounts to include
    - search_term: Text to search in description, reference, etc.
    
    Returns:
    - Filtered DataFrame
    """
    filtered_df = df.copy()
    
    # Filter by date
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & 
                                 (filtered_df['Date'] <= end_date)]
    
    # Filter by amount
    if amount_range:
        min_amount, max_amount = amount_range
        # Filter transactions where either Debit or Credit is in range
        debit_in_range = (filtered_df['Debit'] >= min_amount) & (filtered_df['Debit'] <= max_amount)
        credit_in_range = (filtered_df['Credit'] >= min_amount) & (filtered_df['Credit'] <= max_amount)
        filtered_df = filtered_df[debit_in_range | credit_in_range]
    
    # Filter by transaction type
    if transaction_types and len(transaction_types) > 0:
        filtered_df = filtered_df[filtered_df['Transaction_Type'].isin(transaction_types)]
    
    # Filter by category
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
    
    # Filter by account
    if accounts and len(accounts) > 0:
        filtered_df = filtered_df[filtered_df['Account'].isin(accounts)]
    
    # Filter by search term
    if search_term:
        search_term = search_term.lower()
        # Search in multiple columns
        text_columns = ['Description', 'Customer_Vendor', 'Reference', 'Payment_Method']
        
        # Create a mask for each text column
        masks = []
        for column in text_columns:
            if column in filtered_df.columns:
                # Convert column to string and search
                masks.append(filtered_df[column].astype(str).str.lower().str.contains(search_term))
        
        # Combine masks with OR
        if masks:
            combined_mask = masks[0]
            for mask in masks[1:]:
                combined_mask = combined_mask | mask
            
            filtered_df = filtered_df[combined_mask]
    
    return filtered_df 