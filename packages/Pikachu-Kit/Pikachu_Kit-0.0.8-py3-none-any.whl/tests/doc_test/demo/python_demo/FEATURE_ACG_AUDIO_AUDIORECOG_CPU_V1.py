#!/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:
@Author: yangyongzhen(yangyongzhen@baiu.com)
@Date:   2020-03-13
@Filename: FEATURE_ACG_AUDIO_AUDIORECOG_CPU_V1.py
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import sys
import os
import random


class FeatureReq(XvisionDemo):
    """
    FEATURE_ACG_AUDIO_AUDIORECOG_CPU_V1 demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_data = {
            "request_id": str(random.randint(1000000, 100000000)), # 请求唯一标识，如果不指定，后端会随机生成一个。
            "audio_meta": "audio_meta", #可以将音频信息放在请求里，在返回的时候会原样返回，在一些异步请求的场景下，会更方便
        }
        return json.dumps(req_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地音频文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()
    #生成算子输入
    data = {
        "audio": Util.read_file(input_data),
    }
    feature_data = feature_demo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_ACG_AUDIO_AUDIORECOG_CPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    feature_demo.parse_result(res_data)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    #压测数据生成demo
    audio_file_list = os.listdir(input_dir) #input_dir里边是音频
    with open('audio_file', 'a') as f:
        for audio_file in audio_file_list:
            data = {
                "audio": Util.read_file(input_dir + '/' + audio_file),
            }
            f.write(feature_demo.prepare_request(data))
            f.write('\n')


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_ACG_AUDIO_AUDIORECOG_CPU_V1.py
    生成压测数据：
        python FEATURE_ACG_AUDIO_AUDIORECOG_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./wav_dir/') #./wav_dir/ 是本地的语音数据
    else:
        #特征计算Demo
        feature_calculate('./wav_dir') #./wav_dir 是本地的语音数据