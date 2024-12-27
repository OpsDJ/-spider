# import requests
#
# ci = input('输入1')
# t = int(input('输入2'))
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#     'Referer': 'https://www.ciweimao.com/chapter/110694165',
#     'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
#     'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
#     'Sec-Ch-Ua-Mobile': '?0',
#     'Sec-Ch-Ua-Platform': '"Windows"',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cookie': f'Hm_lvt_1dbadbc80ffab52435c688db7b756e3a=1692441272,1692441340,1692444576,1692459049; get_task_type_sign=1; ci_session={ci} Hm_lpvt_1dbadbc80ffab52435c688db7b756e3a={t}; readPage_visits=17; user_id=18263008; reader_id=18263008; login_token=1a4896b15efc606f1450ecff2ee86475'
# }
#
# url_4 = 'https://www.ciweimao.com/chapter/book_chapter_image'
#
# wkey  = input('input')
#
# params = {
#     "chapter_id": '110694165',
#     'area_width': '870.99',
#     'font': 'undefined',
#     'font_size': '14',
#     'image_code': f'{wkey}',
#     'bg_color_name': 'default',
#     'text_color_name': 'default'
# }
# res2 = requests.get(url_4, headers=headers, params=params)
#
#
# with open('book.png', mode='wb') as f:
#     f.write(res2.content.txt)
#
# print('ok')
import time
t = time.time()
print(int(t))

