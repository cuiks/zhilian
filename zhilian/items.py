# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    place = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    need = scrapy.Field()
    job_desc = scrapy.Field()
    job_place = scrapy.Field()
    com_overview = scrapy.Field()
    company = scrapy.Field()
    com_type = scrapy.Field()
    com_nature = scrapy.Field()
    com_scale = scrapy.Field()
    com_url = scrapy.Field()
    com_place = scrapy.Field()
    welfare = scrapy.Field()
