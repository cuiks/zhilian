# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
import pymongo

from zhilian.settings import Mongoip,MongoPort,MongoDBname,MongoItem


class ZhilianPipeline(object):
    def process_item(self, item, spider):
        return item

class Pipeline_ToCSV(object):

    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '\zhilian.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'a', newline='', encoding='UTF-8-sig')
        # csv写法
        self.writer = csv.writer(self.file)
        # 写入头
        self.writer.writerow(['position','title','salary','place','experience',
                              'education','need','job_desc','job_place','com_overview',
                              'company','com_type','com_nature','com_scale','com_url',
                              'com_place','welfare'])

    def process_item(self, item, spider):
        self.writer.writerow([item['position'], item['title'], item['salary'], item['place'],
                              item['experience'], item['education'], item['need'], item['job_desc'],
                              item['job_place'], item['com_overview'], item['company'], item['com_type'],
                              item['com_nature'], item['com_scale'], item['com_url'], item['com_place'],
                              item['welfare']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()

class MongoPipeline(object):
    def __init__(self):
        host=Mongoip
        port=MongoPort
        dbName=MongoDBname
        client=pymongo.MongoClient(host=host,port=port)    # 创建连接对象client
        db=client[dbName]                          # 使用文档dbName='datago306'
        self.post = db[MongoItem]                  # 使用item MongoItem='jobItem'

    def process_item(self, item, spider):
        job_info = dict(item)                      # item转换为字典格式
        self.post.insert(job_info)                 # 将item写入mongo
        return item


