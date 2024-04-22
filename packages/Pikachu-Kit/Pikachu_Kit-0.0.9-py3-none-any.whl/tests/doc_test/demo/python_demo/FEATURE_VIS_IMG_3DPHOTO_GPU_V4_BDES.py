#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_IMG_3DPHOTO_GPU_V4_BDES Demo, 以及压测数据生成的DEMO
Author: yuanweihang(yuanweihang@baidu.com)
Date: 2022-11-09
Filename: FEATURE_VIS_IMG_3DPHOTO_GPU_V4_BDES.py
"""
from xvision_demo import XvisionDemo
from util import Util
import random
import base64
import urllib
import sys
import os
import json
import requests

bdes_host = ''

def bdes_encode(data, binary=1):
    """
    功能: 加密
    输入: 任意文件
    输出: 加密后的文件
    """
    #def encode(data, binary=0):
    url = bdes_host + '/bdes/encode?binary=' + ('1' if binary else '0')
    res = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    return res.content, res.headers['X-MIPS-BDES-META']

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_3DPHOTO_GPU_V4_BDES demo
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
            'image': base64.b64encode(data['image_url']),
            'type_name': 'inpainting3d',
            'traj_type': 0, #[0,1,2,3,4,5,6]
            'strength': 1.0, # 0.5~1.5
            'duration': 3
        }
        req_data, meta = bdes_encode(json.dumps(req_data))
        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'from': 'xvision',
                    'cmdid': '123',
                    'format': 'json',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(req_data),
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
    #生成算子输入
    data = {
        "image_url": input_data
    }
    feature_data, meta = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_3DPHOTO_GPU_V4_BDES',
        'X_BD_LOGID': str(random.randint(1000000, 100000000)),
        'X-VIS-ENCRYPT-METAINFO': meta,
        'X-VIS-DATA-ENCRYPTED': 'BDES_BINARY'
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
    result = json.loads(res_data)
    result_str = result['feature_result']['value'] #['result']
    result = json.loads(result_str) 
    print(result['err_no'])
    result = result['result'] #['value']['result']
    result = json.loads(result)   
    video_url = base64.b64decode(result['video_url'])
    print(video_url)

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_dir:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    data = {
        "image_url": input_dir
    }
    print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_3DPHOTO_GPU_V4_BDES.py
    生成压测数据：
        python FEATURE_VIS_IMG_3DPHOTO_GPU_V4_BDES.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('http://10.153.117.33:8999/1.png') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('http://10.153.117.33:8999/1.png') # 任意图片utl地址