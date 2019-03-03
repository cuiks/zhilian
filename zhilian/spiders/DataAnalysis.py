# -*- coding: utf-8 -*-
import json
import re
import time
import urllib

import requests

import scrapy
from scrapy.http import Request
from zhilian.items import ZhilianItem
from scrapy_redis.spiders import RedisSpider

class ZhilianSpider(scrapy.Spider):
    name = 'DataAnalysis'
    #岗位列表
    positions = ['Java开发', 'UI设计师', 'Web前端', 'PHP', 'Python', 'Android', '美工', '深度学习',
                 '算法工程师', 'Hadoop', 'Node.js', '数据开发', '数据分析师', '数据架构', '人工智能', '区块链',
                 '电气工程师', '电子工程师', 'PLC', '测试工程师', '设备工程师', '硬件工程师', '结构工程师',
                 '工艺工程师', '产品经理', '新媒体运营', '运营专员', '淘宝运营', '天猫运营', '产品助理',
                 '产品运营', '淘宝客服', '游戏运营', '编辑']


    page_url = 'https://sou.zhaopin.com/?jl=530&kw=Java开发&kt=3'

    base_url = 'https://fe-api.zhaopin.com/c/i/sou' \
               '?start=0&pageSize=60&cityId=530&workExperience=-1&education=-1' \
               '&companyType=-1&employmentType=-1&jobWelfareTag=-1' \
               '&kw={}&kt=3'
    # now_position = positions[-1]
    # Item = ZhilianItem()
    # allowed_domains = ['https://fe-api.zhaopin.com']

    # url = base_url.format(now_position)
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=60&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E6%B8%B8%E6%88%8F%E8%BF%90%E8%90%A5&kt=3']
    # redis_key = 'zhihu:start_urls'

    def parse(self, response):
        for position in self.positions:
            url = self.base_url.format(position)
            print(url)
            yield Request(url=url,callback=self.parse_item,meta={'position':position},dont_filter=True)

    def parse_item(self, response):
        position = response.meta.get('position')
        #请求ajax加载json
        data = response.text
        #解析json
        data = json.loads(data)
        # 获取当前页所有职位,返回值为[{},{},{}...]
        results = data['data']['results']
        first_number = results[0]['number']
        for result in results:
            welfare = ','.join(result['welfare'])
            positionURL = result['positionURL']
            # self.Item['position'] = self.now_position
            if urllib.parse.urlparse(positionURL).netloc == 'jobs.zhaopin.com':
                # if response.meta.get('position'):
                #     position = response.meta.get('position')
                # else:
                #     position = '编辑'
                yield Request(url=positionURL, callback=self.parse_details, meta={'welfare': welfare,'position':position})
        # # 岗位列表是否为空为进入条件
        # if len(self.positions)>=0:
        #构造next_url
        now_page_num = re.findall(r'start=(.*?)&',response.url)[0]
        next_url = re.sub(r'start=(.*?)&','start='+str(int(now_page_num)+60)+'&',response.url)
        #请求下一页json
        res_next = requests.get(next_url)
        #判断下一页json是否为空
        if len(json.loads(res_next.text)['data']['results']) != 0 and json.loads(res_next.text)['data']['results'][0]['number'] != first_number:
            yield Request(url=next_url, callback=self.parse_item, meta={'position': position})
        #     # print(next_url)
        #     # print('返回为0跳转')
        #     # print('***************************')
        #     # position = self.positions.pop()
        #     next_url_temp = re.sub(r'start=(.*?)&', 'start=' + str(0) + '&', response.url)
        #     next_url = re.sub(r'kw=(.*?)&','kw='+position+'&',next_url_temp)
        # #判断下一页json中的第一个item和当前页的第一个item是否相同
        # elif json.loads(res_next.text)['data']['results'][0]['number'] != first_number:
        #     # print(next_url)
        #     # print('返回重复跳转')
        #     # print('***************************')
        #     # position = self.positions.pop()
        #     next_url_temp = re.sub(r'start=(.*?)&', 'start=' + str(0) + '&', response.url)
        #     next_url = re.sub(r'kw=(.*?)&', 'kw=' + position + '&', next_url_temp)

        # print('***********************************')
        # print(next_url)
        # print('***********************************')



    #获取职位详情页面详细信息
    def parse_details(self,response):
        title = response.css('body > div.wrap > div.main > div.main1.cl.main1-stat > div > ul > li:nth-child(1) > h1::text').extract_first('')
        salary = response.css('body > div.wrap > div.main > div.main1.cl.main1-stat > div > ul > li:nth-child(1) > div.l.info-money > strong::text').extract_first('')
        place = response.css('body > div.wrap > div.main > div.main1.cl.main1-stat > div > ul > li.clearfix > div.info-three.l > span:nth-child(1) > a::text').extract_first('')
        experience = response.css('body > div.wrap > div.main > div.main1.cl.main1-stat > div > ul > li.clearfix > div.info-three.l > span:nth-child(2)::text').extract_first('')
        education = response.css('body > div.wrap > div.main > div.main1.cl.main1-stat > div > ul > li.clearfix > div.info-three.l > span:nth-child(3)::text').extract_first('')
        need = response.css('body > div.wrap > div.main > div.main1.cl.main1-stat > div > ul > li.clearfix > div.info-three.l > span:nth-child(4)::text').extract_first('')
        job_desc = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-in > div.responsibility.pos-common').extract_first('')
        job_desc = re.sub(r'<.*?>','',job_desc).replace('\n',' ').replace('展开','').strip()
        job_place = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-in > div.pos-common.work-add.cl > p.add-txt::text').extract_first('')
        com_overview = response.css('body > div.wrap > div.main > div.main-add1.cl > div > div').extract_first('')
        com_overview = re.sub(r'<.*?>','',com_overview).replace('\n',' ').replace('展开','').strip()
        company = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-right > div.promulgator-info.clearfix > h3 > a::text').extract_first('')
        com_type = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-right > div.promulgator-info.clearfix > ul > li:nth-child(1) > strong > a::text').extract_first('')
        com_nature = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-right > div.promulgator-info.clearfix > ul > li:nth-child(2) > strong::text').extract_first('')
        com_scale = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-right > div.promulgator-info.clearfix > ul > li:nth-child(3) > strong::text').extract_first('')
        com_url = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-right > div.promulgator-info.clearfix > ul > li:nth-child(4) > strong > a::text').extract_first('')
        com_place = response.css('body > div.wrap > div.main > div.pos-info.cl > div.l.pos-info-right > div.promulgator-info.clearfix > ul > li:nth-child(5) > strong::text').extract_first('').replace('\n',' ')


        # self.Item['welfare'] = response.meta.get('welfare')
        # self.Item['title'] = title
        # self.Item['salary'] = salary
        # self.Item['place'] = place
        # self.Item['experience'] = experience
        # self.Item['education'] = education
        # self.Item['need'] = need
        # self.Item['job_desc'] = job_desc
        # self.Item['job_place'] = job_place
        # self.Item['com_overview'] = com_overview
        # self.Item['company'] = company
        # self.Item['com_type'] = com_type
        # self.Item['com_nature'] = com_nature
        # self.Item['com_scale'] = com_scale
        # self.Item['com_url'] = com_url
        # self.Item['com_place'] = com_place
        # yield self.Item

        Item = ZhilianItem()
        Item['welfare'] = response.meta.get('welfare')
        Item['position'] = response.meta.get('position')
        Item['title'] = title
        Item['salary'] = salary
        Item['place'] = place
        Item['experience'] = experience
        Item['education'] = education
        Item['need'] = need
        Item['job_desc'] = job_desc
        Item['job_place'] = job_place
        Item['com_overview'] = com_overview
        Item['company'] = company
        Item['com_type'] = com_type
        Item['com_nature'] = com_nature
        Item['com_scale'] = com_scale
        Item['com_url'] = com_url
        Item['com_place'] = com_place
        yield Item
