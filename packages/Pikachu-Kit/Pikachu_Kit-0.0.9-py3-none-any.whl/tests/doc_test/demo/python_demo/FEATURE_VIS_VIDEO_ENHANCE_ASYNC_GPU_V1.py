#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_CVPRE_VIDEO_CUTFRAME_GPU_ASYNC.py Demo
Author: caoqiyun(caoqiyun@baidu.com)
Date: 2021-07-19
Filename: FEATURE_CVPRE_VIDEO_CUTFRAME_GPU_ASYNC.py
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import sys
import random
import base64


class FeatureReq(XvisionDemo):
    """
    FEATURE_CVPRE_VIDEO_CUTFRAME_GPU_ASYNC demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        data = {
            "url":data,
            "store":{
                "bos":{
                    "ak":"",
                    "sk":"",
                    "bucket":"video-extract-test",
                    "path":"tmp/" + str(self.logid) + "/",
                    "endpoint":"http://bj.bcebos.com"
                },
                "bigpipe":{
                    "cluster":"bigpipe_gz_public_cluster",
                    "host":"bigpipe-gz-proxy.dmop.baidu.com:2181",
                    "webservice":"group.opera-gzpublic-bigpipeGW-all-guangzhou.Bigpipe.all",
                    "user":"",
                    "password":"",
                    "token":"",
                    "pipe":"",
                    "video_id":1,  # pipeletid
                    "audio_id":2  # pipeletid
                }
            },
            "rule":{
                "video":{
                    "spf":5,
                    "start":0,
                    "end":106200
                },
                #"audio":{
                #    "vad":True,
                #    "max_piece_time":60
                #}
            }
        }
      
        return json.dumps({
                    'appid': '123456',
                    'logid': self.logid,
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(json.dumps(data)),
                })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    logid = random.randint(1000000, 100000000)
    featureDemo.logid = logid
    # 生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    # 生成百度视频中台输入
    callback_server_info = {
        # "bns"                 : "bns_name_example",           # 可选，BNS 与host 两个必须指定一个，同时指定时优先使用BNS
        # "port_name"           : "port_name",                  # 可选，与bns一起使用，指定BNS 的端口名称，如果端口名非默认名称时需要指定
        "host": "yourhost.baidu.com",
        "port": 8807,
        "path": "/xxx/path/xxx"  # 异步回调路径
    }

    job_name = ''
    token = ''

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_CVPRE_VIDEO_CUTFRAME_GPU_ASYNC',
        'X_BD_LOGID': str(logid)
    }

    xvision_data = {
        'business_name': job_name,  # job_name
        'resource_key': 'test.jpg',  # passthrough data
        'auth_key': token,  # token
        'feature_name': 'FEATURE_CVPRE_VIDEO_CUTFRAME_GPU_ASYNC',  # 算子名
        'data': base64.b64encode(feature_data),
        "callback": json.dumps(callback_server_info)  # 可选，默认为提交作业时提交的回调信息, 优先使用这里的指定参数
    }

    # 异步访问
    url = featureDemo.xvision_online_url + featureDemo.xvision_callback_path
    params = {
        "business_name": xvision_data["business_name"],
        "feature_name": xvision_data["feature_name"]
    }

    print(xvision_data)
    # 请求百度视频中台特征计算服务
    res_data = featureDemo.request_feat(params, xvision_data, url)
    # 打印输出
    featureDemo.parse_result(res_data)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    video_info_list = Util.read_video_file('./video_dir/video_data.txt')
    for video_info in video_info_list:
        data = {
            'video_url': video_info['video_url'],
        }
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_CVPRE_VIDEO_CUTFRAME_GPU_ASYNC.py
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        #feature_calculate("http://video-extract-test.bj.bcebos.com/brave_heart_h264_aac_BD720P.mp4")
        #feature_calculate("http://video-extract-test.bj.bcebos.com/1_e689aaef88f1474fb9361c9ffd1e6dd0.mp4")
        feature_calculate("http://video-extract-test.bj.bcebos.com/h264_aac.mp4")
