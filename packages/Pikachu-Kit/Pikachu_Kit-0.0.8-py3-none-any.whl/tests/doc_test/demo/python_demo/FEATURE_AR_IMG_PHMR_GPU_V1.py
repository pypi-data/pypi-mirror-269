#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_AR_IMG_PHMR_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: cuixiankun01(cuixiankun01@baidu.com)
Date: 2022-11-28
Filename: FEATURE_AR_IMG_PHMR_GPU_V1.py
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
    FEATURE_AR_IMG_PHMR_GPU_V1 demo
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
                "front_image": str(base64.b64encode(data["front_image"]), "utf-8"),
                "side_image": str(base64.b64encode(data["side_image"]), "utf-8"),
                'user_height': data["user_height"],
                'gender': data["gender"]
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
        "front_image": Util.read_file(input_data["front_image"]),
        "side_image": Util.read_file(input_data["side_image"]),
        'user_height': input_data["user_height"],
        'gender': input_data["gender"]
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
        'feature_name': 'FEATURE_AR_IMG_PHMR_GPU_V1',
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
    # print(res)
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
    for file_name in os.listdir(input_dir['image']):
        if file_name.find('side') < 0:
            continue

        gender = file_name.strip().split('_')[0]
        # key_name = '_'.join(file_name.strip().split('_')[:-1])
        front_img_pth = os.path.join(input_dir['image'], file_name.replace('side', 'front'))
        side_img_pth = os.path.join(input_dir['image'], file_name)

        data = {
            #"image": str(encoded_image, encoding='utf-8'),
            "front_image": Util.read_file(front_img_pth),
            "side_image": Util.read_file(side_img_pth),
            'user_height': 1.60,
            'gender': gender
        }

    # print featureDemo.prepare_request(data)  # 压测词表数据


   

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_AR_IMG_PHMR_GPU_V1.py
    生成压测数据：
        python FEATURE_AR_IMG_PHMR_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        input_data = {
            'image': './image_dir/FEATURE_AR_IMG_PHMR_GPU_V1/image'  # 图片目录
        }
        gen_stress_data(input_data)
    else:
        # 特征计算Demo
        input_data = {
            'front_image': './image_dir/FEATURE_AR_IMG_PHMR_GPU_V1/image/male_0017_front.jpg',
            'side_image': './image_dir/FEATURE_AR_IMG_PHMR_GPU_V1/image/male_0017_side.jpg',
            'user_height': 1.60,
            'gender': 'male'
        }
        feature_calculate(input_data)  # 本地图片与参数配置
