#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL Demo
Author: fumingxin(fumingxin@baidu.com)
Author update: shangzhizhou(shangzhizhou@baidu.com)
Date: 2020-05-11
Filename: FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL.py
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import sys
import random
import base64


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """

        logid = random.randint(1000000, 100000000)
        req_array = {
            'logid': logid,
            'req': {
                'video_url': data['video_url']
            },
        }
        return json.dumps(req_array)


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
    feature_data = featureDemo.prepare_request(input_data)

    # 生成百度视频中台输入
    callback_server_info = {
        # "bns"                 : "bns_name_example",           # 可选，BNS 与host 两个必须指定一个，同时指定时优先使用BNS
        # "port_name"           : "port_name",                  # 可选，与bns一起使用，指定BNS 的端口名称，如果端口名非默认名称时需要指定
        "host": "nj03-m22-feed-backup-pool-0967.nj03.baidu.com",
        "port": 8080,
        "path": "/xvision/post"  # 异步回调路径
    }

    job_name = ''
    token = ''

    xvision_data = {
        'business_name': job_name,  # job_name
        'resource_key': 'test.jpg',  # passthrough data
        'auth_key': token,  # token
        'feature_name': 'FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL_ASYN',  # 算子名
        'data': base64.b64encode(feature_data),
        "callback": json.dumps(callback_server_info)  # 可选，默认为提交作业时提交的回调信息, 优先使用这里的指定参数
    }

    # 异步访问
    url = featureDemo.xvision_online_url + featureDemo.xvision_callback_path
    params = {
        "business_name": xvision_data["business_name"],
        "feature_name": xvision_data["feature_name"]
    }

    # 请求百度视频中台特征计算服务
    res_data = featureDemo.request_feat(params, xvision_data, url)
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
    # 压测数据生成demo
    video_info_list = Util.read_video_file('./video_dir/video_data.txt')
    for video_info in video_info_list:
        data = {
            'video_url': video_info['video_url'],
        }
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL.py
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        video_url = 'http://10.63.65.21:8346/file/a541189c743b3c06c44a1dbf46f171a0/file_name/mda-jmgvqt3p5itd4a1i.mp4'
        feature_calculate({'video_url': video_url})
