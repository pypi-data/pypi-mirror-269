#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_FEED_VIDEO_SOUND_SILENCE_CPU_V1 Demo, 以及压测数据生成的DEMO
Author: work(work@baidu.com)
Date: 2019-08-23
Filename: FEATURE_FEED_VIDEO_SOUND_SILENCE_CPU_V1.py 
"""
from xvision_demo import XvisionDemo
import random
import sys


class FeatureReq(XvisionDemo):
    """
    FEATURE_FEED_VIDEO_SOUND_SILENCE_CPU_V1 demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型 or string，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_data = "svc_name=sound_silence_check&video_url=" + data['video_url']
        return req_data


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
                "video_url": input_data
            }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_FEED_VIDEO_SOUND_SILENCE_CPU_V1',
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

def gen_stress_data(input_data):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    demo = FeatureReq()
    #压测数据生成demo
    for video_url in input_data:
        data = {
                "video_url": video_url
                }
        print demo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_FEED_VIDEO_SOUND_SILENCE_CPU_V1.py 
    生成压测数据：
        python FEATURE_FEED_VIDEO_SOUND_SILENCE_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        video_data = ['http://vd3.bdstatic.com/mda-ja9j4zi1mntjs0aq/mda-ja9j4zi1mntjs0aq.mp4']
        gen_stress_data(video_data)
    else:
        #特征计算Demo
        video_url = 'http://vd3.bdstatic.com/mda-ja9j4zi1mntjs0aq/mda-ja9j4zi1mntjs0aq.mp4'
        feature_calculate(video_url)