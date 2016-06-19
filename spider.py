#!/usr/bin/env python
#-*-coding:utf-8 -*-

import sys

import re
import urllib2

import requests

from bs4 import BeautifulSoup

class SimpleSpider(object):
    def __init__(self):
        pass

    def get_page(self, url):
    #""" @url: http://bj.lianjia.com/xiaoqu/$distric/$page_num """

        distric_name = url.split("/")[4]

        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        user_headers = {"User-Agent" : user_agent,
                        "Referer": url}
        request = urllib2.Request(url, headers=user_headers)
        f = urllib2.urlopen(request)
        allinfo = f.read()
        f.close()
        
        r_content = re.compile(r'<li><div class="pic-panel">(.*?)</div></li>')
        #r = re.compile(r'<li><div class="pic-panel">')
        m_all_community = r_content.findall(allinfo)
        if not m_all_community:
            return False

        for com in m_all_community:
            r1 = re.compile(r'<h2><a target="_blank" href="(.*)" title="(.*)">(.*?)</a></h2>')
            href_link = r1.search(com).group(1)
            title_name = r1.search(com).group(2)

            r2 = re.compile(r'<span class="num">(.*)<img')
            com_price = r2.search(com).group(1)

            r3 = re.compile(r'<span>/</span>(.*)</span>(.*?)年建造')
            build_time = r3.search(com).group(2)

            r4 = re.compile(r'<a href="(.*)" title="(.*)">(.*?)</a><span>')
            zone_name = r4.search(com).group(3)

            print "%s\t%s\t%s\t%s\t%s\t%s" %(title_name, href_link, com_price, build_time, distric_name, zone_name)

        return True

class ComplexSpider(object):
    def __init__(self):
        pass

    def get_page(self, url):
        distric_name = url.split("/")[4]

        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)", 
                   "Referer": url
                  }

        request = requests.get(url, headers = headers)
        request.encoding = "utf-8"
        allinfo = request.text

        r_content = re.compile(r'<li><div class="pic-panel">(.*?)</div></li>')
        m_all_community = r_content.findall(allinfo)
        if not m_all_community:
            return False

        for com in m_all_community:
            r1 = re.compile(r'<h2><a target="_blank" href="(.*)" title="(.*)">(.*?)</a></h2>')
            href_link = r1.search(com).group(1)
            title_name = r1.search(com).group(2)

            r2 = re.compile(r'<span class="num">(.*)<img')
            com_price = r2.search(com).group(1)

            r3 = re.compile(ur'<span>/</span>(.*)</span>(.*?)年建造')
            build_time = r3.search(com).group(2)

            r4 = re.compile(r'<a href="(.*)" title="(.*)">(.*?)</a><span>')
            zone_name = r4.search(com).group(3).encode("utf-8")

            print "%s\t%s\t%s\t%s\t%s\t%s" %(title_name, href_link, com_price, build_time, distric_name, zone_name)

        return True

class BestSpider(object):
    def __init__(self):
        pass

    def get_page(self, url):
        distric_name = url.split("/")[4]

        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)", 
                   "Referer": url
                  }

        request = requests.get(url, headers = headers)
        request.encoding = "utf-8"
        allinfo = request.text

        soup = BeautifulSoup(allinfo, "html.parser")
        m_all_community = soup.find_all(class_ = "info-panel")
        if not m_all_community:
            return False

        for com in m_all_community:
            title_name = com.find(target = "_blank").string
            href_link = com.find(target = "_blank").get("href")
            com_price = com.find(class_ = "price").find(class_ = "num").contents[0].string
            if com_price.find(u"span class") >= 0 or com_price.find("暂无均价") >= 0:
                com_price = "0"
            build_time = com.find(class_ = "other").find(class_ = "con").contents[-1].split("年")[0]
            zone_name = com.find(class_ = "other").find(class_ = "con").contents[1].string

            print "%s\t%s\t%s\t%s\t%s\t%s" %(title_name, href_link, com_price, build_time, distric_name, zone_name)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

    #spider = SimpleSpider()
    #spider = ComplexSpider()
    spider = BestSpider()

    districs = ["haidian", "chaoyang", "xicheng", "dongcheng", "shijingshan", "fengtai", 
                "tongzhou", "changping", "daxing", "yizhuangkaifaqu", "shunyi", "fangshan", 
                "mentougou", "pinggu", "huairou", "miyun", "yanqing", "yanjiao"]

    for dis in districs:
        base_url = "http://bj.lianjia.com/xiaoqu/%s" %(dis)
        page_num = 1

        while True:
            url = "%s/pg%d/" %(base_url, page_num)
            try:
                res = spider.get_page(url)
            except Exception,e:
                print e
            #res = spider.get_page(url)
            if res == False:
                break

            page_num += 1
