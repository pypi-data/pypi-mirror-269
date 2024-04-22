#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_NETDISK_VIDEO_TRANSCODE_GPU Demo
Author: daixing(daixing@baidu.com)
Date: 2020-08-10
Filename: FEATURE_NETDISK_VIDEO_TRANSCODE_GPU.py
"""

from xvision_demo import XvisionDemo
import json
import sys
import random

class FeatureReq(XvisionDemo):
    """
    FEATURE_NETDISK_VIDEO_TRANSCODE_GPU demo
    """
    def prepare_request(self, data):
        """
        功能：构建输入参数
        输入：
            src_id： 视频的md5
            输出：
        """
        return json.dumps({
                    'src_id': data,
                })


def feature_calculate(input_data):
    """
    功能：发送转码请求
    输入：
        input_data:视频md5
    输出：
    
    """
    featureDemo = FeatureReq()
    #生成算子输入
    
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NETDISK_VIDEO_TRANSCODE_GPU',
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

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    print "no nedd stress"


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NETDISK_VIDEO_TRANSCODE_GPU.py
    生成压测数据：
        python FEATURE_NETDISK_VIDEO_TRANSCODE_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data("") #./image_dir/ 是本地的图片数据
    else:
        src_id = "47904bcb9rd767f7e7638d4249a8634a"
        #特征计算Demo
        feature_calculate(src_id) #./image_dir/img_file 本地图片

