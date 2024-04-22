#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_AR_IMG_FB_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: liudongdong04(liudongdong04@baidu.com)
Date: 2021-01-21
Filename: FEATURE_AR_IMG_FB_GPU_V1.py
"""
import os

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys


class FeatureReq(XvisionDemo):
    """
    FEATURE_AR_IMG_FB_GPU_V1 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps(
            {
                'image': base64.b64encode(data['image']),
                'property': json.loads(data['param'])
            })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    # 生成算子输入
    data = {
        "image": Util.read_file(input_data['image']),
        "image_quality": 80,
        "param": Util.read_file(input_data['param'])
    }

    feature_data = featureDemo.prepare_request(data)

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path

    job_name = ''
    token = ''
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_AR_IMG_FB_GPU_V1',
        'logid': str(random.randint(1000000, 100000000)),
    }

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    featureDemo.parse_result(res)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    param_file_list = sorted(os.listdir(input_dir['param']))
    img_file_list = sorted(os.listdir(input_dir['image']))  # image_dir里边是图片列表，用于生成压测词表
    for image_file, param_file in zip(img_file_list, param_file_list):
        data = {
            "image": Util.read_file(input_dir['image'] + '/' + image_file),
            "param": Util.read_file(input_dir['param'] + '/' + param_file)
        }
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_AR_IMG_FB_GPU_V1.py
    生成压测数据：
        python FEATURE_AR_IMG_FB_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        input_data = {
            'param': './image_dir/FEATURE_AR_IMG_FB_GPU_V1/param',  # 参数配置目录
            'image': './image_dir/FEATURE_AR_IMG_FB_GPU_V1/image'  # 图片目录
        }
        gen_stress_data(input_data)
    else:
        # 特征计算Demo
        input_data = {
            'param': './image_dir/FEATURE_AR_IMG_FB_GPU_V1/param/beautify.json',
            'image': './image_dir/FEATURE_AR_IMG_FB_GPU_V1/image/boy.jpg'
        }
        feature_calculate(input_data)  # 本地图片与参数配置
