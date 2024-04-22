#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Filename: FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN.py
# Description:
# @Author: yaomingliang@baidu.com
# Created on 2021/10/12 14:38
# Copyright (c) 2021, Baidu.com All Rights Reserved
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
    FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        Args:
            data (dict):输入数据
        Returns:
            [str]: 返回算子的输入数据
        """
        return json.dumps({
            "value": [base64.b64encode(data['image'])], 
            "key":["image"]
            })


def feature_calculate(input_data):
    """
    功能：特征计算
    Args:
        input_data: 本地图片文件
    输出：
        实体链指结果
    """
    feature_demo = FeatureReq()
    #生成算子输入
    data = {
                "image": Util.read_file(input_data)
            }
    feature_data = feature_demo.prepare_request(data)
    job_name = ""  # 应用名
    token = ""  # token
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_test_url + feature_demo.xvision_sync_path
    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    feature_demo.parse_result(res_data)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data: 图片
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    for _, _, files in os.walk(input_dir):
        for image_file in files:
            data = {
                    "image": Util.read_file(input_dir + '/' + image_file) 
                }
            print featureDemo.prepare_request(data) # 压测词表数据



if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN.py
    生成压测数据：
        python FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN/')
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/FEATURE_NETDISK_IMG_LOGODETECT_GPU_WANGPAN/bbc.jpg') # 本地图片
