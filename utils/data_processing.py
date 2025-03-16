import pandas as pd
import os

def load_financial_data(file_path='data/financial_accounting.csv'):
    """
    Đọc và xử lý dữ liệu tài chính từ file CSV
    
    Parameters:
    - file_path: Đường dẫn đến file CSV
    
    Returns:
    - DataFrame đã xử lý
    """
    # Kiểm tra file tồn tại
    if not os.path.exists(file_path):
        # Nếu không tìm thấy file gốc, thử tìm file 1000.csv
        alternative_path = 'data/1000.csv'
        if os.path.exists(alternative_path):
            file_path = alternative_path
        else:
            raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại {file_path} hoặc {alternative_path}")
    
    # Đọc dữ liệu
    df = pd.read_csv(file_path, skipinitialspace=True)
    
    # Xử lý dữ liệu
    df_processed = df.copy()
    
    # Chuyển đổi các cột số sang kiểu float
    df_processed['Debit'] = pd.to_numeric(df_processed['Debit'], errors='coerce')
    df_processed['Credit'] = pd.to_numeric(df_processed['Credit'], errors='coerce')
    
    # Chuyển đổi cột Date sang datetime
    try:
        df_processed['Date'] = pd.to_datetime(df_processed['Date'])
    except:
        print("Cảnh báo: Không thể chuyển đổi cột Date sang định dạng datetime")
    
    return df_processed