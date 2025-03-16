import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from dash import html

class TestMain(unittest.TestCase):
    
    @patch('main.load_financial_data')
    def test_get_data(self, mock_load_financial_data):
        # Setup
        mock_df = MagicMock()
        mock_load_financial_data.return_value = mock_df
        
        # Execute
        result = main.get_data()
        
        # Assert
        mock_load_financial_data.assert_called_once()
        self.assertEqual(result, mock_df)
    
    def test_display_page(self):
        # Test with transactions path
        result_transactions = main.display_page('/transactions')
        self.assertIsInstance(result_transactions, html.Div)
        
        # Test with default path
        result_default = main.display_page('/')
        self.assertIsInstance(result_default, html.Div)
        
        # Test with unknown path
        result_unknown = main.display_page('/unknown')
        self.assertIsInstance(result_unknown, html.Div)

if __name__ == '__main__':
    unittest.main() 