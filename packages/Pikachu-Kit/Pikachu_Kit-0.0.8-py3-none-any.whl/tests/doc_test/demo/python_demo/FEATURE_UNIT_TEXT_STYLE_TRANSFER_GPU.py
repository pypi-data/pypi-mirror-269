#!/usr/bin/env python
# coding=utf-8
"""
Author: gaoyangfan@baidu.com
since: 2022-06-20 21:15:09
LastTime: 2022-06-20 21:33:43
LastAuthor: gaoyangfan@baidu.com
message: FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU Demo, 以及压测数据生成的DEMO
Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import random
import sys
import os
import base64

class FeatureReq(XvisionDemo):
    """
    FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据

        Args:
            data (dict): 包含输入文本和待转换风格, key is (text, style), style is optional

        Returns:
            [str]: 返回算子的输入数据
        """
        return json.dumps(data)


def feature_calculate(input_data):
    """
    功能：特征计算

    Args:
        input_data (dict): 包含输入文本和待转换风格, key is (text, style), style is optional
    Returns:
        风格转换后的结果
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    feature_data = feature_demo.prepare_request(input_data)

    job_name = ""  # 应用名
    token = ""  # token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': '',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path
    # url = feature_demo.xvision_test_url + feature_demo.xvision_sync_path

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

    res_data = json.loads(res_data)
    res_data['feature_result']['value'] = json.loads(res_data['feature_result']['value'])
    return res_data


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待链指的文本，json 形式的 dict, key 是 text 和 style(可选)，每一行是一个json字符串
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            line = json.loads(line.strip())
            print(featureDemo.prepare_request(line))


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU.py
    生成压测数据：
        python FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./text_dir/dialog_style_transfer_test_data')  # 本地的测试数据
    else:
        # 风格转换Demo
        feature_calculate({'text': '这是风格转换服务', 'style': 0})
