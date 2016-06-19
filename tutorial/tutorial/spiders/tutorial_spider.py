#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import scrapy
from tutorial.items import TutorialItem

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class tutorial_spider(CrawlSpider):
    name = "tutorial"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "http://bj.lianjia.com/xiaoqu/haidian", 
        "http://bj.lianjia.com/xiaoqu/dongcheng", 
        "http://bj.lianjia.com/xiaoqu/xicheng", 
        "http://bj.lianjia.com/xiaoqu/chaoyang", 
        "http://bj.lianjia.com/xiaoqu/fengtai", 
        "http://bj.lianjia.com/xiaoqu/daxing", 
        "http://bj.lianjia.com/xiaoqu/shijingshan", 
        "http://bj.lianjia.com/xiaoqu/changping", 
        "http://bj.lianjia.com/xiaoqu/fangshan", 
    ]

    #rules = (
    #    #Rule(LinkExtractor(allow=(r"bj.lianjia.com/xiaoqu/haidian/pg\d+")), callback = "parse_item"), 
    #    Rule(LinkExtractor(allow=(r"/xiaoqu/haidian/pg2")), callback = "parse_item"), 
    #)

    #def parse_item(self, response):
    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        items = []

        base_url = "/".join(response.url.split("/")[:5])
        district_name = base_url.split("/")[-1]
        for sel in response.xpath('//ul[@class="house-lst"]/li//div[@class="info-panel"]'):
            item = TutorialItem()
            item["title_name"] = sel.xpath("h2/a/@title").extract()[0]
            item["link_href"] = sel.xpath("h2/a/@href").extract()
            item["com_price"] = sel.xpath('.//div[@class="price"]//span[@class="num"]/text()').extract()
            item["build_time"] = sel.xpath('.//div[@class="con"]/text()').extract()[1]
            item["zone_name"] = sel.xpath('.//div[@class="con"]/a/@title').extract()[1]
            item["district_name"] = district_name
            items.append(item)
            yield item

        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        if len(page_data) == 1:
            cur_page = eval(page_data[0])["curPage"]
            total_page = eval(page_data[0])["totalPage"]
            if cur_page < total_page:
                next_url = "%s/pg%d" %(base_url, cur_page+1)
                req = Request(url=next_url, callback=self.parse)
                yield req

        #return items
