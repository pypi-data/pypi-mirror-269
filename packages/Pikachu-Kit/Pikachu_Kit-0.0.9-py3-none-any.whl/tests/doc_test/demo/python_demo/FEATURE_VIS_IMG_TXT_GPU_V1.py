#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2021-04-07
Filename: FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU.py 
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
    FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        imgfile = data.get('imgfile')
        text = data.get('text')
        img = Util.read_file(imgfile)
        args = []
        args.append({
            'type': 'query',
            'type_value': text,
            'type_probs': 1.0,
        })
        stream = {
            'frame_id': 0,
            'stream_ts': int(round(time.time() * 1000)),
            'image_str': base64.b64encode(img),
            'args': args,
        }
        apply = {
            'has_human_body': False,
            'has_human_face': False,
            'has_vehicle': False,
            'need_track': False
        }
        data = {
            'stream': stream,
            'apply': apply
        }
        req_data = {
            'appid': '1234567',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(json.dumps(data))
        }
        # return json.dumps(req_data)
        return json.dumps(data)

def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: {'imgfile': '', 'text': ''}
    输出：
        相似度
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)

    # 灵视callback人物创建地址
    job_name = ""  # 申请的作业名 压测作业名
    token = ""  # 作业的token
    feature_name = ''
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_TXT_GPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path
    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}
    # url = 'http://10.227.112.141:2000//StreamService/stream_with_apply'
    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)

def gen_stress_data(input_data):
    """
    功能：生成压测数据
    输入：
        imgfile: 图片路径
        text: 文本
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    
    print featureDemo.prepare_request(input_data)#压测数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_VIRTUALHUMAN_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        # imgfile: 图片路径
        # text: 文本
        gen_stress_data({
            'imgfile': './image_dir/FEATURE_VIS_IMG_TXT_GPU/猛虎下山.jpeg',
            'text': '猛虎下山'
        })
    else:
        # 合成视频
        feature_calculate({
            'imgfile': './image_dir/FEATURE_VIS_IMG_TXT_GPU/猛虎下山.jpeg',
            'text': '猛虎下山'
        })
