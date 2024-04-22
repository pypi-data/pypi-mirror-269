# !/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:
@Author: chendawei(chendawei03@baiu.com)
@Date:   2020-04-27
@Filename: FEATURE_ACG_IMG_FACE_TRACKING_GPU.py
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


class FeatureReq(XvisionDemo):
    """
    FEATURE_ACG_IMG_FACE_TRACKING_GPU demo
    """

    def prepare_request(self, data_map):
        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(json.dumps(data_map)),
        })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()
    feature_data = feature_demo.prepare_request(input_data)
    # 生成百度视频中台输入

    job_name = ""  # 需要替换成平台的job_name
    token = ""  # 需要替换成作业详情的token

    callback = {}
    callback["bns"] = "my-bns"  # 回调服务的bns
    callback["path"] = "/callback-path/test"  # 服务接收回调的url

    callback_str = json.dumps(callback)

    job_name = ""  # 需要替换成平台的job_name
    token = ""  # 需要替换成作业详情的token

    xvision_data = gen_data({
        'business_name': job_name,
        'resource_key': 'test.jpg',
        'auth_key': token,
        'feature_name': 'FEATURE_ACG_IMG_FACE_TRACKING_GPU',  # 算子名
        'feature_input_data': feature_data,
        'callback': callback_str
    })
    # 获取url
    # 在线作业：xvision_online_url，离线作业：xvision_offline_url
    # 回调算子专用格式url
    url = "http://xvision-api.sdns.baidu.com/xvision/xvision_callback?business_name=" \
          + job_name + "acg_face_tracking&feature_name=FEATURE_ACG_IMG_FACE_TRACKING_GPU"
    # 请求百度视频中台特征计算服务""

    #高可用型、均衡型作业需将job_name, feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": xvision_data["business_name"],
            "feature_name": xvision_data["feature_name"]
        }
    else:
        params = {}

    res_data = feature_demo.request_feat(params, xvision_data, url)
    # 打印输出
    feature_demo.parse_result(res_data)


def gen_data(argv_dict):
    """
    功能：生成百度视频中台输入(适用于/xvision/xvision_sync接口)
    输入：
        argv_dict = {
            'business_name': '',#作业名
            'resource_key': '',#数据标记，可以是图片/视频/音频的title
            'auth_key': '',#token
            'feature_name',#算子名，比如FEATURE_xxxx
            'feature_input_data': ''#算子输入数据
        }
    输出：
        百度视频中台的输入
    """
    return {
        "business_name": argv_dict['business_name'],
        "resource_key": argv_dict['resource_key'],
        "auth_key": argv_dict['auth_key'],  # token
        "feature_name": argv_dict['feature_name'],  # 算子名
        "data": base64.b64encode(argv_dict['feature_input_data']),
        "callback": argv_dict['callback']
    }


def gen_stress_data(input_data):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    # 压测数据生成demo
    with open('img_file', 'a') as f:
        for i in range(200):
            f.write(feature_demo.prepare_request(input_data))
            f.write('\n')


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_DE_IMG_LUTAOELEMENT_GPU.py
    生成压测数据：
        python FEATURE_DE_IMG_LUTAOELEMENT_GPU.py GEN_STRESS_DATA

    本算子只适用于异步调用
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    data_map = {}
    data_map['mode'] = 'async'
    data_map['jobId'] = 'tracking-callback-test'
    data_map['timeoutInMs'] = 2000000
    data_map['args'] = ["face_tracking"]
    data_map['enableStdout'] = True
    data_map['enableStderr'] = False
    # 替换 bos信息
    data_map['stdin'] = "{\"type\": \"face_tracking\",\"params\": {\"zipFileUrl\": " \
                        "\"https://bj.bcebos.com/v1/videoai-vio/videoai_in_one/chendawei/images_1.tar\"," \
                        "\"sampleRate\": " \
                        "16000,\"target\": {\"host\":\"bj.bcebos.com\",\"bucket\":\"my-bucket\"," \
                        "\"ak\":\"12312321321\",\"sk\":\"123123213123213\"," \
                        "\"object\":\"test/\"}}, \"config\":{}} "
    data_map['callback'] = 'http://127.0.0.1:10001'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data(data_map)
    else:
        # 特征计算Demo
        feature_calculate(data_map)

