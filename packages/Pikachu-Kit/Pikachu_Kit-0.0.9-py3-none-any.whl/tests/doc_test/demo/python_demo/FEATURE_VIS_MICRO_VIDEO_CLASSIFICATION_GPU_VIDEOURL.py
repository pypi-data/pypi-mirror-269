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
import base64
import urllib
import sys
import os
import random
import commands

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
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL',
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
    video_info_list = Util.read_video_file('./video_dir/video_data.txt')
    for video_info in video_info_list:
        data = {
                    'video_url': video_info['video_url'],
                }
        print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_MICRO_VIDEO_CLASSIFICATION_GPU_VIDEOURL.py
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        video_url = 'http://10.63.65.21:8346/file/a541189c743b3c06c44a1dbf46f171a0/file_name/mda-jmgvqt3p5itd4a1i.mp4'
        feature_calculate({'video_url': video_url})
