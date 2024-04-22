#!/usr/bin/env python
# coding=utf-8
"""
Author: changwanli@baidu.com
since: 2021-02-03 19:55:39
LastTime: 2021-09-26 09:57:22
LastAuthor: changwanli@baidu.com
message: FEATURE_KG_TEXT_EGL_GPU Demo, 以及压测数据生成的DEMO
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
    FEATURE_KG_TEXT_EGL_GPU demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据

        Args:
            data (dict): key is [line,mention], mention is optional

        Returns:
            [str]: 返回算子的输入数据
        """
        return json.dumps(data)


def feature_calculate(input_data):
    """
    功能：特征计算

    Args:
        input_data (dict): key is [line,mention], the key of 'mention' is optional
    输出：
        实体链指结果
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
        'feature_name': 'FEATURE_KG_TEXT_EGL_GPU_V3',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path

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
    # 打印输出
    res_data = json.loads(res_data)
    res_data['feature_result']['value'] = json.loads(res_data['feature_result']['value'])
    print json.dumps(res_data, ensure_ascii=False, indent=4)


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待链指的文本，json 形式的 dict, key 是 line 和 mention(可选)，每一行是一个json字符串
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
    """
    main
    特征计算执行：
        python FEATURE_KG_TEXT_EGL_GPU.py
    生成压测数据：
        python FEATURE_KG_TEXT_EGL_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./text_dir/egl_stree_data_100.json')
    else:
        # 特征计算Demo
        """
        如果需要对进行知识获取，输入如下，请联系 wangguanchao@baidu.com 申请 tn 与 token
        input ={
            "line": u"刘德华的老婆是谁呀？",
            "mention":u"刘德华",
            "knowledge_acquisition": {
                "tn": "xxxxxxxx",
                "token": "xxxxxxxxx",
                "type_property": {
                    "Person": [
                        "alias",
                        "bdbkUrl",
                        "birthDate",
                        "gender",
                        "name",
                        "nationality"
                    ]
                }
            }
        }
        """
        input = {'line': u'刘德华的妻子是谁？', 'mention': u'刘德华'}

        feature_calculate(input)
