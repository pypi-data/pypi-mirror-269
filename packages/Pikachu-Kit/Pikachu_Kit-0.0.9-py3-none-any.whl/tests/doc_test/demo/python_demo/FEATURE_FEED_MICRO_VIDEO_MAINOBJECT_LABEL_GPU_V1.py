#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_FEED_MICRO_VIDEO_MAINOBJECT_LABEL_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: xiaoyunfeng(xiaoyunfeng@baidu.com)
Date: 2019-09-16
Filename: FEATURE_FEED_MICRO_VIDEO_MAINOBJECT_LABEL_GPU_V1.py
"""
import base64
import json
import os
import random
import sys
import urllib
import commands

from util import Util
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_FEED_MICRO_VIDEO_MAINOBJECT_LABEL_GPU_V1 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_data = {
            "svc_name": "mainobject_detect",
            'image': data['image'],
            'image_url': data['image_url'],
            'video_url': data['video_url'],
            'feat_args': data['feat_args'],
        }

        return urllib.urlencode(req_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    # 生成算子输入
    data = {
        "image" : "",
        "image_url" : input_data['image_url'],
        "video_url" : input_data['video_url'],
        "feat_args" : "{\"source_type\": \"image\"}"
    }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_FEED_MICRO_VIDEO_MAINOBJECT_LABEL_GPU_V1',
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
        input_dir : （视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    video_image_info_list = Util.read_video_image_file(input_dir)
    for video_image_info in video_image_info_list:
        data = {
            "image":"",
            "image_url" : video_image_info['image_url'],
            "video_url" : video_image_info['video_url'],
            "feat_args" : "{\"source_type\": \"image\"}"
        }
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_FEED_MICRO_VIDEO_MAINOBJECT_LABEL_GPU_V1.py
    生成压测数据：
        python FEATURE_FEED_MICRO_VIDEO_MAINOBJECT_LABEL_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./video_dir/video_data.txt')
    else:
        # 特征计算Demo
        video_image_list = Util.read_video_image_file('./video_dir/video_data.txt')
        feature_calculate(video_image_list[0])
