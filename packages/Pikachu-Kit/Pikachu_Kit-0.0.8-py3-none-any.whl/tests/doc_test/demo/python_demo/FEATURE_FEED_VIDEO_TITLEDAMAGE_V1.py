#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_FEED_VIDEO_TITLEDAMAGE_V1 Demo, 以及压测数据生成的DEMO
Author: yuanruiting(yuanruiting@baidu.com)
Date: 2019-08-31
Filename: FEATURE_FEED_VIDEO_TITLEDAMAGE_V1.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import random
import base64
import urllib
import sys
import os

class FeatureReq(XvisionDemo):
    """
    FEATURE_FEED_VIDEO_TITLEDAMAGE_V1 demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型 or string，算子处理对象（text）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_data = "svc_name=title_damage_core&text_utf8=" + urllib.quote(data['text'])
        return req_data


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地文本文件
    输出：
        文本特征
    """
    featureDemo = FeatureReq()

    #生成算子输入
    data = {
            "text": open(input_data).readline()
         }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_FEED_VIDEO_TITLEDAMAGE_V1',
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
        input_data:（视频/图片/音频/文本）
    输出：
        压测数据
    """
    demo = FeatureReq()
    #压测数据生成demo
    text_file_list = sorted(os.listdir(input_dir)) #text_dir里边是文本列表，用于生成压测词表
    for text_file in text_file_list:
        data = {
                    "text": Util.read_file(input_dir + '/' + text_file) 
                }
        print demo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_FEED_VIDEO_TITLEDAMAGE_V1.py 
    生成压测数据：
        python FEATURE_FEED_VIDEO_TITLEDAMAGE_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/') #./text_dir/ 是本地的文本数据
    else:
        #特征计算Demo
        feature_calculate('./text_dir/text_file') #./text_dir/text_file 本地文本文件

