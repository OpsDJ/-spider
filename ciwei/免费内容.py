# 创建文件
import os
# 执行JavaScript
import subprocess
import requests
import time
import re
# 可用于post请求
import json
# 可用靓汤也可用lxml
from bs4 import BeautifulSoup
from lxml import etree

# 时间戳
t = time.time()
# 可以选择指定的小说
# bid = int(input('请输入书本的ID：'))

# 打开之前获取的id文件
with open('id.txt', mode='r', encoding='utf-8') as f:
    bids = f.readlines()
# print(bids)

# 设置最大重试请求
max_retries = 3
# 设置重试间隔
delay = 1
# 循环每一个小说id
for bid in bids:
    # 初始化和格式规约
    retries = 0
    bid = int(bid)
    # 打印出提示
    print('下一本id--------------->', bid)
    # 请求头
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Length": "0",
        "Origin": "https://www.ciweimao.com",
        "Referer": f"https://www.ciweimao.com/chapter/{bid}",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "X-Requested-With": "XMLHttpRequest"}
    # 持久化请求
    ssess = requests.session()
    # 为了post请求
    data = {
        'book_id': f"{bid}",
        "chapter_id": "0",
        "orderby": '0'
    }
    # 书本章节
    details_url = 'https://www.ciweimao.com/chapter/get_chapter_list_in_chapter_detail'
    # 书名
    ur = f"https://www.ciweimao.com/book/{bid}"
    # 设置重试逻辑
    while retries < max_retries:
        try:
            resp = ssess.get(ur, headers=headers)

            tree = etree.HTML(resp.text)

            # print(resp)
            # 获取书名，本文使用xpath解析
            name = tree.xpath('//h1/text()')[0].replace('/', '_')

            print('正在下载', name)

            # 获取章节
            res = ssess.post(details_url, headers=headers, data=data)

            tree = etree.HTML(res.text)

            url_list = tree.xpath('//ul[@class="book-chapter-list"]/li/a')
            # 计数
            counts = 0
            for urls in url_list:
                # 获取章节名称
                title = urls.xpath('./text()')[0].replace('/', '_')
                # 提取章节id
                id = urls.xpath('./@href')[0]

                print("下载章节---------->", title)

                id = id.split("/")[-1]

                # url_main = f'https://www.ciweimao.com/chapter/{id}'
                # #
                # res = ssess.get(url_main, headers=headers)
                #

                url = 'https://www.ciweimao.com/chapter/ajax_get_session_code'

                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "Content-Length": "0",
                    "Origin": "https://www.ciweimao.com",
                    "Referer": f"https://www.ciweimao.com/chapter/{id}",
                    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                    "X-Requested-With": "XMLHttpRequest"}

                data = {
                    "chapter_id": f"{id}"
                }
                # 提取提取chapter_access_key
                res1 = ssess.post(url, headers=headers, data=data)

                chapter_access_key = res1.json()["chapter_access_key"]

                # print(chapter_access_key)

                url = 'https://www.ciweimao.com/chapter/get_book_chapter_detail_info'

                data = {
                    "chapter_id": f"{id}",
                    "chapter_access_key": chapter_access_key
                }

                # 提取chapter_content encryt_keys
                res2 = ssess.post(url=url, headers=headers, data=data)

                chapter_content = res2.json()['chapter_content']

                encryt_keys = res2.json()['encryt_keys']
                # print(res2.json())
                # 保存chapter_content
                # 保存到本地
                with open('chapter_content.txt', 'w', encoding='utf8') as f:
                    f.write(chapter_content)

                # 保存ncryt_keys
                with open('encryt_keys.txt', 'w', encoding='utf8') as f:
                    json.dump(encryt_keys, f)

                # 保存chapter_access_key
                with open('chapter_access_key.txt', 'w', encoding='utf8') as f:
                    f.write(chapter_access_key)

                # 补充JavaScript环境
                os.environ["NODE_PATH"] = r"D:\New Folder\node_modules"
                # 运行JavaScript代码
                result = subprocess.run(['node', 'ciweimao.js'], capture_output=True)
                contents = result.stdout.decode('utf-8').strip()
                # print(contents)

                # 解析出文字
                soup = BeautifulSoup(contents, 'html.parser')
                chapter_tags = soup.find_all('p', class_='chapter')

                # 去除无关信息
                text_content = [tag.get_text().strip().replace("24KdT4", "") for tag in chapter_tags]

                result = '\n'.join(text_content)
                counts += 1
                # 指定具体路径
                directory = f'内容/{name}'

                # 如果文件不存在，创建路径
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # 去除无效字符
                title = re.sub(r'[<>:"/\\|?*]', "", title)
                # 指定具体路径
                file_path = f'{directory}/{counts}_{title}.txt'
                # 写入文件
                with open(file_path, mode='w', encoding='utf-8') as f:
                    f.write(result)
            break
        except Exception as e:
            print("请求失败，正在重试...", e)
            retries += 1
            time.sleep(delay)
    if retries == max_retries:
        print(f'到达最大重试次数ID为{bid}，跳过该请求...')
        with open('error_id.txt', mode='a', newline='', encoding='utf-8') as f:
            f.write(str(bid))
            f.write('\n')
        print('下载失败的id已存入文件')

    else:
        print(f'小说——{bid}, 下载成功！')

    continue
