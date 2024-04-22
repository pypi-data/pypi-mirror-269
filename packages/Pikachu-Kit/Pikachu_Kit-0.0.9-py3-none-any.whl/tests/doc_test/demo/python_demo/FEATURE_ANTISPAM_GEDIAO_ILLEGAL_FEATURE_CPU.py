#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_ANTISPAM_GEDIAO_ILLEGAL_FEATURE_CPU Demo, 以及压测数据生成的DEMO
Author: hupeng08(hupeng08@baidu.com)
Date: 2021-07-31
Filename: FEATURE_ANTISPAM_GEDIAO_ILLEGAL_FEATURE_CPU.py 
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
    FEATURE_ANTISPAM_GEDIAO_ILLEGAL_FEATURE_CPU demo  
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
        文本色情预测得分
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_ANTISPAM_GEDIAO_ILLEGAL_FEATURE_CPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path
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


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_data:（文本）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_file, "r") as fin:
        for i in fin:
            data = i.strip()
            print featureDemo.prepare_request(data)  #压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_ANTISPAM_GEDIAO_ILLEGAL_FEATURE_CPU.py 
    生成压测数据：
        python FEATURE_ANTISPAM_GEDIAO_ILLEGAL_FEATURE_CPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/anti_text.txt')  #./text_dir/anti_text.txt 是本地的文本数据
    else:
        #特征计算Demo
        feature_calculate(json.dumps({"check_type": "illegal", "check_text": ["大麻"]}))  # "大麻" 是本地测试数据
