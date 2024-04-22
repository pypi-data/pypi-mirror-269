#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_LIPOPTIMIZE_KOL_GPU Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2021-12-26
Filename: FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_LIPOPTIMIZE_KOL_GPU.py 
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
    FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_LIPOPTIMIZE_KOL_GPU demo  
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
            "action": "lipkol",  # 固定值
            "task_id": str(uuid.uuid4()), # 任务ID，建议唯一，字符串
            "track_url": data.get('track_url'), # 代表形象
            "req_audio_id": data.get('req_audio_id'), # 用户音频地址
        }
        return json.dumps(request_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: {'track_url': '', 'req_audio_id': ''}
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)

    # 灵视callback人物创建地址
    # url = 'http://group.xvision-callbackmanager.xvision.all.serv:8090/xvision/v1/add_task'
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = 'FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_LIPOPTIMIZE_KOL_GPU'

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
            }
            print featureDemo.prepare_request(data)#压测数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_LIPOPTIMIZE_KOL_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_LIPOPTIMIZE_KOL_GPU.py GEN_STRESS_DATA
    """
    feature_calculate({
        "track_url": "http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz10.tar.gz",
        # 支持如下形象包
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz10.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz11.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz13.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz14.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz15.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz16.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz7.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz8.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnxz9.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnzsz1.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnzsz2.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnzsz3.tar.gz
        # http://facefusion-2021-peoplesdaily.bj.bcebos.com/track/people_kolsmnzsz4.tar.gz
        "req_audio_id": "http://ar-material.bj.bcebos.com/upload/ttv/tts_4100_1.wav",
    })
        

