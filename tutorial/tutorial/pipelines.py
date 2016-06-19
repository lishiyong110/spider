# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class TutorialPipeline(object):
    def process_item(self, item, spider):
        link_href = "http://bj.lianjia.com/%s" %(item["link_href"][0])

        try:
            com_price = int(item["com_price"][0])
        except:
            com_price = 0

        if item["build_time"].find("未知") >= 0:
            build_time = 9999
        elif item["build_time"].find("年") >= 0:
            build_time = int(item["build_time"].split("年")[0])
        else:
            build_time = 9999

        print "%s\t%s\t%s\t%s\t%s\t%s" %(
            item["title_name"], 
            link_href, 
            com_price, 
            build_time, 
            item["zone_name"], 
            item["district_name"]
        )
        return item
