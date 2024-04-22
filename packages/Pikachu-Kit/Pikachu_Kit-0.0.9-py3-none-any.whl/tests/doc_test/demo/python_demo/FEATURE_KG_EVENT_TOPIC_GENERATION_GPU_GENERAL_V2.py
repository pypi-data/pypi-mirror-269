#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: shengguangzhi
# @Date:   2021-08-25 16:16:00
"""
Brief: FEATURE_KG_EVENT_TOPIC_GENERATION_GPU_GENERAL_V2 Demo, 以及压测数据生成的DEMO
Author: shengguangzhi(shengguangzhi@baidu.com)
Date: 2021-08-25
Filename: FEATURE_KG_EVENT_TOPIC_GENERATION_GPU_GENERAL_V2.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import os

class FeatureReq(XvisionDemo):
    """
        FEATURE_KG_EVENT_TOPIC_GENERATION_GPU_GENERAL_V2 demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：string类型，待计算的文本
        输出：
            返回算子的输入数据
        """
        return json.dumps({"data": data})


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:待计算的文本
    输出：
        切分好的文本特征
    """
    feature_demo = FeatureReq()
    #生成算子输入
    feature_data = feature_demo.prepare_request(input_data)

    job_name = "" #应用名
    token = "" #token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_KG_EVENT_TOPIC_GENERATION_GPU_GENERAL_V2',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    #获取url
    #高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    #请求百度视频中台特征计算服务
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    #打印输出
    feature_demo.parse_result(res_data)


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待切分文本文件，每一行是一个JSON
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            print featureDemo.prepare_request(data["data"]) # 压测文本内容数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_KG_EVENT_TOPIC_GENERATION_GPU_GENERAL_V2.py
    生成压测数据：
        python FEATURE_KG_EVENT_TOPIC_GENERATION_GPU_GENERAL_V2.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        gen_stress_data('./text_dir/topicgen_testcase.mini.v2.txt')
    else:
        # 文本主题生成Demo
        test_data = {
            "title": "沈梦辰和杜海涛官宣结婚，婚戒很大，谢娜吴昕何炅暂时没祝贺！！",
            "summary": "嫁给沈梦辰杜海涛关璇，他们相恋9年，长跑终于有了结果。" + \
                       "杜海涛和沈梦辰在娱乐圈相恋已久，但两人感情很好。因为他" + \
                       "和杜海涛官方公布的恋情，口碑反转，然后得到了汪涵的支持他很" + \
                       "会自欺欺人，虽然偶尔还是有恶评，但问题不大。对于沈梦辰和杜海涛，" + \
                       "的正式宣布结婚，主持人朱桢第送上祝福，随后是李维嘉，和主持人刘烨，作为四朵小花之一。"
        }
        feature_calculate([test_data])
