#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_ANTISPAM_ZHIDAO_IRRELEVANT_CLASSIFICATION_V1_GPU Demo, 以及压测数据生成的DEMO
Author: niushixiong(niushixiong01@baidu.com)
Date: 2023-09-01
Filename: FEATURE_ANTISPAM_ZHIDAO_IRRELEVANT_CLASSIFICATION_V1_GPU.py
"""
import os

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import requests


def feature_calculate(url="", xvision_online_url="", job_name="", feature_name="", title="", cont=""):
    """
    功能：特征计算
    输入：
        url,xvision_online_url,job_name,feature_name,title,cont
    输出：
        none        
    """
    token = ''
    logid = str(random.randint(1000000, 100000000))
    request_ip = "10.23.4.55"

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': feature_name,
    }
    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {
            "business_name": job_name,
            "feature_name": feature_name
        }

    data = {
        "req": {"text_a": title, "text_b": cont},
        "model_type": "IrrelevantBertBlendCNNModel",
        "business_name": job_name,
        "feature_name": feature_name,
        "logid": logid,
        "request_ip": request_ip
    }
    try:
        request_json = json.dumps(data)
    except:
        request_json = json.dumps(data, encoding='gb18030')
    res = requests.post(url, params=params, data=request_json, headers=headers)
    # 打印输出
    print(res.json())


def prepare_request(title, cont, job_name="", feature_name=""):
    """
    功能：构建算子的输入数据
    输入：tile, content, job_name, feature_name
    输出： requst_json
    """
    logid = str(random.randint(1000000, 100000000))
    request_ip = "10.23.4.55"
    data = {
        "req": {"text_a": title, "text_b": cont},
        "model_type": "IrrelevantBertBlendCNNModel",
        "business_name": job_name,
        "feature_name": feature_name,
        "logid": logid,
        "request_ip": request_ip
    }
    try:
        request_json = json.dumps(data)
    except:
        request_json = json.dumps(data, encoding='gb18030')
    return request_json


def gen_stress_data():
    """
    功能：生成压测数据
    输出：
        压测数据
    """
    job_name = ""
    feature_name = ""
    for line in sys.stdin:
        sp = line.split("\t")
        title = sp[0]
        cont = sp[1]
        title = title.decode("gb18030", "ignore")
        cont = cont.decode("gb18030", "ignore")
        print(prepare_request(title, cont,
              job_name=job_name, feature_name=feature_name))


if __name__ == '__main__':
    """
    main
    """
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    xdemo = XvisionDemo()
    url = xdemo.xvision_online_url + xdemo.xvision_sync_path
    job_name = ""
    feature_name = ""

    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        gen_stress_data()
    else:
        # 特征计算Demo
        title = "山东日照丁德增液压开普菱QQ号是多少？"
        cont = "以腾讯凳拍视频APP版本:8.2.78.21637为例，由于腾讯视频内不同账号之间会员\
            权益不互通需使用开通的会员账号登录腾讯视频观影。若显示非会员，请退出帐号重新登\
            录查看，客户端版本过低也会导致会员状态显示不正确，建议可以尝试重新下载安旁\
            宏装下腾讯视频客户端再登录查看运粗册。【fh.ihzg.com.cn/news/30591.mp3】【vq.51mg.cn/news/01267.mp3】"
        feature_calculate(url, xdemo.xvision_online_url,
                          job_name, feature_name, title=title, cont=cont)
