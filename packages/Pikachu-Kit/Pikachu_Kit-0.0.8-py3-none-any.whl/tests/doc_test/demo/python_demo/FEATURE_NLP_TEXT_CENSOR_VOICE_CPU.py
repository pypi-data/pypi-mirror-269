#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_NLP_TEXT_CENSOR_VOICE_CPU Demo, 以及压测数据生成的DEMO
Author: zhangxiaobin04(zhangxiaobin04@baidu.com)
Date: 2020-11-25
Filename: FEATURE_NLP_TEXT_CENSOR_VOICE_CPU.py
"""
import json
import random
import sys
import base64
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_NLP_TEXT_CENSOR_VOICE_CPU demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（text）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        json_data = {
            "fields": {"content": data},
            "config": {
                "labels": ["1", "2", "3", "4", "5", "6"],
                "sub_labels": {"4": ["1", "2"]}
            }
        }
        return json.dumps({
            "appid": "123456",
            "logid": "123456",
            "format": "json",
            "from": "test-python",
            "cmdid": "123",  # 这个暂时没有用到，可以写死
            "clientip": "0.0.0.0",  # client ip
            "data": base64.b64encode(json.dumps(json_data, ensure_ascii=False))
        })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: 文本内容
    输出：
        预测结果
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    feature_data = feature_demo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NLP_TEXT_CENSOR_VOICE_CPU',
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


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:（文本）
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, "r") as fin:
        for i in fin:
            data = i.strip()
            print feature_demo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NLP_TEXT_CENSOR_VOICE_CPU.py
    生成压测数据：
        python FEATURE_NLP_TEXT_CENSOR_VOICE_CPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./text_dir/perf_text.txt')  # ./text_dir/perf_text.txt 是本地的文本数据
    else:
        # 特征计算Demo
        feature_calculate('今天天气如何')  # "今天天气如何" 是本地测试数据
