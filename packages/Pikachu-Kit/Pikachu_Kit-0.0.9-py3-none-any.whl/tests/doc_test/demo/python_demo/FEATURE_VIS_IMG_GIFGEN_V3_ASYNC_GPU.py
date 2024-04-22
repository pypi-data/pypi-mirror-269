#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU Demo, 以及压测数据生成的DEMO
Author: wuye03(wuye03@baidu.com)
Date: 2023-05-31
Filename: FEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU.py
Note: before you  execute "python2 FEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU.py", you need execute "python3 callback.py" to launch a local server to receive the return json. As for "callback.py",please contact wuye03
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os
#import bdes
import bdes_2023
import requests



class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU demo  
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        # upload_url: 上传视频到poms时使用的上传地址
        new_data = {
            "image": base64.b64encode(data['image']).decode('utf-8'),
            "text_prompt": data['text_prompt'],
        }
        
        new_data = json.dumps(new_data).encode("utf-8")
        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(new_data).decode(),
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
    with open(input_data, 'rb') as f:
        image_data = f.read()
    # 生成算子输入
    params = {
        "image": base64.b64encode(image_data).decode("utf-8"),
    }
    

    callback = {
        "host": "10.255.106.17", # 填写测试机器（接收服务返回结果的机器）的ip,请注意一定要写对ip,否则无法接收返回的结果。
        "port": 8200, # 任意一个没有占用的端口
        "path": "/",
        "retry_times": 3,
    }

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = "FEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU"
    data = {
        'business_name': job_name,
        'resource_key': 'test',
        'auth_key': token,
        'feature_name': feature_name,
        "callback": json.dumps(callback),
        'data': base64.b64encode(json.dumps(params).encode('utf-8')).decode(),
    }

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = "http://xvision-api.sdns.baidu.com/xvision/xvision_callback?business_name=%s&feature_name=%s" \
        % (job_name, feature_name)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())


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
        if not (image_file.endswith(".jpg") or image_file.endswith(".png")):
            continue
        with open(os.path.join(input_dir, image_file), 'rb') as f:
            image_data = f.read()
        data = {
            "image": image_data,
            "text_prompt": "an image"
        }
        print (featureDemo.prepare_request(data))  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU.py
    生成压测数据：
        python FFEATURE_VIS_IMG_GIFGEN_V3_ASYNC_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/666.png')  # ./image_dir/img_file 本地图片
