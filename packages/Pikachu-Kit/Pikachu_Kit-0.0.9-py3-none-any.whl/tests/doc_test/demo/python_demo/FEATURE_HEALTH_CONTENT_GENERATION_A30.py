#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:对话转内容的接口
Author: wangyouya(wangyouya@baidu.com)
Date: 2023-06-01
Filename: FEATURE_HEALTH_CONTENT_GENERATION_A30.py 
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
    FEATURE_HEALTH_CONTENT_GENERATION_A30 demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：json串，参考示例
        输出：
            返回算子的输入数据
        """

        return json.dumps(data)


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
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_HEALTH_CONTENT_GENERATION_A30',
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
                print featureDemo.prepare_request(json.loads(line.strip())) #压测词表数据
                feature_calculate(json.loads(line.strip()))

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_HEALTH_CONTENT_GENERATION_A30.py 
    生成压测数据：
        python FEATURE_HEALTH_CONTENT_GENERATION_A30.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('test/') #本地的文本数据
    else:
        #特征计算Demo
        feature_calculate({"prompt":"得了新冠之后，需要做CT吗", "history":[]}) # 文本数据

