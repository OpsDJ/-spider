import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from urllib.parse import urljoin
import random
import time
import os

url = f"https://www.zhipin.com/web/geek/job?query=python&city=101110100&page=1"

# 创建浏览器实例
driver = webdriver.Chrome()
# 打开浏览器
driver.get(url)
input('请在网页中完成登录，登录完成输入回车结束')
# 记录程序开始时间
start_time = time.time()
# 输入关键词
key_words = ['Python']
# 输入不同的城市代码

# 城市名称: 北京 ，code值: 101010100
city_list = [101230200, 101250100, 101270100, 101180100, 101040100]
# 设置循环的页数
max_page = 10
for city in city_list:
    for key_word in key_words:
        for page in range(1, max_page + 1):
            # 创建url
            url = f"https://www.zhipin.com/web/geek/job?query={key_word}&city={city}&page={page}"
            # 打开浏览器
            driver.get(url)
            # 向下滚动页面
            driver.execute_script("window.scrollBy(0, 1000);")  # 向下滚动1000个像素
            time.sleep(random.uniform(1, 3))
            # 向上滚动页面
            driver.execute_script("window.scrollBy(0, -1000);")  # 向上滚动1000个像素
            # 等待页面加载完成
            try:
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="job-name"]')))
            except:
                print('主页面未加载。。。。。。。。。。。。')
                print('请打开浏览器通过验证，输入回车结束')
                input()
            # 获取selenium渲染等待后的页面源码
            page_source = driver.page_source
            # 封装成HTML对象
            tree = etree.HTML(page_source)
            # 获取网页职位的url地址
            url_list = tree.xpath('//ul[@class="job-list-box"]/li/div/a/@href')
            # 遍历每个职位的卡片
            for job_detail_url in url_list:
                # 提取每个职位详情页的链接
                full_url = urljoin(url, job_detail_url)
                print(full_url)
                # 对于每个职位，发起请求到职位详情页
                # 初始化WebDriver
                driver.get(full_url)
                # 向下滚动页面
                driver.execute_script("window.scrollBy(0, 1000);")  # 向下滚动1000个像素
                # 反爬
                time.sleep(random.uniform(2, 3))
                # 向上滚动页面
                driver.execute_script("window.scrollBy(0, -1000);")  # 向上滚动1000个像素
                # 等待页面加载完成
                try:
                    wait = WebDriverWait(driver, 30)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@title]')))
                except:
                    print('详情页面未加载。。。。。。。。。。。。')
                    print('请打开浏览器通过验证，输入回车结束')
                    input()
                time.sleep(random.uniform(2, 3))
                # 获取selenium渲染等待后的页面源码
                page_source = driver.page_source
                # 封装成HTML对象
                tree = etree.HTML(page_source)
                # 提取职位页面上的详细信息
                try:
                    job_title = tree.xpath('//h1[@title]/text()')[0].strip()
                except:
                    job_title = 'None'
                try:
                    salary = tree.xpath('//span[@class="salary"]/text()')[0].strip()
                except:
                    salary = 'None'
                try:
                    job_location = tree.xpath('//a[@class="text-desc text-city"]/text()')[0].strip()
                except:
                    job_location = 'None'
                try:
                    experience = tree.xpath('//span[@class="text-desc text-experiece"]/text()')[0].strip()
                except:
                    experience = None
                try:
                    education = tree.xpath('//span[@class="text-desc text-degree"]/text()')[0].strip()
                except:
                    experience = None
                try:
                    company_name = tree.xpath('//li[@class="company-name"]/text()')[0].strip()
                except:
                    try:
                        company_name = tree.xpath('//div[@class="company-info"]/a[2]/text()')[0].strip()
                    except:
                        company_name = None
                try:
                    job_description = "".join(tree.xpath('//div[@class="job-sec-text"]/text()'))
                except:
                    job_description = None
                try:
                    skills = ",".join(tree.xpath('//ul[@class="job-keyword-list"]/li/text()'))
                except:
                    skills = None
                print(skills)
                print('当前的主页位于', url)
                # 检查文件是否存在，如果不存在则创建文件并写入表头
                file_exists = os.path.isfile(f'job_data_{key_word}.csv')
                with open(f'job_data_{key_word}.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(
                            ['Job Title', 'Salary', 'Location', 'Experience', 'Education', 'Company Name',
                             'Job Description',
                             'Skills', 'URL'])
                    writer.writerow(
                        [job_title, salary, job_location, experience, education, company_name, job_description, skills,
                         full_url])
end_time = time.time()

print("程序工耗时间", end_time - start_time)
# 关闭浏览器实例
driver.close()
