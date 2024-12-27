# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Boss.py
# Time       ：2024-06-20-11-23-02
# version    ：python 3.9
# Description：
"""
import json

from DrissionPage import ChromiumPage
from DataRecorder import Recorder



# 登录Boss直聘
def login_account_no():
    page.get(f'https://www.zhipin.com/')
    # page.wait.load_start()
    # sleep(1)
    log_btn = page.ele('t:a@@class:header-login-btn')
    if log_btn:
        user_input = input('用户完成登录后，输入Y后继续：')
        if user_input.upper() == "Y":
            print('当前已经手动登录完成！')


# 根据输入的中文名获取城市数据
def query_city_code(jobname, city='宁波'):
    city_code = '101210400'
    page.get(f'https://www.zhipin.com/web/geek/job?query={jobname}')
    page.listen.start('zpgeek/common/data/city/site.json')
    packet1 = page.listen.wait()
    siteList = packet1.response.body['zpData']['siteList']
    city_array = {}
    for site in siteList:
        tmp_city_list = site['subLevelModelList']
        if tmp_city_list:
            for cItem in tmp_city_list:
                city_array[cItem['name']] = cItem['code']
    # print(f'全国主要城市的清单为：{city_array}')
    try:
        city_code = city_array[city[:2]]
    except KeyError:
        pass
    return city_code


def query_and_download(job_name, city_code):
    query_job_info(job_name, city_code)


def query_job_info(keyword, city_code, pageno=1):
    print(f'当前开始查询并采集第{pageno}页数据！')

    page.listen.start('zpgeek/search/joblist.json')  # 监控接口
    targetUrl = f'https://www.zhipin.com/web/geek/job?query={keyword}&city={city_code}&page={pageno}'

    page.get(targetUrl)

    packet = page.listen.wait()

    # print(packet.response)

    jobList = packet.response.body['zpData']['jobList']
    jobCount = packet.response.body['zpData']['totalCount']
    data_list = []
    for job in jobList:
        jobName = job['jobName']
        salaryDesc = job['salaryDesc']
        jobExperience = job['jobExperience']
        jobDegree = job['jobDegree']
        cityName = job['cityName']
        areaDistrict = job['areaDistrict']
        businessDistrict = job['businessDistrict']
        brandName = job['brandName']
        brandIndustry = job['brandIndustry']
        brandStageName = job['brandStageName']
        brandScaleName = job['brandScaleName']
        welfareList = ','.join(job['welfareList'])
        skills = ','.join(job['skills'])
        encryptJobId = job['encryptJobId']
        securityId = job['securityId']
        # 构造详情页请求地址
        descUrl = "https://www.zhipin.com/job_detail/" + encryptJobId + ".html?" + "&" + securityId + "&sessionId="
        jobDesc = query_job_description(descUrl)

        print(jobName, salaryDesc, jobExperience, jobDegree, cityName, areaDistrict, businessDistrict, brandName,
              brandIndustry, brandStageName, brandScaleName, welfareList, skills, jobDesc)
        data_list.append(
            [jobName, salaryDesc, jobExperience, jobDegree, cityName, areaDistrict, businessDistrict, brandName,
             brandIndustry, brandStageName, brandScaleName, welfareList, skills, jobDesc])
    r.add_data(data_list)
    r.record()
    if jobCount > (pageno * 30):
        query_job_info(keyword, city_code, pageno + 1)


def query_job_description(descUrl):
    # 开始监听接口
    page.listen.start(descUrl)

    # 获取接口数据
    page.get(descUrl)

    # 等待监听到数据包
    page.listen.wait()

    # 使用XPath获取工作描述信息
    try:
        jobDesc = page.ele('.job-sec-text').text
    except:
        jobDesc = ""
    # 返回工作描述信息
    return jobDesc


if __name__ == "__main__":

    # # 打开名为 city.json 的文件并读取其中的内容
    # with open('city.json', 'r', encoding='utf-8') as file:
    #     json_data = file.read()
    #
    # # 使用 json.loads() 方法将 JSON 字符串加载为 Python 字典
    # data = json.loads(json_data)
    #
    # # 提取所有 subLevelModelList 中的 code 值
    # sublevel_codes = []
    # for city in data['zpData']['hotCityList']:
    #     sublevel_codes.append(city['code'])
    #
    # # 打印提取的 subLevelModelList 中的 code 值
    # print("提取的 subLevelModelList 中的 code 值：", sublevel_codes)

    # 从文件中读取数据
    with open('city-c.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用逗号分隔字符串，并生成列表
    sublevel_codes = content.split(',')

    # 打印转换后的列表
    print("转换后的列表：", sublevel_codes)

    r = Recorder('Boss直聘数据.xlsx')
    r.add_data(['jobName', 'salaryDesc', 'jobExperience', 'jobDegree', 'cityName', 'areaDistrict', 'businessDistrict',
                'brandName', 'brandIndustry', 'brandStageName', 'brandScaleName', 'welfareList', 'skills', 'jobDesc'])
    r.record()

    page = ChromiumPage()

    # login_account_no()

    jobName = "数据分析"

    print(f'你输入的关键词为：{jobName}')
    city_code = sublevel_codes
    print(city_code)
    for city in city_code:
        print("正在爬取", city)
        # 开始采集数据
        try:
            query_job_info(jobName, int(city))
        except Exception as e:
            print(e)
            print("BAD!")
            pass
