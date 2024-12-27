import scrapy
from liepin.items import LiepinItem
import json
import execjs



js_file = open('../lp.js', mode='r', encoding='utf-8').read()


# 循环1个城市，一个城市数据大约为400条
city_list = ['010', '020', '030', '040', '050020', '050090',
             '060080', '060020', '070020', '210040'
             '280020', '170020', '270020']
key_word = ['数据']

class LpSpider(scrapy.Spider):
    name = "lp"
    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': []
    }
    def start_requests(self):

        for city in city_list:
            for key in key_word:
                for page in range(0, 10):
                    # 下一页
                    js_code = execjs.compile(js_file)
                    ckId = js_code.call('r', 32)

                    # 构造请求数据
                    data = {
                        "data": {
                            "mainSearchPcConditionForm": {
                                "city": f"{city}",
                                "dq": f"{city}",
                                "pubTime": "",
                                "currentPage": page,
                                "pageSize": 40,
                                "key": f"{key}",
                                "suggestTag": "",
                                "workYearCode": "0",
                                "compId": "",
                                "compName": "",
                                "compTag": "",
                                "industry": "",
                                "salary": "",
                                "jobKind": "",
                                "compScale": "",
                                "compKind": "",
                                "compStage": "",
                                "eduLevel": ""
                            },
                            "passThroughForm": {
                                "sfrom": "search_job_pc",
                                "ckId": f"{ckId}",
                                "skId": "sp4jb97xndy4mffxe6hsrqixqwd9frma",
                                "fkId": "sp4jb97xndy4mffxe6hsrqixqwd9frma",
                                "scene": "page"
                            }
                        }
                    }

                    # 将请求数据转换为 JSON 字符串
                    json_data = json.dumps(data)

                    url = 'https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job'

                    headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Encoding': 'gzip, deflate, br, zstd',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Cookie': 'inited_user=1508f7e15374f5c662497f7e54cc075a; __gc_id=56b658ce9ef84a40ba9cd3e631284647; _ga=GA1.1.1517025605.1710725973; __uuid=1710725973358.79; need_bind_tel=false; c_flag=c6220a1bb750728113130636911f0893; imId=1e487899739262e483ff6016b82bfb4b; imId_0=1e487899739262e483ff6016b82bfb4b; imClientId=1e487899739262e41e5e88f68d8c8473; imClientId_0=1e487899739262e41e5e88f68d8c8473; _ga_54YTJKWN86=GS1.1.1717071858.9.0.1717071866.0.0.0; XSRF-TOKEN=Sk4f5POFQp-2bmZwiQm46Q; __tlog=1717075783974.26%7C00000000%7C00000000%7C00000000%7C00000000; UniqueKey=05c83a3a152699967ecd4408bb1e9b04; liepin_login_valid=0; lt_auth=vLwMOnMGzFz%2FsXnc2mcN5adIioj5Bmmc%2FSsNjREC0d7uDv234P%2FkQQ6HrbED%2FCoIqxxydagzMLf%2FMuj5zHtC70sX%2B1GkkICzuuW81mEHdvRcN8W2vfj%2BkcjXe58clUAB8mNbtkI%3D; access_system=C; hpo_role-sec_project=sec_project_liepin; hpo_sec_tenant=0; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1717071862,1717075887; user_roles=0; user_photo=5f8fa3a9dfb13a7dee343d4808u.png; user_name=%E8%A6%81%E7%A6%BB%E5%BC%80; new_user=false; acw_tc=2760829a17170758873383400ea085dd55bebbaa70a4a1b9e90593bcd884af; imApp_0=1; inited_user=1508f7e15374f5c662497f7e54cc075a; fe_im_opened_pages=; fe_im_connectJson_0=%7B%220_05c83a3a152699967ecd4408bb1e9b04%22%3A%7B%22socketConnect%22%3A%222%22%2C%22connectDomain%22%3A%22liepin.com%22%7D%7D; __session_seq=13; __uv_seq=16; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1717076077; __tlg_event_seq=31; fe_im_socketSequence_new_0=6_6_5',
                        'Host': 'api-c.liepin.com',
                        'Origin': 'https://www.liepin.com',
                        'Referer': 'https://www.liepin.com/',
                        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                        'Sec-Ch-Ua-Mobile': '?0',
                        'Sec-Ch-Ua-Platform': '"Windows"',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                        'X-Client-Type': 'web',
                        'X-Fscp-Bi-Stat': '{"location": "https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=2&pageSize=40&key=%E4%BC%9A%E8%AE%A1&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salary=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&sfrom=search_job_pc&ckId=uhzrclzer8682dt2kzjghptp6fypx9h8&skId=sp4jb97xndy4mffxe6hsrqixqwd9frma&fkId=sp4jb97xndy4mffxe6hsrqixqwd9frma&scene=page&suggestId="}',
                        'X-Fscp-Fe-Version': '',
                        'X-Fscp-Std-Info': '{"client_id": "40108"}',
                        'X-Fscp-Trace-Id': '0d179b97-4120-4a54-ab1f-7e4bead44905',
                        'X-Fscp-Version': '1.1',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-Xsrf-Token': 'o-zeJD8bS9-w_hf07HpN9w',
                    }

                    # 发送 POST 请求，并使用代理
                    yield scrapy.Request(url=url, method='POST', headers=headers, body=json_data, callback=self.parse)



    def parse(self, response):
        # 解析响应数据
        data = json.loads(response.body)
        # print(data)
        # 提取目标链接列表
        target_links = []
        job_card_list = data['data']['data']['jobCardList']
        for job_card in job_card_list:
            job_link = job_card['job']['link']
            # 将url_list传递给下一个回调函数parse_details
            yield scrapy.Request(url=job_link, callback=self.parse_details_page)

    def parse_details_page(self, response):
        # 在这里处理详情页的具体解析
        try:
            item = LiepinItem()
            # 职位title
            title = response.xpath('//span[@class="name ellipsis-2"]/text()').get()
            # # 当链接出错的时候进行重试
            # if not title.strip():
            #     retry_times = response.meta.get('retry_times', 0)
            #     if retry_times < 3:  # 最多重试3次
            #         retry_times += 1
            #         print('Retry..............', retry_times)
            #         # 重新发起请求，将重试次数传递到 meta 中
            #         yield scrapy.Request(url=response.url, callback=self.parse_details_page,
            #                              meta={'retry_times': retry_times})
            #         return
            item['title'] = title
            # 薪资
            item['salary'] = response.xpath('//span[@class="salary"]/text()').get()
            print(title)

            # 公司名称
            item['company_name'] = response.xpath('//div[@class="name ellipsis-1"]/text()').get()

            # 公司介绍
            item['company_intro'] = response.xpath('//div[@class="inner ellipsis-3"]/text()').get()

            # 职位介绍
            item['job_intro'] = response.xpath('//dd[@data-selector="job-intro-content"]/text()').get()

            # 职位地区
            item['job_loca'] = response.xpath('/html/body/section[3]/div[1]/div[3]/span[1]/text()').get()

            # 经验
            item['job_exp'] = response.xpath('/html/body/section[3]/div[1]/div[3]/span[3]/text()').get()

            # 学历
            item['job_educate'] = response.xpath('/html/body/section[3]/div[1]/div[3]/span[5]/text()').get()
            # 关键词
            key_word_elements = response.xpath('//div[@class="tag-box"]/ul/li/text()')
            item['key_word_list'] = [key_word_elements[i].get() for i in range(len(key_word_elements))]

            # 提取信息并存储在列表中
            item['company_info'] = [
                response.xpath('//div[@class="company-other"]/div[1]/span[@class="text"]/text()').get(),  # 企业行业
                response.xpath('//div[@class="company-other"]/div[2]/span[@class="text"]/text()').get(),  # 人数规模
                response.xpath('//div[@class="company-other"]/div[3]/span[@class="text"]/text()').get(),  # 职位地址
                response.xpath('//div[@class="register-info"]/div[1]/span[@class="text"]/text()').get(),  # 注册时间
                response.xpath('//div[@class="register-info"]/div[2]/span[@class="text"]/text()').get(),  # 注册资本
                response.xpath('//div[@class="register-info"]/div[3]/span[@class="text"]/text()').get()  # 经营范围
            ]

            # 详情链接
            item['details_url'] = response.url
            yield item
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            # self.logger.error(f"Response URL: {response.url}")
            # self.logger.error(f"Response body: {response.body}")
