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


def prepare_req(video_path, info):
    """
    功能：构建算子的输入数据
    输入：
        video_path：视频地址
        info 服务信息
    输出：
        返回算子的输入数据
    """
    demo = {
        'session_id': '123',
        'video_base64': base64.b64encode(open(video_path, 'rb').read()),
        'mode': 1,
        'pic_num': 1024,
        'frame_rate': 25,
        'debug': 1
    }
    url = 'http://' + info['server'] + '/xvision/xvision_sync'

    headers = {
        'resource_key': 'test.jpg',
        'auth_key': info['token'],
        'business_name': info['job'],
        'feature_name': info['feature'],
        'logid': str(random.randint(1000000, 100000000))
    }

    req = urllib2.Request(url, data=json.dumps(demo), headers=headers)
    req.add_header('Content-Type', 'application/json')
    return req


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
    time_start = time.time()
    req = prepare_req(video_path, prepare_info())
    res = urllib2.urlopen(req).read()
    print res
    # print res
    json_data = json.loads(res)
    feature = json_data['feature_result']
    value = json.loads(feature['value'])
    time_end = time.time()
    cost_ms = (time_end - time_start) * 1000
    print 'cost(ms):%f' % cost_ms


if __name__ == '__main__':
    """
        主函数
    """
    simple_test(sys.argv[1])
