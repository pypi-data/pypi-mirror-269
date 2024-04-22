#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_NEW_GPU Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2021-04-07
Filename: FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_NEW_GPU.py 
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
    FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_NEW_GPU demo  
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
            "action": "merge",  # 固定值
            "task_id": str(uuid.uuid4()),
            "track_url": "https://facefusion-2021-peoplesdaily.cdn.bcebos.com/track/\
            53d23a2e-97c9-4531-8135-6cb307b19d43_new_v1.tar.gz", # 模型人物包
            "req_image_id": data.get('req_image_id'),
            "req_audio_id": data.get('req_audio_id'),
            "alpha": 1,
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
    feature_name = ''

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
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_NEW_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_NEW_GPU.py GEN_STRESS_DATA
    """
    # op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    # if op_type == 'GEN_STRESS_DATA':
    #     # 生成压测数据
    #     # audio.txt: 音频url列表文件
    #     # image.txt: 图片url列表文件
    #     gen_stress_data('./video_url_dir/FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU/audio.txt',
    #                     './video_url_dir/FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU/image.txt')
    # else:
     # 合成视频
    feature_calculate({
        'req_audio_id': 'http://bj.bcebos.com/bjh-pixel/aigc-nlp-vidpress/1/tts_merge_4d479d8c73.wav',
        'req_image_id': 'https://facefusion-2021-peoplesdaily.bj.bcebos.com/virtualhuman/image/1280*720.png',
    })

