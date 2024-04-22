#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_HIGHLIGHT_GPU_V2 Demo, 以及压测数据生成的DEMO
Author: wanghua11(wanghua11@baidu.com)
Date: 2019-07-29
Filename: FEATURE_VIS_VIDEO_HIGHLIGHT_GPU_V2.py 
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
    FEATURE_VIS_VIDEO_HIGHLIGHT_GPU_V2 demo  
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
                "sk": "514",
                "object_prefix": "",
                "image_num": 3,
                "video_url": data['video_url'],
                "endpoint": "http://su.bcebos.com",
                "duration": 6,
                "ak": "07",
                "clip_num": 3,
                "bucket": "test-bucket4"
        } 
        return json.dumps({
                    'appid': 'xvision_job_name',
                    'logid': random.randint(1000000, 100000000),
                    'from': 'xvision',
                    'clientip': commands.getoutput("hostname"),
                    'data': base64.b64encode(json.dumps(req_data)),
                })


def feature_calculate():
    """
    功能：特征计算
    输入：
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
            "video_url": "http://cp01-rdqa-dev003-lifu.epc.baidu.com:8011/ps_classify/video/mda-hcfeihgfvunf0wia.mp4"
            }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_VIDEO_HIGHLIGHT_GPU_V2',
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
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_dir, 'r') as fp:
        video_file_list = fp.readlines()
    for video_url in video_file_list:
        data = {
                    "video_url":  video_url.rstrip('\n') 
                }
        print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_HIGHLIGHT_GPU_V2.py 
    生成压测数据：
        python FEATURE_VIS_VIDEO_HIGHLIGHT_GPU_V2.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./video_url_dir/url_file') #./video_url_dir/url_file 是本地的视频列表，一行一个
    else:
        #特征计算Demo
        feature_calculate() 
