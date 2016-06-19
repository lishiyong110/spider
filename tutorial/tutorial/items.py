# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_name = scrapy.Field()
    link_href = scrapy.Field()
    com_price = scrapy.Field()
    build_time = scrapy.Field()
    zone_name = scrapy.Field()
    district_name = scrapy.Field()
