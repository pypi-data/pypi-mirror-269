#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_FEATURE_VIS_IMG_FEATURE_FRAME_GPU_ONLINE_V4 Demo, 以及压测数据生成的DEMO
Author: xieshuai(xieshuai@baidu.com)
Date: 2021-09-10
Filename: FEATURE_FEATURE_VIS_IMG_FEATURE_FRAME_GPU_ONLINE_V4.py
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os
import commands


class FeatureReq(XvisionDemo):
    """
    FEATURE_FEATURE_VIS_IMG_FEATURE_FRAME_GPU_ONLINE_V4 demo
    """

    def prepare_request(self, data, config_info):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps({
            "appid": "123456",
            "logid": random.randint(1000000, 100000000),
            "format": "json",
            "from": "xvision",
            "cmdid": "123",
            "clientip": "0.0.0.0",
            'auth_key': config_info['auth_key'],
            'business_name': config_info['business_name'],
            'feature_name': config_info['feature_name'],
            "data": base64.b64encode(json.dumps(data))
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
    calc_type = 1 + 2 + 4 + 16384
    data = {
        'logid': 'test_666',
        'format': 'json',
        'imagesnum': 1,
        'image_type':-1,
        'targetfacenum': 10,
        'scene_type': 100,
        'images': [
            {
                'calc_type': calc_type,
                #'live_map_type': 1,
                'imageid': "123",
                'image':base64.b64encode(Util.read_file(input_data["image"])),
                'infos':""
                #"face_type" : 1
            }
        ],
        "imagesnum": 1
    }
    input_data_1 = {
        'provider': 'get_feature',
        'input': json.dumps(data)
    }

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = "" # 算子名称
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        # 'resource_key': 'test.jpg',
        # 'auth_key': token,
        # 'business_name': job_name,
        # 'feature_name': 'FEATURE_VIS_IMG_FEATURE_FRAME_GPU_ONLINE_V3',
        # 'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    config_info = {
        'auth_key': token,
        'business_name': job_name,
        'feature_name': feature_name,
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    feature_data = featureDemo.prepare_request(input_data_1, config_info)


    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path

    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if featureDemo.xvision_test_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)


def gen_stress_data(input_data):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_data["image"]))  # image_dir里边是图片列表，用于生成压测词表
    for i in xrange(len(img_file_list)):
        data = {
            "image": base64.b64encode(Util.read_file(input_data["image"] + '/' + img_file_list[i])),
        }
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_FEATURE_VIS_IMG_FEATURE_FRAME_GPU_ONLINE_V4.py
    生成压测数据：
        python FEATURE_FEATURE_VIS_IMG_FEATURE_FRAME_GPU_ONLINE_V4.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        input_data = {
            "image": "./image_dir/FEATURE_AR_IMG_FACESKELETON_CPU_V1/img/"
        }
        gen_stress_data(input_data)  # ./image_dir/ 是本地的图片数据
    else:

        # 特征计算Demo
        input_data = {
            "image": "./image_dir/FEATURE_AR_IMG_FACESKELETON_CPU_V1/img/woman20.jpg"
        }
        feature_calculate(input_data)  # ./image_dir/img_file 本地图片
