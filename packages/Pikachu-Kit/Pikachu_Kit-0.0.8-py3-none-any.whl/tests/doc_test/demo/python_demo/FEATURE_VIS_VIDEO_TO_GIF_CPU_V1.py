#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_TO_GIF_CPU_V1 Demo, 以及压测数据生成的DEMO
Author: wanghua11(wanghua11@baidu.com)
Date: 2019-09-20
Filename: FEATURE_VIS_VIDEO_TO_GIF_CPU_V1.py
"""
import base64
import json
import os
import random
import sys
import urllib
import commands
from util import Util
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_TO_GIF_CPU_V1 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps({
            'appid': 'xvision_job_name',
            'logid': random.randint(1000000, 100000000),
            'from': 'xvision',
            'clientip': commands.getoutput("hostname"),
            'data': base64.b64encode(json.dumps(data))
        })

def feature_calculate():
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    # 生成算子输入
    data = {
            "video_url": 'http://yq01-gpu-159-15-00.epc.baidu.com:8765/200a9405c49cef2360020c6d31e02f0b8b80e1b5.mp4',
            "ak": '07',
            "bucket": '',
            "sk": '',
            "video_rate": 1,
            "ocr_results": {
                    "00000001.jpg": [
                        [483, 256, 576, 115, "\u79d2dng\u89c6\u9891"]
                                    ]
                    }
            } 
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_VIDEO_TO_GIF_CPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
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
    featureDemo.parse_result(res_data)

def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as fp:
        data_file_list = fp.readlines() 
        for data in data_file_list:
            print featureDemo.prepare_request(json.loads(data.rstrip('\n')))  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_TO_GIF_CPU_V1.py
    生成压测数据：
        python FEATURE_VIS_VIDEO_TO_GIF_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./FEATURE_VIS_VIDEO_TO_GIF_CPU_V1_param2.json')  #FEATURE_VIS_VIDEO_TO_GIF_CPU_V1_param2.json 详细字段参见：http://xvision.baidu-int.com/xvision/operatorDetail?id=300, 字段都需要用户自己构造 
    else:
        # 特征计算Demo
        #feature_calculate('./image_dir/img_file')  # ./image_dir/img_file 本地图片
        feature_calculate()  # ./image_dir/img_file 本地图片

