import unittest
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.charts import create_revenue_expense_chart, create_category_pie_chart, create_cash_flow_chart

class TestCharts(unittest.TestCase):
    
    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=10),
            'Debit': [100, 200, 150, 300, 250, 180, 220, 190, 210, 230],
            'Credit': [150, 250, 200, 350, 300, 230, 270, 240, 260, 280],
            'Category': ['Rent', 'Salary', 'Utilities', 'Sales', 'Rent', 
                         'Salary', 'Utilities', 'Sales', 'Rent', 'Salary']
        })
    
    def test_create_revenue_expense_chart(self):
        # Test with default time_period='month'
        fig = create_revenue_expense_chart(self.df)
        
        # Assert that the figure is a plotly Figure object
        self.assertIsInstance(fig, go.Figure)
        
        # Assert that the figure has 2 traces (Expenses and Revenue)
        self.assertEqual(len(fig.data), 2)
        
        # Test with time_period='day'
        fig_day = create_revenue_expense_chart(self.df, time_period='day')
        self.assertIsInstance(fig_day, go.Figure)
        
        # Test with time_period='year'
        fig_year = create_revenue_expense_chart(self.df, time_period='year')
        self.assertIsInstance(fig_year, go.Figure)
    
    def test_create_category_pie_chart(self):
        # Test with default value_column='Debit'
        fig = create_category_pie_chart(self.df)
        
        # Assert that the figure is a plotly Figure object
        self.assertIsInstance(fig, go.Figure)
        
        # Test with value_column='Credit'
        fig_credit = create_category_pie_chart(self.df, value_column='Credit')
        self.assertIsInstance(fig_credit, go.Figure)
    
    def test_create_cash_flow_chart(self):
        fig = create_cash_flow_chart(self.df)
        
        # Assert that the figure is a plotly Figure object
        self.assertIsInstance(fig, go.Figure)
        
        # Assert that the figure has at least one trace
        self.assertGreaterEqual(len(fig.data), 1)

if __name__ == '__main__':
    unittest.main() 