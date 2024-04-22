#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1 Demo, 以及压测数据生成的DEMO
Filename: FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1.py
author: chengang06@baidu.com
"""

from xvision_demo import XvisionDemo
from util import Util
import urllib
import sys
import random


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1 demo
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
            "video_url": data['video_url'],
            "svc_name": "FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1",
            "logid": self.logid
        }
        return urllib.urlencode(req_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    data = {
        'video_url': input_data['video_url'],
    }
    feature_data = feature_demo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1',
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
    # 压测数据生成demo
    video_info_list = Util.read_video_file(input_dir)
    for video_info in video_info_list:
        data = {
            'video_url': video_info['video_url'],
        }
        print feature_demo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1.py
    生成压测数据：
        python FEATURE_VIS_VIDEO_VIDEOTAG_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./video_dir/video_data.txt')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        video_info_list = Util.read_video_file('./video_dir/video_data.txt')
        feature_calculate(video_info_list[0])
