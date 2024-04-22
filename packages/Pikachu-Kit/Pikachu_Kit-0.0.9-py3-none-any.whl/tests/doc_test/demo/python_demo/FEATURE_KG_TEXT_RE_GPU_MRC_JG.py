#!/usr/bin/env python3
# coding=utf-8


"""
Author: sunjiandong@baidu.com
since: 2021-12-29 13:42:39
LastTime: 2021-12-29 14:23:14
LastAuthor: sunjiandong@baidu.com
message: FEATURE_KG_TEXT_RE_GPU_MRC_JG Demo, 以及用于压测数据生成的DEMO
Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
"""


from xvision_demo import XvisionDemo
from util import Util
import json
import random
import sys
import os
import base64


class FeatureReq(XvisionDemo):
    """
    FEATURE_KG_TEXT_RE_GPU_MRC_JG demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据

        Args:
            data: dict, data for request

        Returns:
            [str]: 返回算子的输入数据

        """
        request_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        print(request_data)
        return request_data


def feature_calculate(input_data):
    """
    功能：特征计算

    Args:
        input_data: dict, request data
    输出：
        kger 结果
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    feature_data = feature_demo.prepare_request(input_data)

    job_name = ""  # 应用名
    token = ""  # token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_KG_TEXT_RE_GPU_MRC_JG',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path
    # url = feature_demo.xvision_test_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    # 请求百度视频中台特征计算服务
    print(params)
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    res_data = json.loads(res_data)
    print(res_data)

    return res_data


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待链指的文本，json 形式的 dict, key 是 line 和 mention(可选)，每一行是一个json字符串
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            print(feature_demo.prepare_request(data))


if __name__ == '__main__':
    # 特征计算Demo
    input = {
                "texts": [
                    {"text": "美国专家称，俄罗斯t-90坦克是世界上最致命的坦克。"},
                    {"text": "C-17 运输机和 F-18 战斗机均属于美空军，其编号分别为 C-1716 和 F-1812。"}
                ],
                "config": {
                    "model_name": "mrc_model",
                    "domain": "JG"
                }
            }

    print(json.dumps(feature_calculate(input), ensure_ascii=False, indent=4))
