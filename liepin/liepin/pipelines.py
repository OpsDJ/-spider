# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv


class LiepinPipeline:
    def __init__(self):
        self.file = open('data.csv', 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Job Name', 'Salary', 'Company Name', 'Company Intro', 'Job Intro',
                              'Job Location', 'Job Experience', 'Job Education', 'key_word_list',
                              'company_info' 'Details URL'])

    def process_item(self, item, spider):
        self.writer.writerow([item['title'], item['salary'], item['company_name'], item['company_intro'],
                              item['job_intro'], item['job_loca'], item['job_exp'], item['job_educate'],
                              item['key_word_list'], item['company_info'], item['details_url']])
        print('pipline are ok!')
        return item

    def close_spider(self, spider):
        self.file.close()
