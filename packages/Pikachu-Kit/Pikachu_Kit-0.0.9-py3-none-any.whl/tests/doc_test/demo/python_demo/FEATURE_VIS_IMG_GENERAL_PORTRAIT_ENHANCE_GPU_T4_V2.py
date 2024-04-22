#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_GENERAL_PORTRAIT_ENHANCE_GPU_T4_V2 Demo, 以及压测数据生成的DEMO
Author: liufanglong(liufanglong@baidu.com)
Date: 2021-07-19
Filename: FEATURE_VIS_IMG_GENERAL_PORTRAIT_ENHANCE_GPU_T4_V2.py 
"""
from xvision_demo_enc import XvisionDemoEnc
from util import Util
import json
import base64
import random
import requests
import sys
import os
import bdes


class FeatureReq(XvisionDemoEnc):
    """
    FEATURE_VIS_IMG_GENERAL_PORTRAIT_ENHANCE_GPU_T4_V2 demo  
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        # type_name  string  请求类型：selfie2painting
        new_data = {
            "image": base64.b64encode(data['image']),
            "type_name": "general-portrait-enhance",
            "face_area_thresh": "0.007",
            "face_num_max": "5",
        }
        new_data, meta = bdes.encode(json.dumps(new_data))
        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'from': 'xvision',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(new_data),
        }), meta


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    with open(input_data, 'rb') as f:
        image_data = f.read()
    # 生成算子输入
    data = {
        "image": image_data
    }
    feature_data, meta = featureDemo.prepare_request(data)

    job_name = ""
    token = ""
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-VIS-ENCRYPT-METAINFO': meta,
        'X-VIS-DATA-ENCRYPTED': 'BDES_BINARY',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_GENERAL_PORTRAIT_ENHANCE_GPU_T4_V2',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))

    }
    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        url += '?business_name=%s&feature_name=%s' % (headers['business_name'], headers['feature_name'])

    # url = "http://10.187.122.17:2002"
    # 请求百度视频中台特征计算服务
    res_data = requests.post(url, feature_data, headers=headers)
    # 打印输出
    featureDemo.parse_result(res_data.text)


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
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            "image": Util.read_file(input_dir + '/' + image_file)
        }
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_GENERAL_PORTRAIT_ENHANCE_GPU_T4_V2.py 
    生成压测数据：
        python FEATURE_VIS_IMG_GENERAL_PORTRAIT_ENHANCE_GPU_T4_V2.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        # feature_calculate(
        #     '/ssd1/vis/lixin41/UGTIT/sketch/test_server/data/60BB1DD814CDC8ED66FEBA656.png')  # ./image_dir/img_file 本地图片
        feature_calculate('./image_dir/img_file')
