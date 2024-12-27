import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import csv

# 从文件中读取失败的请求URL
with open('failed_requests.txt') as f:
    failed_requests = [line.strip() for line in f.readlines()]

# 设置Selenium WebDriver
driver = webdriver.Chrome()

# 设置隐式等待时间
driver.implicitly_wait(3)

has_logged_in = False

# 打开CSV文件用于写入数据
with open('failed_requests_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(
        ['Company Name', 'Company Intro', 'Job Intro', 'Job Location', 'Job Experience', 'Job Education', 'Title',
         'Salary', 'Key Words', 'Company Info', 'Details URL'])

    for failed_request in failed_requests:
        driver.get(failed_request)
        if not has_logged_in:
            input('请登录')
            has_logged_in = True
        try:
            # 显式等待，等待特定元素加载完成（例如页面中的一个关键元素）
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="name ellipsis-2"]'))
            )
            time.sleep(1)
            res = driver.page_source
            tree = etree.HTML(res)

            # 提取数据
            try:
                title = tree.xpath('/html/body/section[3]/div[1]/div[1]/span[1]/span/text()')[0]
            except:
                title = ''
            try:
                salary = tree.xpath('//span[@class="salary"]/text()')[0]
            except:
                salary = ''
            try:
                company_name = tree.xpath('//div[@class="name ellipsis-1"]/text()')[0]
            except:
                company_name = ''
            try:
                company_intro = tree.xpath('//div[@class="inner ellipsis-3"]/text()')[0]
            except:
                company_intro = ''
            try:
                job_intro = tree.xpath('//dd[@data-selector="job-intro-content"]/text()')[0]
            except:
                job_intro = ''
            try:
                job_loca = tree.xpath('/html/body/section[3]/div[1]/div[3]/span[1]/text()')[0]
            except:
                job_loca = ''
            try:
                job_exp = tree.xpath('/html/body/section[3]/div[1]/div[3]/span[3]/text()')[0]
            except:
                job_exp = ''
            try:
                job_educate = tree.xpath('/html/body/section[3]/div[1]/div[3]/span[5]/text()')[0]
            except:
                job_educate = ''
            try:
                key_word_elements = tree.xpath('//div[@class="tag-box"]/ul/li/text()')
                key_word_list = ', '.join([element for element in key_word_elements])
            except:
                key_word_list = ''
            try:
                company_info = [
                    tree.xpath('//div[@class="company-other"]/div[1]/span[@class="text"]/text()'),  # 企业行业
                    tree.xpath('//div[@class="company-other"]/div[2]/span[@class="text"]/text()'),  # 人数规模
                    tree.xpath('//div[@class="company-other"]/div[3]/span[@class="text"]/text()'),  # 职位地址
                    tree.xpath('//div[@class="register-info"]/div[1]/span[@class="text"]/text()'),  # 注册时间
                    tree.xpath('//div[@class="register-info"]/div[2]/span[@class="text"]/text()'),  # 注册资本
                    tree.xpath('//div[@class="register-info"]/div[3]/span[@class="text"]/text()')  # 经营范围
                ]
            except:
                company_info = []
            try:
                company_info_str = ', '.join([''.join(info) for info in company_info])
            except:
                company_info_str = ''

            details_url = driver.current_url

            # 写入数据到CSV文件
            writer.writerow(
                [title, salary, company_name, company_intro, job_intro, job_loca, job_exp, job_educate, key_word_list,
                 company_info, details_url])
        except:
            print('Error ', failed_request)

# 关闭WebDriver
driver.quit()
