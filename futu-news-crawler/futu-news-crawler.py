import os 
import requests
import sqlite3
import json

print(os.path)

# 连接到 SQLite 数据库
conn = sqlite3.connect('futu-news.db')
cursor = conn.cursor()

# 创建表格（如果不存在）
cursor.execute('''CREATE TABLE IF NOT EXISTS news_data_table
            (news_id INTEGER PRIMARY KEY, ts timestamp, content TEXT)''')


def checkIfExist(news_id):
    cursor.execute(f"""SELECT * FROM news_data_table where news_id = {news_id}""")
    rr = cursor.fetchone()
    return rr is not None


def do_one_search(news_id):
    if checkIfExist(news_id):
        return

    # 发送 HTTP 请求
    url = f"""http://news.futunn.com/client/market-list?news_id={news_id}&lang=zh-cn"""
    response = requests.get(url)
    # print(f"""begin {news_id}""")

    res_data = json.loads(response.text)
    for temp_data in res_data["data"]["list"]:
        temp_news_id = temp_data["news_id"]
        if not checkIfExist(temp_news_id):
            content = json.dumps(temp_data, indent=4, ensure_ascii=False)
            print(content, "\n\n\n")
            # 将响应的内容存储到数据库
            cursor.execute('INSERT INTO news_data_table (news_id, ts, content) VALUES (?, ?, ?)', 
            (temp_news_id, temp_data["time_str"], content  ))
            conn.commit()

    # print(f"""done {news_id}""")




for ii in range(220000, 260000, 50):
    do_one_search(ii)


