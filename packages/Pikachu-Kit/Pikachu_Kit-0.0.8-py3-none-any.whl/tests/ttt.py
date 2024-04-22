# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@time: 2023/2/11 17:41 $
@desc:

"""
import json
import os
import time
from datetime import datetime
import random
import traceback
from lxml import etree
from DrissionPage import WebPage, ChromiumOptions, SessionOptions


class DrissionPageDemo(object):
    """

    """

    def __init__(self):
        """

        """
        self.get_page()


    def get_page(self, ua=None, incognito=False, time_out=60, headless=False, cookies=None):
        """

        :param ua:
        :param incognito:
        :return:
        """
        self.page = None
        co = ChromiumOptions()
        so = SessionOptions()
        # co.set_argument('--window-size', '800,600')
        co.auto_port(True)
        co.headless(headless)
        co.ignore_certificate_errors(True)
        co.mute(True)
        co.set_timeouts(page_load=time_out)

        self.page = WebPage()

        return self.page

    def get_html(self,url):
        self.page.get(url)
        time.sleep(random.randint(3,5))
        # print(self.page.html)
        return self.page.html

    def parse_html(self,html):
        tree = etree.HTML(html)
        lis = tree.xpath('//div[@class="tit"]')
        for li in lis:
            detail_url = li.xpath("./a/@href")
            yield detail_url[0]

    def parse_detail(self,html):
        tree = etree.HTML(html)
        name = tree.xpath('//h1[@class="shop-name"]//text()')[0]
        address =tree.xpath('//span[@id="address"]//text()')[0]
        phone = "".join(tree.xpath('//div[@id="basic-info"]/p[1]//text()')).replace("电话：","")
        return name,address,phone





if __name__ == '__main__':
    dp = DrissionPageDemo()
    with open("./1.txt","w",encoding="utf-8")as fp:
        for i in range(7,47):
            html = dp.get_html(f"https://www.dianping.com/search/keyword/7/0_%E4%B8%AD%E5%8C%BB/p{i}")
            for detail_url in dp.parse_html(html):
                detail_html = dp.get_html(detail_url)
                name,address,phone = dp.parse_detail(detail_html)
                fp.write(f"{name}\t{address}\t{phone}\t\n")
                fp.flush()
                time.sleep(random.randint(5,15))
