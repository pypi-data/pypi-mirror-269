#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4 Demo, 以及压测数据生成的DEMO
Author: yanjianfeng01(yanjianfeng01@baidu.com)
Date: 2023-08-29
Filename: FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4.py
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
import numpy as np
class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4 demo
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
            "appid": "xvision_job_name", #填写视频中台的作业名，方便排查问题
            "logid": random.randint(1000000, 100000000),
            "format": "json",
            "from": "xvision",
            "cmdid": "123",
            "clientip": commands.getoutput("hostname"), #请求ip，用户发送请求的ip地址，方便排查问题
            "data": data
        }
        return json.dumps(req_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    demo = FeatureReq()

    input_json = {
            "object_type":"faceswap_picture",
            "first_image":base64.b64encode(open(input_data['first_name'],'r').read()),
            "second_image":base64.b64encode(open(input_data['second_name'] ,'r').read()), #ase64.b64encode(imgfile.read()),
            "source_image":base64.b64encode(open(input_data['source_name'],'r').read()), #base64.b64encode(imgfile.read()),
            "first_lmks":' '.join([str(r) for r in np.load(input_data['first_lmk_name']).flatten().tolist()]),
            "second_lmks":' '.join([str(r) for r in np.load(input_data['first_lmk_name']).flatten().tolist()]),
            "source_lmks":' '.join([str(r) for r in np.load(input_data['source_lmk_name']).flatten().tolist()]),
    }

    #生成算子输入
    feature_data = demo.prepare_request(json.dumps(input_json))

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        # 'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 灵视参数报装
    request_data = json.dumps({
        'resource_key': '',
        'auth_key': token,
        'data': base64.b64encode(feature_data),
    })

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = demo.xvision_online_url + demo.xvision_sync_path

    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    params = {
        "business_name": job_name,
        "feature_name": "FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4"
    }

    res_data = demo.request_feat_new(params, request_data, url, headers)
    # 打印输出
    demo.parse_result(res_data)


def gen_stress_data(input_datas):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    demo = FeatureReq()
    #压测数据生成demo

    #image_dir里边是图片列表，用于生成压测词表
    for input_data in input_datas:
        input_json = {
            "object_type":"faceswap_picture",
            "first_image":base64.b64encode(open(input_data['first_name'],'r').read()),
            "second_image":base64.b64encode(open(input_data['second_name'] ,'r').read()), #ase64.b64encode(imgfile.read()),
            "source_image":base64.b64encode(open(source_name,'r').read()), #base64.b64encode(imgfile.read()),
            "first_lmks":' '.join([str(r) for r in np.load(input_data['first_lmk_name']).flatten().tolist()]),
            "second_lmks":' '.join([str(r) for r in np.load(input_data['first_lmk_name']).flatten().tolist()]),
            "source_lmks":' '.join([str(r) for r in np.load(input_data['source_lmk_name']).flatten().tolist()]),
        }

        #生成算子输入
        feature_data = demo.prepare_request(json.dumps(input_json))


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4.py
    生成压测数据：
        python FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    input_data = {

    'first_name': './image_dir/FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4/0000000001.jpg',
    'second_name': './image_dir/FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4/0000000125.jpg',
    'source_name':'./image_dir/FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4/source.jpg',
    'first_lmk_name':'./image_dir/FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4/0000000001_lmk72.npy',
    'source_lmk_name':'./image_dir/FEATURE_VIS_IMG_EMOTIONDRIVER_GPU_YIKE_T4/source_lmk72.npy'
    }

    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data([input_data]) #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate(input_data) #./image_dir/img_file 本地图片
