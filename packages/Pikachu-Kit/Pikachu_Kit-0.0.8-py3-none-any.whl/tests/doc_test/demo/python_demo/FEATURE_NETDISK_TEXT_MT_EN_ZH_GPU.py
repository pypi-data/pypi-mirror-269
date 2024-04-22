#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Description:
@Date       :2023/05/18 17:30:04
@Author     :yumengshi01@baidu.com
@version    :1.0
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

    def prepare_request(self, ori_data):
        """
        功能：构建算子的输入数据

        Args:
            data (dict): key is [data, stype], stype is optional

        Returns:
            [str]: 返回算子的输入数据
        """
        #s = {"chapter":ori_data, "logid":1, "sv_type":1}
        s = ori_data
        data = {"content":json.dumps(s)}

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
        'Content-Type': 'application/json;charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NETDISK_TEXT_MT_EN_ZH_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_test_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}
    # 请求百度视频中台特征计算服务
    #feature_data = '{"data": "{\\"chapter\\": \\"test\\", \\"logid\\": 1, \\"sv_type\\": 0}", "stype": 1}'
    #print(url)
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    feature_demo.parse_result(res_data)


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待评分的小说的文本，data中需要包含chapter，logid，sv_type缺一不可，每一行是一个json字符串
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            #line = json.loads(line.strip())
            print(featureDemo.prepare_request(line))


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_TEXT_CLASSIFY_GPU_NETDISC5.py
    生成压测数据：
        python FEATURE_TEXT_CLASSIFY_GPU_NETDISC5.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./text_dir/mt_en_zh_test.json')
    else:
        # 特征计算Demo
	#s = {"chapter":"test", "logid":1, "sv_type":0}
        #feature_calculate("dQXE7JUw7q8cCyb8DDWz2u4URUEy3/BTe0fg5DOofsU=")
        feature_calculate("Looking at the world, the scenery is better")