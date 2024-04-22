#!/usr/bin/env python
# coding=utf-8
"""
Author: yangbaoshan@baidu.com
since: 2022-07-05
message: FEATURE_KG_TEXT_ICACOREENTITY_GPU_V0 Demo, 以及压测数据生成的DEMO
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
    FEATURE_KG_TEXT_TAG_GPU_V2 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据

        Args:
            data (dict): key is [line,meta]

        Returns:
            [str]: 返回算子的输入数据
        """
        return json.dumps(data)


def feature_calculate(input_data):
    """
    功能：特征计算

    Args:
        input_data (dict): key is data
    输出：
        NER 结果
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
        'feature_name': 'FEATURE_KG_TEXT_ICACOREENTITY_GPU_V0',
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
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)

    res_data = json.loads(res_data)
    res_data['feature_result']['value'] = json.loads(res_data['feature_result']['value'])
    return res_data


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待链指的文本，json 形式的 dict, key 是 content 和 meta，每一行是一个json字符串,详见测试数据
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            line = json.loads(line.strip())
            print featureDemo.prepare_request(line)


if __name__ == '__main__':
    # 特征计算Demo
    data = {"data":[
                {
                    "content_type": "rawtext",
                    "content":
                    [
                         "男单众好手齐聚日本公开赛 谌龙急需一冠证明自己"
                    ],
                    "meta":
                    {
                         "entity_list":
                        [
                            {
                                "type": "",
                                "entity": "日本公开赛"
                            },
                            {
                                "type": "",
                                "entity": "谌龙"
                            },
                            {
                                "type": "",
                                "entity": "男单"
                            },
                            {
                                "type": "",
                                "entity": "日本"
                            }
                        ]
                    }
                }
            ]
        }
    # print()
    print(json.dumps(feature_calculate(data), ensure_ascii=False, indent=4))
