#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU Demo, 以及压测数据生成的DEMO
Author: hupeng08(hupeng08@baidu.com)
Date: 2021-12-21
Filename: FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import re
import os

class FeatureReq(XvisionDemo):
    """
    FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：json串，参考示例
        输出：
            返回算子的输入数据
        """

        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(data),
                })

    def parse_result(self, response):
        """
        功能：解析结果
        输入：
            response: 请求返回响应的结果
        """

        response_json = json.loads(response)
        value = response_json["feature_result"]["value"]
        value_json = json.loads(value)
        result = value_json["result"]
        result_data = base64.b64decode(result)
        result_json = json.loads(result_data)

        print("[INFO] check result label: [{0}], score: [{1}], suggestion: [{2}], "  \
                    "errno: [{3}], errmas: [{4}]".format(
                    result_json["gediao_label"], result_json["gediao_score"], 
                    result_json["gediao_suggestion"], result_json["errno"], 
                    result_json["errmas"]))


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地文件
    输出：
        文本格调审核结果
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU',
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


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_data:（文本）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_file, "r") as fin:
        for i in fin:
            data = i.strip()
            print featureDemo.prepare_request(data)  #压测词表数据


def text_process(text):
    """将长文本进行切分, 先按照标点符号切分, 再按照128长度切分, 如果文本长度小于10则不切分, 返回切分列表
    Args:
    text: input text
    
    Return:
    divide text list
    """
    PUNCS = "[{}]".format('\!\?\;。？！；')

    text_list = []
    text_u = text.decode("utf-8", "ignore")

    # return if text too short
    if len(text_u) < 10:
        text_list.append(text)
        return text_list

    values = re.split(PUNCS.decode("utf-8"), text_u)
    for value in values:
        if len(value.strip()) == 0:
            continue

        value_split = re.findall(r'.{128}', value)
        for tt in value_split:
            text_list.append(tt.encode("utf-8", "ignore"))
        last_text = value[(128 * len(value_split)):]
        if len(last_text) > 0:
            text_list.append(last_text.encode("utf-8", "ignore"))

    return text_list


def main():
    """
    main
    简单测试执行：
        python2 FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU.py 
    生成压测数据：
        python2 FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU.py GEN_STRESS_DATA
    使用标准输入审核数据执行：
        echo "今天天气如何" | python2 FEATURE_ANTISPAM_GEDIAO_MODEL_SERVICE_CPU.py STD_INPUT_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/anti_text.txt')  #./text_dir/anti_text.txt 是本地的文本数据
    elif op_type == "STD_INPUT_DATA":
        #标准输入进行预测
        for line in sys.stdin:
            line = line.rstrip("\n")
            text_list = text_process(line)
            input_info = {"check_types": ["porn", "illegal"], "check_texts": text_list}
            feature_calculate(json.dumps(input_info))
    else:
        feature_calculate(json.dumps({"check_types": ["illegal"], "check_texts": ["今天天气如何"]}))  # "今天天气如何" 是本地测试数据


if __name__ == '__main__':
    main()
