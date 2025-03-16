import unittest
import pandas as pd
import os
import sys
from unittest.mock import patch, mock_open
import io

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processing import load_financial_data

class TestDataProcessing(unittest.TestCase):
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_load_financial_data_default_path(self, mock_read_csv, mock_exists):
        # Setup
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02'],
            'Debit': ['100', '200'],
            'Credit': ['300', '400']
        })
        mock_read_csv.return_value = mock_df
        
        # Execute
        result = load_financial_data()
        
        # Assert
        mock_exists.assert_called_with('data/financial_accounting.csv')
        mock_read_csv.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result['Debit'].dtype, 'float64')
        self.assertEqual(result['Credit'].dtype, 'float64')
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_load_financial_data_alternative_path(self, mock_read_csv, mock_exists):
        # Setup
        mock_exists.side_effect = lambda path: path == 'data/1000.csv'
        mock_df = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02'],
            'Debit': ['100', '200'],
            'Credit': ['300', '400']
        })
        mock_read_csv.return_value = mock_df
        
        # Execute
        result = load_financial_data()
        
        # Assert
        mock_read_csv.assert_called_once()
        self.assertEqual(len(result), 2)
    
    @patch('os.path.exists')
    def test_load_financial_data_file_not_found(self, mock_exists):
        # Setup
        mock_exists.return_value = False
        
        # Execute & Assert
        with self.assertRaises(FileNotFoundError):
            load_financial_data()
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_load_financial_data_date_conversion_error(self, mock_read_csv, mock_exists):
        # Setup
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'Date': ['invalid-date', 'another-invalid'],
            'Debit': ['100', '200'],
            'Credit': ['300', '400']
        })
        mock_read_csv.return_value = mock_df
        
        # Execute
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            result = load_financial_data()
            
        # Assert
        self.assertTrue("Cảnh báo: Không thể chuyển đổi cột Date" in fake_stdout.getvalue())
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main() 