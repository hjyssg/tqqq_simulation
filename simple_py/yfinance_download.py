import yfinance as yf

# 将数据保存为CSV文件
def save_to_csv(data, filename):
    data.to_csv(filename)


# 通过股票代码获取数据
def download_stock_data(stock_symbol):
    try:
        data = yf.download(stock_symbol)
        filename = stock_symbol + ".csv"
        save_to_csv(data, filename)
        print("数据已保存到", filename)
    except Exception:
        print(Exception)



# 主程序
if __name__ == "__main__":
    # 输入你感兴趣的股票代码
    
    # 下载股票数据
    # data = download_stock_data("^SPX")

    # data = download_stock_data("^NDX")


    ll = ["^RUT", "NVDA", "soxl", "sqqq", "tqqq", "qyld"]
    for e in ll:
        download_stock_data(e)
    

    
