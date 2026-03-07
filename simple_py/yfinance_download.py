import yfinance as yf
import pandas as pd
import os  # 导入用于处理路径的库
os.environ['HTTP_PROXY'] = 'socks5://127.0.0.1:10808'
os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:10808'



current_script_path = os.path.dirname(__file__)
directory = os.path.join(current_script_path, "../data")

# 将数据保存为CSV文件的函数
def save_to_csv(data, filename):
    full_path = os.path.join(directory, filename)
    data.to_csv(full_path)
    print("数据已保存到", full_path)

# 通过股票代码获取数据的函数
def normalize_stooq_symbol(stock_symbol):
    symbol = stock_symbol.strip().lower()

    # Stooq 不接受 ^ 前缀（例如 ^SPX）
    if symbol.startswith("^"):
        symbol = symbol[1:]

    # 对于美股/ETF，补充 .us 后缀（例如 tqqq -> tqqq.us）
    if "." not in symbol and symbol.isalnum():
        symbol = f"{symbol}.us"

    return symbol


def download_from_stooq(stock_symbol):
    stooq_symbol = normalize_stooq_symbol(stock_symbol)
    url = f"https://stooq.com/q/d/l/?s={stooq_symbol}&i=d"

    data = pd.read_csv(url)
    if data.empty or "Date" not in data.columns:
        raise ValueError(f"Stooq 返回空数据: {stock_symbol} ({stooq_symbol})")

    data["Date"] = pd.to_datetime(data["Date"])
    data = data.set_index("Date").sort_index()

    # 对齐 yfinance 的列结构
    if "Adj Close" not in data.columns and "Close" in data.columns:
        data["Adj Close"] = data["Close"]

    return data


def download_stock_data(stock_symbol, source="yahoo"):
    try:
        if source == "yahoo":
            data = yf.download(stock_symbol, period='max', auto_adjust=False)
        elif source == "stooq":
            data = download_from_stooq(stock_symbol)
        else:
            raise ValueError(f"不支持的数据源: {source}")

        filename = stock_symbol + ".csv"
        save_to_csv(data, filename)
    except Exception as e:
        print("下载数据失败:", stock_symbol, "source=", source)
        print("错误:", e)

# 主程序，用于下载股票列表中的数据
if __name__ == "__main__":
    # stock_list = ["^NDX", "^SPX"]
    # stock_list = ["^RUT", "^N225", "^HSI"]
    # stock_list = ["SMH", "SOXX", "SSO"]
    # stock_list =  ["sso", "upro", "qqq"]
    # stock_list =  ["NVDA"]
    stock_list = ["tqqq", "qld", "qqq"]
    source = "yahoo"  # 可改为 "stooq"
    for stock_symbol in stock_list:
        download_stock_data(stock_symbol, source=source)
