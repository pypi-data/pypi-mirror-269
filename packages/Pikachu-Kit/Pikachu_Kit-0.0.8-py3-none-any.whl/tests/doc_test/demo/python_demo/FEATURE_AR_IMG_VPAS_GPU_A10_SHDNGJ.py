#! /usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_AR_IMG_VPAS_GPU_A10_SHDNGJ Demo, 以及压测数据生成的DEMO
Author: zhengxuexing(zhengxuexing@baidu.com)
Date: 2021-08-24
Filename: FEATURE_AR_IMG_VPAS_GPU_A10_SHDNGJ.py 
"""
import os

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import requests

class FeatureReq(XvisionDemo):
    """
    FEATURE_AR_IMG_VPAS_GPU_A10_SHDNGJ demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（log_id，context，request_data）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps(
            {
                'log_id': '20210811-1624-py',
                'context': '',
                'request_data': data['request_pb']
            })

def trackframe(input_data):
    """
    功能：测试 trackframe 接口
    输入：
        input_data: request_pb 路径
    输出：
        trackframe 结果
    """
    featureDemo = FeatureReq()
    # 生成算子输入
    data = {
        "request_pb": base64.b64encode(Util.read_file(input_data["request_pb"]))
    }
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_AR_IMG_VPAS_GPU_A10_SHDNGJ',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    # url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path
    url = featureDemo.xvision_test_url + featureDemo.xvision_sync_path

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
    

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_AR_IMG_VPAS_GPU_A10_SHDNGJ.py
    生成压测数据：
        python FEATURE_AR_IMG_VPAS_GPU_A10_SHDNGJ.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'FEATURE_CALCULATE':
        # 视觉定位 Demo
        input_data = {
            'request_pb': './proto/FEATURE_AR_IMG_VPAS_GPU_A10/request_data.pb'
        }
        trackframe(input_data)  # 本地 request_pb 数据
