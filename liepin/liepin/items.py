# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位标题
    title = scrapy.Field()

    # 薪资
    salary = scrapy.Field()

    # 公司名称
    company_name = scrapy.Field()

    # 公司介绍
    company_intro = scrapy.Field()

    # 职位介绍
    job_intro = scrapy.Field()

    # 职位地区
    job_loca = scrapy.Field()

    # 经验
    job_exp = scrapy.Field()

    # 学历
    job_educate = scrapy.Field()

    # 详情链接
    details_url = scrapy.Field()

    # 关键词
    key_word_list = scrapy.Field()

    # 公司详情
    company_info = scrapy.Field()