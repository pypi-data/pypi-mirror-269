#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_NLP_STR_TITLEPREDICTOR_CTRL_GPU Demo, 以及压测数据生成的DEMO
Author: liqinrui(liqinrui@baidu.com)
Date: 2021-05-07
Filename: FEATURE_NLP_STR_TITLEPREDICTOR_CTRL_GPU.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os

class FeatureReq(XvisionDemo):
    """
    FEATURE_NLP_STR_TITLEPREDICTOR_CTRL_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：json串，参考示例
        输出：
            返回算子的输入数据
        """

        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(data),
                })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NLP_STR_TITLEPREDICTOR_CTRL_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_test_url + featureDemo.xvision_sync_path
    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    file_list = sorted(os.listdir(input_dir)) #dir里边是文本列表，用于生成压测词表
    for file in file_list:
        with open(input_dir + '/' + file, "r") as fd:
            for line in fd:
                print featureDemo.prepare_request(line)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NLP_STR_TITLEPREDICTOR_CTRL_GPU.py 
    生成压测数据：
        python FEATURE_NLP_STR_TITLEPREDICTOR_CTRL_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/') #./dir/ 是本地的文本数据
    else:
        #特征计算Demo
        feature_calculate('{"text":"南亚小国斯里兰卡近几年发展突飞猛进，经济水平一路飙升\
            ，这一现象引起了美国的注意，有美国媒体在查阅资料后发现，斯里兰卡颠覆性逆袭的背后，\
            是中国的大力支持！据美国彭博社14日报道，斯里兰卡政府债券的收益在今年的亚洲各国美元\
            债券中名列第一，原因是在中国融资机制的帮助下，投资者们看好该国短期不会违约。彭博社的\
            数据显示，斯里兰卡债券本季度的回报率为15%，使今年迄今的涨幅达到25%，是2021年亚洲国\
            家以美元计价的债券中表现最好的。然而这个南亚小国在去年，还因为新冠肺炎疫情的影响，财政\
            几乎破产，不得不靠借债和发行国债度日。斯里兰卡的经济能够在短时间内快速扭转，这背后掩藏\
            了什么秘密？其实答案很简单，因为斯里兰卡与中国签署了15亿美元的货币互换协议，这一协议的\
            签订让许多投资者对斯里兰卡都有一定改观。有银行投资人员认为，中国此举相当于“拯救了斯里兰卡”。\
            如果接下来几个月内仍然没有国家愿意为他们注入资金，自己的债券继续负收益的话，政府将不得不走入\
            破产程序，用国家财产抵押给外资企业来救急，走到这一步时候就相当于已经陷入了深渊。值得注意的是，\
            对于中国的支援，斯里兰卡政府也十分感激，事实上，中国已经成为了斯里兰卡在金融上的重要盟友！根据斯\
            央行2020财年报告显示，2020年新冠疫情导致全球供应链中断，中国超过印度成为斯第一大贸易伙伴，\
            美国仍保持斯第三大贸易伙伴。2020年，中国、印度、美国对斯贸易总额为105亿美元，较2019年126亿美\
            元减少21亿美元。从国别看，斯对美、英、德、比利时、荷兰和意大利等国保持明显贸易顺差，而对包括\
            中国、印度、阿联酋、新加坡、马来西亚、日本等在内的亚洲国家均呈现逆差。报告称，为加强贸易平衡，\
            应增加对亚洲国家出口同时减少从亚洲国家进口。","ctrl":"147"}') # 本地文本
