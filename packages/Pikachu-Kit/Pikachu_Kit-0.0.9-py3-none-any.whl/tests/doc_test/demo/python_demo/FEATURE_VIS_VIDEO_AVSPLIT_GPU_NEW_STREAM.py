#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_VIS_VIDEO_AVSPLIT_GPU Demo, 以及压测数据生成的DEMO
Author: zhuangjingpeng(zhuangjingpeng@baidu.com)
Date: 2020-10-27
Filename: FEATURE_VIS_VIDEO_AVSPLIT_GPU.py
"""

import random
import urllib2
import json
import time
import base64
import os
import sys

import requests


def prepare_info():
    """
        功能：算子服务配置
    """
    return {
        'server': 'xvision-api.sdns.baidu.com',
        'feature': 'FEATURE_VIS_VIDEO_AVSPLIT_GPU',
        'job': '',
        'token': ''
    }


def simple_test(video_path):
    """
       功能：执行算子调用服务
       输入：
           video_path:本地视频地址
       输出：
           调用返回
    """
    params = {
        'session_id': '123',
        'mode': 1,
        'frame_rate': 4,
        'pic_num': 8,
        'debug': 1
    }

    data = open('%s' % video_path, 'rb').read()
    url = 'http://' + prepare_info()['server'] + '/xvision/xvision_sync'
    headers = {
        'resource_key': 'test.jpg',
        'auth_key': '',
        'business_name': '',
        'feature_name': 'FEATURE_VIS_VIDEO_AVSPLIT_GPU',
        'logid': str(random.randint(1000000, 100000000)),
        'Content-Type': "multipart/form-data"
    }
    res = requests.post(url, params=params, data=data, headers=headers)

    time_start = time.time()
    json_data = json.loads(res.text)
    feature = json_data['feature_result']
    value = json.loads(feature['value'])
    print json.dumps(value)
    time_end = time.time()
    cost_ms = (time_end - time_start) * 1000
    print 'cost(ms):%f' % cost_ms


if __name__ == '__main__':
    """
        主函数
    """
    simple_test(sys.argv[1])
