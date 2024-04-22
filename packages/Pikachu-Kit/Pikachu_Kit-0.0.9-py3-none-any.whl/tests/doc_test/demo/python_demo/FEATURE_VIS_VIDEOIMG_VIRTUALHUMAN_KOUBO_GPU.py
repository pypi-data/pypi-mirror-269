#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_KOUBO_GPU Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2021-05-18
Filename: FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_KOUBO_GPU.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os
import uuid
import time
import requests

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_KOUBO_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        request_data = {
            "action": "koubo", # merge 动作，固定值
            "task_id": str(uuid.uuid4()), # 业务唯一ID，自定义，回调会传递回
            "req_image_id": data.get("req_image_id"),
            "req_audio_id": data.get("req_audio_id"),
            "image_landmark": data.get("image_landmark"), # 图片150关键点
        }
        return json.dumps(request_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: {'req_audio_id': '', 'req_image_id': ''}
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)

    # 灵视callback人物创建地址
    # url = 'http://group.xvision-callbackmanager.xvision.all.serv:8090/xvision/v1/add_task'
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = 'FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_KOUBO_GPU'

    url = featureDemo.xvision_online_url + featureDemo.xvision_callback_path
    params = {
        "business_name": job_name,
        "feature_name": feature_name,
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X_BD_LOGID': str(random.randint(1000000, 100000000)),
    }
    data = {
        "business_name": job_name,
        "resource_key": 'test',
        "auth_key": token,
        "feature_name": feature_name,
        "data": base64.b64encode(feature_data),
        # callback 信息，可选参数
        'callback': json.dumps({
            "path": "/face-api/virtualhuman/task/callback",
            "host": "yq01-sys-hic-k8s-k40-qm-0019.yq01.baidu.com",
            "port": 8090,
        })
    }

    res_data = featureDemo.request_feat_new(params, json.dumps(data), url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)


def gen_stress_data(audio_input_file, image_input_file):
    """
    功能：生成压测数据
    输入：
        audio_input_file: 音频url文件
        image_input_file: 图片url文件
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(audio_input_file, 'r') as fp:
        audio_urls = fp.readlines()
    with open(image_input_file, 'r') as fp:
        image_urls = fp.readlines()
    for audio_url in audio_urls:
        for image_url in image_urls:
            data = {
                'req_image_id': image_url.strip(),
                'req_audio_id': audio_url.strip(),
                'image_landmark': "", # 需要获取图片的150关键点
            }
            print featureDemo.prepare_request(data)#压测数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_KOUBO_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_KOUBO_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        # audio.txt: 音频url列表文件
        # image.txt: 图片url列表文件
        gen_stress_data('./video_url_dir/FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU/audio.txt',
                        './video_url_dir/FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU/image.txt')
    else:
        # 合成视频
        feature_calculate({
            "req_image_id": "http://facefusion-2021-peoplesdaily.bj.bcebos.com\
            /image/16521605961282_cf97c8e6d4ec32ad30542c13b91a1e66",
            "req_audio_id": "http://facefusion-2021-peoplesdaily.bj.bcebos.com/\
            wav/16521605963056_aac811ede6b2737073371c3578366781.wav",
            "image_landmark": """
                202.73 277.82
                214.1 311.84
                229.46 344.88
                249.83 377
                283.04 404.46
                321.85 423.25
                357.49 423.46
                387.69 402.07
                409.94 363.1
                419.22 328.53
                422.11 294.41
                423.43 260.24
                421.14 226.33
                244.81 261.11
                253.47 249.58
                265.49 243.84
                279.07 245
                291.23 254.81
                281.04 259.38
                268.69 263.16
                255.61 263.66
                267.8 252.55
                221.4 236.72
                234.9 218.73
                253.29 212.58
                271.9 211.64
                290.87 220.21
                272.74 222.83
                254.56 224.13
                237.3 228.36
                344.12 242.75
                350.62 228.22
                362.04 221.32
                375.17 221.02
                387.34 227.59
                379.71 234.75
                368.13 240.13
                355.4 242.02
                362.25 230.65
                333.53 211.68
                346.31 196.54
                361.88 189.85
                379.52 186.5
                397.48 196.47
                381.5 196.1
                365.38 200.34
                349.87 206.39
                304.88 252.92
                306.65 276.15
                308.43 299.4
                307.19 324
                320.42 320.54
                345.88 314.79
                357.15 311.9
                347.2 291.24
                339.2 269.06
                331.31 246.91
                331.09 305.17
                303.85 367.52
                320.11 354.67
                339.47 348.78
                358.19 344.95
                376.37 348.65
                365.98 367.6
                347.24 378.89
                324.1 378.88
                323.08 362.14
                341.59 358.34
                359.01 353.35
                359.71 357.67
                343.26 363.65
                324.7 366.99
                208.65 294.8
                221.75 328.45
                239.11 361.79
                265.7 391.83
                301.98 414.94
                339.4 425.62
                374.51 415.02
                399.59 382.97
                415.3 345.89
                420.95 311.57
                422.84 277.33
                422.37 243.33
                220.92 232.94
                289.92 214.56
                331.71 206.11
                396.64 192.91
                248.28 254.88
                258.78 245.85
                272.43 243.3
                285.77 248.85
                285.99 256.94
                274.98 261.72
                262.13 264.09
                250.38 262.45
                257.62 255.54
                278.34 251.4
                346.19 234.94
                355.47 223.94
                368.6 220.05
                381.75 223.28
                383.27 231.32
                374.18 238.03
                361.76 241.55
                349.67 242.14
                352.74 234.08
                372.98 228.89
                318.31 249.95
                323.4 272.43
                328.6 295.11
                317.6 329.65
                317.99 315.01
                345.56 308.75
                351.35 321.2
                335.07 326.11
                306.54 367.19
                373.88 349.69
                308.53 362.79
                313.85 358.46
                325.98 350.75
                332.34 348.97
                345.65 345.61
                351.62 344.13
                364.69 345.31
                370.59 346.64
                373.67 355.47
                370.59 361.98
                361.1 373.18
                354.92 377.07
                339.45 381.35
                331.58 381.25
                316.52 376.52
                310.02 372.42
                310.32 365.47
                316.38 363.74
                329.41 360.23
                335.36 359.05
                347.46 355.98
                352.96 354.3
                364.77 351.46
                370.11 349.97
                370.88 352.35
                365.56 354.88
                354.2 359.67
                348.96 361.49
                336.91 364.77
                331.04 365.84
                317.57 367.56
                311.04 368.07
            """
        })

