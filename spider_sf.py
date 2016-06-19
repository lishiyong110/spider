#!/usr/bin/env python
#-*-coding:utf-8 -*-

import sys

import re
import urllib2

import requests

from bs4 import BeautifulSoup

class BestSpider(object):
    def __init__(self):
        pass

    def get_page(self, url, dis):
        distric_name = dis

        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)", 
                   "Referer": url
                  }

        request = requests.get(url, headers = headers)
        #request.encoding = "utf-8"
        allinfo = request.text

        soup = BeautifulSoup(allinfo, "html.parser")
        m_all_community = soup.find(class_ = "houseList").find_all(id = "Div1")
        if not m_all_community:
            return False

        for com in m_all_community:
            try:
                com_price = com.find(class_ = "price").string
            except:
                com_price = "0"
            title_name = com.find(class_ = "info rel floatl ml15").find_all(target = "_blank")[0].string
            href_link = com.find(class_ = "info rel floatl ml15").find_all(target = "_blank")[0].get("href")
            zone_name = com.find(class_ = "info rel floatl ml15").find_all(target = "_blank")[1].string
            build_time = "0000"
            print "%s\t%s\t%s\t%s\t%s\t%s" %(title_name, href_link, com_price, build_time, distric_name, zone_name)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

    spider = BestSpider()

    districs = {"haidian": 0, 
                "chaoyang": 1, 
                "dongcheng": 2, 
                "xicheng": 3, 
                "fengtai": 6, 
                "shijingshan": 7, 
                "fangshan": 8, 
                "mentougou": 9, 
                "tongzhou": 10, 
                "shunyi": 11, 
                "changping": 12, 
                "miyun": 13, 
                "huairou": 14, 
                "yanqing": 15, 
                "pinggu": 16, 
                "daxing": 585, 
                "yanjiao": 987
    }

    for dis in districs:
        base_url = "http://esf.fang.com/housing/%d__0_0_0_0" %(districs[dis])
        page_num = 1

        while page_num < 101:
            url = "%s_%d_0_0/" %(base_url, page_num)
            #try:
            #    res = spider.get_page(url)
            #except Exception,e:
            #    print e
            res = spider.get_page(url, dis)
            if res == False:
                break

            page_num += 1
