import requests
import re
# 本代码使用并发，有点小暴力
from concurrent.futures import ThreadPoolExecutor


def get_id(url):
    # 持久化请求
    ssess = requests.session()
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Length": "0",
        "Origin": "https://www.ciweimao.com",
        "Referer": "https://www.ciweimao.com/chapter/110694165",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "X-Requested-With": "XMLHttpRequest"}
    # 发生请求
    res1 = ssess.get(url, headers=headers)
    # 使用正则提取
    pattern = r'<td><p class="name"><a href="(.*?)"'
    href_values = re.findall(pattern, res1.text)
    # 保存文件
    with open('id.txt', mode='a', newline='', encoding='utf-8') as f:
        for href_value in href_values:
            id = href_value.split("/")[-1]
            f.write(id)
            f.write('\n')
    print('保存成功')


if __name__ == '__main__':
    # 设置30线程
    with ThreadPoolExecutor(max_workers=30) as exe:
        for i in range(1, 136):
            url = f'https://www.ciweimao.com/book_list/0-0-0-0-0-2/quanbu/{i}'
            exe.submit(get_id, url)
