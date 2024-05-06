import yfinance as yf
import os  # 导入用于处理路径的库

current_script_path = os.path.dirname(__file__)
directory = os.path.join(current_script_path, "../data")

# 将数据保存为CSV文件的函数
def save_to_csv(data, filename):
    full_path = os.path.join(directory, filename)
    data.to_csv(full_path)
    print("数据已保存到", full_path)

# 通过股票代码获取数据的函数
def download_stock_data(stock_symbol):
    try:
        data = yf.download(stock_symbol)
        filename = stock_symbol + ".csv"
        save_to_csv(data, filename)
    except Exception as e:
        print("下载数据失败:", stock_symbol)
        print("错误:", e)

# 主程序，用于下载股票列表中的数据
if __name__ == "__main__":
    # stock_list = ["^NDX", "^SPX"]
    stock_list = ["^RUT", "^N225", "^HSI"]
    for stock_symbol in stock_list:
        download_stock_data(stock_symbol)
