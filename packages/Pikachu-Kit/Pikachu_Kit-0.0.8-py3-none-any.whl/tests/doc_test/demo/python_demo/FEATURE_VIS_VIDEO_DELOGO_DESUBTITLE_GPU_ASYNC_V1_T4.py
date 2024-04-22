#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_DELOGO_DESUBTITLE_GPU_ASYNC_V1_T4 Demo, 以及压测数据生成的DEMO
Author: liufanglong (liufanglong@baidu.com)
Date: 2022-03-04
Filename: FEATURE_VIS_VIDEO_DELOGO_DESUBTITLE_GPU_ASYNC_V1_T4.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import urllib
import sys
import os
import requests

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_DELOGO_DESUBTITLE_GPU_ASYNC_V1_T4 demo
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
                    'appid': '123456',      # 可选, 方便排查问题
                    'format': 'json',       # 可选, json: data 字段base64编码；其他值：data字段不编码
                    'from': 'test-python',  # 可选, 方便排查问题
                    'cmdid': '123',         # 可选, 方便排查问题
                    'clientip': '0.0.0.0',  # 可选, 方便排查问题
                    'logid': self.logid,    # 必选, 访问时需要在http header 中设置logid: X_BD_LOGID, 两个logid需要保持一致
                    'data': base64.b64encode(json.dumps(data)),
                })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:输入url
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
                "video_url": input_data
            }
    feature_data = featureDemo.prepare_request(data)

    callback_server_info  = {
        # "bns"                 : "bns_name_example",           # 可选，BNS 与host 两个必须指定一个，同时指定时优先使用BNS
        # "port_name"           : "port_name",                  # 可选，与bns一起使用，指定BNS 的端口名称，如果端口名非默认名称时需要指定
        # "host"                : "host_name_example",          # 可选，BNS 与host 两个必须指定一个，同时指定时优先使用BNS
        # "port"                : 8888,                         # 可选，与host一起使用，指定访问主机的端口号，默认是80
        # "path"                : "/url/path",                  # 必选，回调url的path
        # "method"              : "post",                       # 可选，目前仅支持post
        # "connect_timeout"     : 1500,                         # 可选，指定连接超时时间，单位毫秒
        # "read_timeout"        : 1500,                         # 可选，指定读超时时间，单位毫秒
        # "write_timeout"       : 1500,                         # 可选，指定写超时时间，单位毫秒,
                                                                # 总的回调超时时间（连接超时+读超时+ 写超时）最大为60秒（60000）（仅针对回调，不包括算子运行时间）
        # "retry_times"         : 4,                            # 可选，重试次数，总访问次数为重试次数+1
        "host": "yq01-ps-1-m42-pc49.yq01.baidu.com",
        "port": 8089,
        "path": "/xvision/post",
    }

    job_name = ""
    token  = ""

    #生成百度视频中台输入
    xvision_data = {
            'business_name': job_name,                                          # job_name
            'resource_key': 'test.jpg',                                         # passthrough data
            'auth_key': token,                                                  # token
            'feature_name': 'FEATURE_VIS_VIDEO_DELOGO_DESUBTITLE_GPU_ASYNC_V1_T4',           # 算子名
            'data': base64.b64encode(feature_data),
            "callback": json.dumps(callback_server_info),                       #  可选，默认为提交作业时提交的回调信息, 优先使用这里的指定参数
    }
    #获取url
    #近线作业: xvision_online_url
    #离线作业: xvision_offline_url
    #调研作业: xvision_test_url
    #在线作业: xvision_online_ex_sdns_url: 在线作业要求在调用的URL中传入作业名和算子名，用于匹配流量转发规则, xvision_data 中的作业名和算子名此时为可选
    online_ex_data = "?business_name=%s&feature_name=%s" % (xvision_data["business_name"], xvision_data["feature_name"])

    # 注意该算子只允许异步访问
    url = featureDemo.xvision_online_url + featureDemo.xvision_callback_path + online_ex_data
    # url = featureDemo.xvision_sandbox_url + featureDemo.xvision_callback_path + online_ex_data

    # 指定数据类型和logid
    http_headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "X_BD_LOGID": "%d" % featureDemo.logid,
    }

    #请求百度视频中台特征计算服务
    res_data = requests.post(url, json.dumps(xvision_data), headers=http_headers)
    #打印输出
    featureDemo.parse_result(res_data.text)


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_file) as fd:
        for video_url in fd.readlines():
            if len(video_url.strip()) > 0:
                data = {
                        "video_url": video_url,
                }
                print featureDemo.prepare_request(data) #压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_DELOGO_DESUBTITLE_GPU_ASYNC_V1_T4.py
    """
    #特征计算Demo
    test_video_url = "http://10.128.225.31:8346" + \
            "/file/a541189c743b3c06c44a1dbf46f171a0/file_name/mda-jmgvqt3p5itd4a1i.mp4"
    feature_calculate(test_video_url)