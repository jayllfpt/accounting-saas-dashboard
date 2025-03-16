import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_revenue_expense_chart(df, time_period='month'):
    """
    Create a chart of revenue and expenses over time
    
    Parameters:
    - df: DataFrame containing financial data
    - time_period: Time period for analysis ('day', 'week', 'month', 'quarter', 'year')
    
    Returns:
    - Plotly figure displaying revenue and expenses over time
    """
    # Đảm bảo cột Date là datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Tạo cột thời gian dựa trên khoảng thời gian được chọn
    if time_period == 'day':
        df['TimePeriod'] = df['Date'].dt.date
    elif time_period == 'week':
        df['TimePeriod'] = df['Date'].dt.isocalendar().week
    elif time_period == 'month':
        df['TimePeriod'] = df['Date'].dt.to_period('M').astype(str)
    elif time_period == 'quarter':
        df['TimePeriod'] = df['Date'].dt.to_period('Q').astype(str)
    elif time_period == 'year':
        df['TimePeriod'] = df['Date'].dt.year
    
    # Tính tổng Debit và Credit theo khoảng thời gian
    time_data = df.groupby('TimePeriod').agg({
        'Debit': 'sum',
        'Credit': 'sum'
    }).reset_index()
    
    # Tạo biểu đồ
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=time_data['TimePeriod'],
        y=time_data['Debit'],
        name='Expenses',
        marker_color='#fd7e14'
    ))
    
    fig.add_trace(go.Bar(
        x=time_data['TimePeriod'],
        y=time_data['Credit'],
        name='Revenue',
        marker_color='#28a745'
    ))
    
    fig.update_layout(
        title='Revenue and Expenses by ' + time_period,
        xaxis_title='Time Period',
        yaxis_title='Value',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_category_pie_chart(df, value_column='Debit'):
    """
    Create a pie chart analyzing by category
    
    Parameters:
    - df: DataFrame containing financial data
    - value_column: Value column for analysis ('Debit' or 'Credit')
    
    Returns:
    - Plotly figure displaying distribution by category
    """
    category_data = df.groupby('Category')[value_column].sum().reset_index()
    
    if len(category_data) > 0:
        fig = px.pie(
            category_data, 
            values=value_column, 
            names='Category',
            title=f'Distribution by Category ({value_column})',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
    else:
        fig = px.pie(title='No data to display')
    
    return fig

def create_cash_flow_chart(df):
    """
    Create a cash flow chart over time with daily bar chart
    
    Parameters:
    - df: DataFrame containing financial data
    
    Returns:
    - Plotly figure displaying cash flow over time
    """
    # Đảm bảo cột Date là datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Tạo bản sao để tránh ảnh hưởng đến DataFrame gốc
    df_copy = df.copy()
    
    # Xử lý dữ liệu dòng tiền dựa trên Transaction_Type và Category
    df_copy['CashFlowValue'] = 0
    
    # Xác định các giao dịch thu (inflow)
    inflow_mask = (df_copy['Category'] == 'Revenue') | (df_copy['Transaction_Type'] == 'Sale')
    df_copy.loc[inflow_mask, 'CashFlowValue'] = df_copy.loc[inflow_mask, 'Credit']
    
    # Xác định các giao dịch chi (outflow)
    outflow_mask = (df_copy['Category'] == 'Expense') | (df_copy['Transaction_Type'] == 'Purchase')
    df_copy.loc[outflow_mask, 'CashFlowValue'] = -df_copy.loc[outflow_mask, 'Debit']
    
    # Tính dòng tiền theo ngày
    cash_flow = df_copy.groupby(df_copy['Date'].dt.date)['CashFlowValue'].sum().reset_index()
    cash_flow.columns = ['Date', 'CashFlow']
    
    # Tính dòng tiền tích lũy
    cash_flow['CumulativeCashFlow'] = cash_flow['CashFlow'].cumsum()
    
    # Tạo biểu đồ với subplot để có 2 biểu đồ riêng biệt
    fig = go.Figure()
    
    # Thêm đường cơ sở (zero line) để dễ phân biệt dòng tiền dương và âm
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
    
    # Bar chart for daily cash flow
    fig.add_trace(go.Bar(
        x=cash_flow['Date'],
        y=cash_flow['CashFlow'],
        name='Daily Cash Flow',
        marker_color=cash_flow['CashFlow'].apply(lambda x: '#28a745' if x >= 0 else '#dc3545')
    ))
    
    # Line chart for cumulative cash flow (using second y-axis)
    fig.add_trace(go.Scatter(
        x=cash_flow['Date'],
        y=cash_flow['CumulativeCashFlow'],
        mode='lines+markers',
        name='Cumulative Cash Flow',
        line=dict(color='#007BFF', width=3),
        yaxis='y2'
    ))
    
    # Update layout with second y-axis
    fig.update_layout(
        title='Cash Flow Analysis Over Time',
        xaxis=dict(
            title='Date',
            type='category',
            tickangle=-45,
            tickmode='auto',
            nticks=20
        ),
        yaxis=dict(
            title='Daily Cash Flow',
            side='left',
            showgrid=True
        ),
        yaxis2=dict(
            title='Cumulative Cash Flow',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        barmode='relative',
        height=500,
        margin=dict(l=50, r=50, t=80, b=100)
    )
    
    # Add annotation
    fig.add_annotation(
        text="Green: Positive Cash Flow | Red: Negative Cash Flow",
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        font=dict(size=12)
    )
    
    return fig