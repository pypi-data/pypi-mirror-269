#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: shengguangzhi
# @Date:   2021-11-29 21:06:11
"""
Brief: FEATURE_KG_LOCAL_OFFLINE_DATAFLOW_CPU_GENERAL_BASIC Demo, 以及压测数据生成的DEMO
Author: shengguangzhi(shengguangzhi@baidu.com)
Date: 2021-11-29
Filename: FEATURE_KG_LOCAL_OFFLINE_DATAFLOW_CPU_GENERAL_BASIC.py
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
        FEATURE_KG_LOCAL_OFFLINE_DATAFLOW_CPU_GENERAL_BASIC demo
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
        'feature_name': 'FEATURE_KG_LOCAL_OFFLINE_DATAFLOW_CPU_GENERAL_BASIC',
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
        python FEATURE_KG_LOCAL_OFFLINE_DATAFLOW_CPU_GENERAL_BASIC.py
    生成压测数据：
        python FEATURE_KG_LOCAL_OFFLINE_DATAFLOW_CPU_GENERAL_BASIC.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        gen_stress_data('./text_dir/topicgen_testcase.mini.txt')
    else:
        # 文本主题生成Demo
        test_data = {
            "title": "测试标题",
            "summary": "中新网江苏新闻7月2日电 7月1日，在喜庆的音乐声中，江苏沛县汉兴街道的10对新人肩并肩、手牵手，" + \
                       "走上红地毯喜结连理，他们共同以“零彩礼”集体婚礼的方式倡导时代文明新风。此次集体婚礼由沛县经济" + \
                       "开发区、汉兴街道主办，倡导移风易俗、婚事新办的社会新风，培养健康、文明、节俭的婚尚理念，展示新" + \
                       "时代广大青年满怀激情、奋发向上的精神风貌"
        }
        feature_calculate([test_data])
