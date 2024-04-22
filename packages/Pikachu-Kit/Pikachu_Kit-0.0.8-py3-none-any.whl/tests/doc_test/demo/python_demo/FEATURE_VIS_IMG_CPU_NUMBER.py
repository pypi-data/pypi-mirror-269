#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_CPU_NUMBER Demo, 以及压测数据生成的DEMO
Author: Wu Yongjun(wuyongjun01@baidu.com)
Date: 2020-03-14
Filename: FEATURE_VIS_IMG_CPU_NUMBER.py
"""

import os
import sys
import json
import base64
import random
import urllib

from util import Util
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_CPU_NUMBER demo
    """
    def prepare_request(self, imgData):
        """ prepare data for request

        Args:
            conf: conf file

        Returns:
            data: protobuf
        """

        # 算子提供方需要详情描述 data 字段, 必填
        data = ""

        # data的字段含义如下：
        # 可选，st_ocrapi_all结果带有单字，st_ocrapi无单字结果
        data += "type=st_ocrapi_all"
        # 必填，写死
        data += "&detecttype=LocateRecognize"
        # 必填，写死
        data += "&languagetype=CHN_ENG"
        # 必填，写死
        data += "&recg_type=seq"
        # 必填，写死
        data += "&locate_type=v2"
        # 是否加入方向判断，如果不加入这个字段则不加入方向判断，加入的话会加入方向判断
        data += "&imgDirection=setImgDirFlag"
        # 必填，写死
        data += "&object_type=number"

        # 可选
        #data += "&eng_granularity=word"
        #data += "&appid=10005"
        #data += "&clientip=x.x.x.x"
        #data += "&fromdevice=pc"
        #data += "&version=1.0.0"
        #data += "&encoding=1"
        #data += "&international=1"

        data += "&image=" + base64.b64encode(imgData)

        return json.dumps({
                'appid': 'xvision_job_name',
                'logid': random.randint(1000000, 100000000),
                'format': 'json',
                'from': 'test-python',
                'cmdid': '123',
                'client': '0.0.0.0', 
                'data': base64.b64encode(data),
        })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    # 生成算子输入
    feature_data = featureDemo.prepare_request(Util.read_file(input_data))

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_CPU_NUMBER',
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


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = Util.read_file(input_dir + '/' + image_file)
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_CPU_NUMBER.py
    生成压测数据：
        python FEATURE_VIS_IMG_CPU_NUMBER.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/ocr.png')  # ./image_dir/img_file 本地图片
