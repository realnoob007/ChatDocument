import datetime
import sqlite3
import requests
import time

# 创建本地数据库
conn = sqlite3.connect('library.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS libraries
             (id text, last_modified text, document_url text)''')

api_key = "sk-TrVWBuAgrgt7k3mIm8mZ6kroxXeW8xjQgUa9IfBqaKklIabc"  # 请替换为你的API密钥

while True:
    # 每10分钟检查并移除所有last modified时间距离目前北京时间过去>30分钟的知识库中的所有文档
    for row in c.execute('SELECT * FROM libraries ORDER BY last_modified'):
        last_modified = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
        if (datetime.datetime.now() - last_modified).total_seconds() > 30 * 60:
            res = requests.get('https://aiproxy.io/api/library/listDocument', headers={"Api-Key": api_key},
                               params={'order': 'desc', 'orderBy': 'gmtCreate', 'page': 1, 'pageSize': 10,
                                       'libraryId': row[0]})
            documents = res.json().get('data', {}).get('records', [])
            for doc in documents:
                requests.post('https://aiproxy.io/api/library/document/delete', headers={"Api-Key": api_key},
                              json={'libraryId': row[0], 'docIds': [doc['docId']]})
            print(
                f"Library {row[0]} hasn't been used for more than 30 minutes. All documents have been deleted.")
            c.execute("UPDATE libraries SET document_url = '' WHERE id = ?", (row[0],))
            conn.commit()
    time.sleep(600)  # 等待10分钟
