#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_KOUBO_CLASS_GPU_V1 Demo
Filename: FEATURE_VIS_KOUBO_CLASS_GPU_V1.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import os


class FeatureVisKouboClassGPUV1(XvisionDemo):
    """
    FEATURE_VIS_KOUBO_CLASS_GPU_V1 Demo
    """

    def prepare_request(self, data):
        """
        功能: 构建算子的输入数据
        输入:
            data: dict 类型, 算子处理对象包含
                  video_url(可以是视频文件或者直播流的地址)
        输出:
            返回算子的输入数据
        """
        req_data = {
            'appid': '123456',
            'logid': 1,
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(data),
        }
        return json.dumps(req_data)


def feature_calculate():
    """
    功能: 特征计算
    输入:
        input_url: 视频文件或者直播流的url
        url_type："file" 或者 "stream"
    输出:
        视频抖动得分
    """
    input_url = 'http://yq01-gpu-158-18-00.epc.baidu.com:8900/' \
                'workspace/project/ActionRecognition/data/data/VID_20190404_213159_4.mp4'
    featureDemo = FeatureVisKouboClassGPUV1()
    # 生成算子输入
    data = {
        'video_url': input_url
    }
    data = json.dumps(data)
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_KOUBO_CLASS_GPU_V1',
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


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureVisKouboClassGPUV1()
    f = open('stress_data', 'a')
    # 压测数据生成demo
    with open(input_file, 'r') as fin:
        video_url_file = fin.readlines()
    for video_url in video_url_file:
        data = {
            "video_url": video_url.rstrip('\n'),
        }
        data = json.dumps(data)
        f.write(featureDemo.prepare_request(data))  # 压测词表数据
        f.write('\n')


if __name__ == '__main__':
    """
    main
    特征计算执行:
        python FEATURE_VIS_KOUBO_CLASS_GPU_V1.py
    生成压测数据：
        python FEATURE_VIS_KOUBO_CLASS_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./video_url_dir/url.txt')  # ./video_url_dir/url.txt 是视频url文件
    else:
        # 特征计算Demo
        feature_calculate()
