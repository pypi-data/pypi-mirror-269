#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_NLP_TEXT_CTINKER_LIGHTDET_CPU_V01 Demo, 以及压测数据生成的DEMO
Author: mayun03(mayun03@baidu.com)
Date: 2022-11-30
Filename: FEATURE_NLP_TEXT_CTINKER_LIGHTDET_CPU_V01.py
"""
import json
import os
import random
import sys
import urllib
import base64
import time

from util import Util
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_NLP_TEXT_CTINKER_LIGHTDET_CPU_V01 demo
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
            "action": "text_correction",
            "data":
            [
                {
                    "content": data
                }
            ],
            "subservice": {
            "is_punct":True,
            "is_article": True,
            "is_ecnet": False,
            "is_fever": True,
            "is_sent": True,
            "is_hfreq": False,
            "is_rule": True,
            "is_entity": False,
            "is_address": True,
            "is_poem": True
        },
            "source": "word",
            "system": "Unix",
            "type": 1,
            "user_id": "002",
            "web_version": "v1.0",
        }
        request_data = {
            "appid": "123456",      # 注意这里是 str
            "logid": int(time.time()*1000),
            "format": "json",
            "from": "test-python",
            "cmdid": "123",     # 这个暂时没有用到，可以写死
            "clientip": "0.0.0.0",    # client ip
            "data": base64.b64encode(json.dumps(json_data, ensure_ascii=False))
        }
        return json.dumps(request_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: 文本内容
    输出：
        预测结果
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)
    print(feature_data)
    #生成百度视频中台输入

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': '',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NLP_TEXT_CTINKER_LIGHTDET_CPU_V01',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 高可用型、均衡型作业：xvision_online_url;
    # 高吞吐型作业：xvision_offline_url;
    # 测试作业：xvision_test_url;
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
    #featureDemo.parse_result(res_data)
    # print(res_data)

    try:
        # 解析灵视返回的结果
        info = json.loads(res_data)
        print(json.dumps(info, ensure_ascii=False, indent=4))

        # 解析算子返回的输出
        result_str = info["feature_result"]["value"]
        result = json.loads(result_str)["result"]
        result = json.loads(base64.b64decode(result))
        print(json.dumps(result, ensure_ascii=False, indent=4))
    except:
        print("failed to parse data")


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:（文本）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_file, "r") as fin:
        for i in fin:
            data = i.strip()
            print(featureDemo.prepare_request(data))  #压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NLP_TEXT_CTINKER_LIGHTDET_CPU_V01.py
    生成压测数据：
        python FEATURE_NLP_TEXT_CTINKER_LIGHTDET_CPU_V01.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/perf_text.txt')  #./text_dir/perf_text.txt 是本地的文本数据
    else:
        #特征计算Demo
        sample = "习进平同志，第二社区社区马上取采了措施，美丽地姑娘，河北省郑州市，人材,白日依山进"
        feature_calculate(sample)  #本地测试数据
