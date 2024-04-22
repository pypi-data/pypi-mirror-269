#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_THUMBNAIL_V1_ASYN Demo, 以及压测数据生成的DEMO
Author: lifu(lifu@baidu.com)
Date: 2020-06-10
Filename: FEATURE_VIS_VIDEO_THUMBNAIL_V1_ASYN.py
"""
import base64
import json
import random
import sys
import commands
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_THUMBNAIL_V1_ASYN demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps({
            'appid': 'xvision_job_name',
            'logid': random.randint(1000000, 100000000),
            'from': 'xvision',
            'clientip': commands.getoutput("hostname"),
            'data': base64.b64encode(json.dumps({"video_url": data['video_url'], "number": 1}))
        })


def feature_calculate():
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
        "video_url": "http://yq01-gpu-88-149-14-00.epc.baidu.com:8080/video_preview/video/mda-he19rj841js9hr46.mp4"
    }
    feature_data = featureDemo.prepare_request(data)

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
        'feature_name': 'FEATURE_VIS_VIDEO_THUMBNAIL_V1_ASYN',  # 算子名
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
    f = open('stress_data', 'a')
    # 压测数据生成demo
    with open(input_dir, 'r') as f:
        video_url_file = f.readlines()
    for video_url in video_url_file:
        data = {
            "video_url": video_url.rstrip('\n')
        }
        f.write(featureDemo.prepare_request(data))  # 压测词表数据
        f.write('\n')


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_THUMBNAIL_V1_ASYN.py
    生成压测数据：
        python FEATURE_VIS_VIDEO_THUMBNAIL_V1_ASYN.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./video_url_dir/url.txt')  # ./video_url_dir/url_file 是视频url文件
    else:
        # 特征计算Demo
        feature_calculate()
