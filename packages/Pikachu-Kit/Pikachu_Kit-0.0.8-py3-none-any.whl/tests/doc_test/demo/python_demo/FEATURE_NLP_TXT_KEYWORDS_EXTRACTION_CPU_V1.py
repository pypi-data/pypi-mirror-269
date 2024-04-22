#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_NLP_TXT_KEYWORDS_EXTRACTION_CPU_V1 Demo, 以及压测数据生成的DEMO
Author: liqinrui(liqinrui@baidu.com)
Date: 2021-05-07
Filename: FEATURE_NLP_TXT_KEYWORDS_EXTRACTION_CPU_V1.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os

class FeatureReq(XvisionDemo):
    """
    FEATURE_NLP_TXT_KEYWORDS_EXTRACTION_CPU_V1 demo  
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


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NLP_TXT_KEYWORDS_EXTRACTION_CPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
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


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    file_list = sorted(os.listdir(input_dir)) #dir里边是文本列表，用于生成压测词表
    for file in file_list:
        with open(input_dir + '/' + file, "r") as fd:
            for line in fd:
                print featureDemo.prepare_request(line)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NLP_TXT_KEYWORDS_EXTRACTION_CPU_V1.py 
    生成压测数据：
        python FEATURE_NLP_TXT_KEYWORDS_EXTRACTION_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/') #./dir/ 是本地的文本数据
    else:
        #特征计算Demo
        feature_calculate('{"text_list":["据商务部网站7日消息，商务部等17部门发布《关于搞活汽车流通扩大汽车消费若干措施的通知》，\
            其中提到要支持新能源汽车消费、引导充电桩企业适当下调服务费、取消对二手车经销不合理限制、鼓励加大汽车消费信贷支持等。支持新能\
            源汽车消费引导充电桩企业适当下调服务费促进跨区域自由流通，破除新能源汽车市场地方保护，各地区不得设定本地新能源汽车车型备案目录，\
            不得对新能源汽车产品销售及消费补贴设定不合理车辆参数指标。支持新能源汽车消费，研究免征新能源汽车车辆购置税政策到期后延期问题。\
            深入开展新能源汽车下乡活动，鼓励有条件的地方出台下乡支持政策，引导企业加大活动优惠力度，促进农村地区新能源汽车消费使用。\
            积极支持充电设施建设，加快推进居住社区、停车场、加油站、高速公路服务区、客货运枢纽等充电设施建设，引导充电桩运营企业适当下调充电服务费。\
            取消对二手车经销不合理限制支持二手车流通规模化发展取消对开展二手车经销的不合理限制，明确登记注册住所和经营场所在二手车交易市场以外的企业\
            可以开展二手车销售业务。促进二手车商品化流通，明确汽车销售企业应当按照国家统一的会计制度，将购进并用于销售的二手车按照“库存商品”科目进行会计核算。\
            支持二手车流通规模化发展，各地区严格落实全面取消二手车限迁政策，自2022年8月1日起，在全国范围（含国家明确的大气污染防治重点区域）\
            取消对符合国五排放标准的小型非营运二手车的迁入限制，促进二手车自由流通和企业跨区域经营。"],"num":10}') # 本地文本
