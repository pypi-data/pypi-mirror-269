#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
"""
File: FEATURE_NLP_XUESHU_INDUSTRY_CLASSIFICATION.py
Author: wuyuwei(wuyuwei@baidu.com)
Date: 2022/10/13 2:38 下午
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import os


class FeatureReq(XvisionDemo):
    """
        FEATURE_NLP_XUESHU_INDUSTRY_CLASSIFICATION demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：string类型，待计算的文本
        输出：
            返回算子的输入数据
        """
        return json.dumps(data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:待分类的文本
    输出：
        分类结果
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    feature_data = feature_demo.prepare_request(input_data)
    job_name = ""  # 应用名
    token = ""  # token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NLP_XUESHU_INDUSTRY_CLASSIFICATION',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path
    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}
    # 请求百度视频中台特征计算服务
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    feature_demo.parse_result(res_data)


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待分类文本，每一行是一个JSON
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            print featureDemo.prepare_request(data)  # 压测文本内容数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NLP_XUESHU_INDUSTRY_CLASSIFICATION.py
    生成压测数据：
        python FEATURE_NLP_XUESHU_INDUSTRY_CLASSIFICATION.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        gen_stress_data('./text_dir/xvision_industry_classification_testcase.txt')
    else:
        # Demo
        with open('./text_dir/xvision_industry_classification_testcase.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                test_content = json.loads(line)
                break
        feature_calculate(test_content)