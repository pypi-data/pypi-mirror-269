#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_IMG_IMAGECAPTION_GPU_ASYNC_A30 Demo, 以及压测数据生成的DEMO
Author: wanghui48(wanghui48@baidu.com)
Date: 2024-3-15
Filename: FEATURE_IMG_IMAGECAPTION_GPU_ASYNC_A30.py 
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
    FEATURE_IMG_IMAGECAPTION_GPU_ASYNC_A30 demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        imagedata = open("123.jpg", 'rb').read()
        protodata = base64.b64encode(imagedata)
        request_data = {
            "appid": "2312313",
            "logid": "demo",
            "image": str(protodata, encoding='utf8'),
            "session_id": "whtestpred3",
            "prompt": "",
            "history":[[""]],
            "skip_ocr": False
        }
        return json.dumps(request_data)


def feature_calculate(input_data):
    """
    功能：图生文
    输入：
        input_data
    输出：
        图片链接
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)

    # 灵视callback任务创建地址
    # url = 'http://group.xvision-callbackmanager.xvision.all.serv:8090/xvision/v1/add_task'
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = 'FEATURE_IMG_IMAGECAPTION_GPU_ASYNC_A30'

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
        # callback 信息
        'callback': json.dumps({
            "path": "",
            "host": "",
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
    


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_IMG_IMAGECAPTION_GPU_ASYNC_A30.py 
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    feature_calculate({})

