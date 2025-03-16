from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime
import pytz

from components.summary_stats import create_summary_stats
from components.charts import (
    create_revenue_expense_chart,
    create_category_pie_chart,
    create_cash_flow_chart
)

def register_overview_callbacks(app, df_function):
    """
    Register callbacks for overview dashboard
    
    Parameters:
    - app: Dash app instance
    - df_function: Function returning financial data DataFrame
    """
    
    @app.callback(
        [Output('summary-stats-container', 'children'),
         Output('revenue-expense-chart', 'figure'),
         Output('category-pie-chart', 'figure'),
         Output('cash-flow-chart', 'figure'),
         Output('last-update-time', 'children')],
        [Input('date-range-filter', 'start_date'),
         Input('date-range-filter', 'end_date'),
         Input('transaction-type-filter', 'value'),
         Input('category-filter', 'value'),
         Input('time-period-selector', 'value'),
         Input('category-value-selector', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_overview_dashboard(start_date, end_date, transaction_types, 
                                 categories, time_period, category_value, n_intervals):
        """
        Update overview dashboard based on filters
        """
        # Lấy dữ liệu
        df = df_function()
        
        # Lọc dữ liệu
        filtered_df = filter_data(df, start_date, end_date, transaction_types, categories)
        
        # Tính toán thống kê tổng quan
        total_debit = filtered_df['Debit'].sum()
        total_credit = filtered_df['Credit'].sum()
        transaction_count = len(filtered_df)
        net_cash_flow = total_credit - total_debit
        
        # Tạo các thành phần
        summary_stats = create_summary_stats(
            total_debit, total_credit, transaction_count, net_cash_flow
        )
        
        revenue_expense_fig = create_revenue_expense_chart(filtered_df, time_period)
        category_pie_fig = create_category_pie_chart(filtered_df, category_value)
        cash_flow_fig = create_cash_flow_chart(filtered_df)
        
        # Update time
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.now(vietnam_tz).strftime("%d/%m/%Y %H:%M:%S")
        update_time = f"Last updated: {current_time}"
        
        return summary_stats, revenue_expense_fig, category_pie_fig, cash_flow_fig, update_time
    
    @app.callback(
        [Output('transaction-type-filter', 'options'),
         Output('category-filter', 'options')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_filter_options(n_intervals):
        """
        Cập nhật các tùy chọn bộ lọc
        """
        df = df_function()
        
        transaction_type_options = [
            {'label': t, 'value': t} for t in sorted(df['Transaction_Type'].unique())
        ]
        
        category_options = [
            {'label': c, 'value': c} for c in sorted(df['Category'].unique())
        ]
        
        return transaction_type_options, category_options

def filter_data(df, start_date, end_date, transaction_types, categories):
    """
    Lọc dữ liệu dựa trên các bộ lọc
    
    Parameters:
    - df: DataFrame gốc
    - start_date: Ngày bắt đầu
    - end_date: Ngày kết thúc
    - transaction_types: Danh sách loại giao dịch
    - categories: Danh sách danh mục
    
    Returns:
    - DataFrame đã lọc
    """
    filtered_df = df.copy()
    
    # Lọc theo ngày
    if start_date and end_date:
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & 
                                 (filtered_df['Date'] <= end_date)]
    
    # Lọc theo loại giao dịch
    if transaction_types and len(transaction_types) > 0:
        filtered_df = filtered_df[filtered_df['Transaction_Type'].isin(transaction_types)]
    
    # Lọc theo danh mục
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
    
    return filtered_df