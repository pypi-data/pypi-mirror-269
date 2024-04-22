#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_OCR_CPU_IDCARD_V1 Demo, 以及压测数据生成的DEMO
Author: Wu Yongjun(wuyongjun01@baidu.com)
Date: 2020-03-14
Filename: FEATURE_VIS_IMG_OCR_CPU_IDCARD_V1.py
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
    FEATURE_VIS_IMG_OCR_CPU_IDCARD_V1 demo
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
        # st_ocrapi(返回行识别结果),st_ocrapi_all（返回行和单字结果）
        data += "type=st_ocrapi_all"

        # LocateRecognize（检测识别）；Recognize（只识别）；Locate（只检测）
        data += "&detecttype=LocateRecognize"
        
        # CHN_ENG(中英)  、 ENG ，不填写这个字段默认为CHN_ENG
        data += "&languagetype=CHN_ENG"
        
        # v2
        data += "&locate_type=v2"
        
        # id_card（身份证正面），id_card_backside（身份证反面）
        data += "&object_type=id_card"
        
        # true/false是否方向判断，默认false
        data += "&imgDirection=true"
        
        # fast（识别小模型）high（识别大模型，推荐）
        data += "&accuracy_type=high"
        
        # 是否身份证五分类。true（是），false（否）
        data += "&is_detect_risk=true"
        
        # 身份证图片文件头，默认为空。可以填充为图片文件二进制文件头信息base64编码后结果。最大长度为base64编码前15KB
        # data += "&image_header_part=图片二进制数据前15KB的base64编码"
        
        # 是否返回行置信度。true（是），false（否），默认或不填为false
        data += "&line_probability=false"
        
        # 是否进行检测头像，会返回头像照片的base64编码和位置，默认为false
        data += "&is_detect_photo=false"
        
        # 是否进行检测头像位置，只返回头像照片的位置，默认为false
        data += "&is_detect_photo_location=false"
        
        # 强制进行横向识iiii别
        data += "&direction=horizontal"
        
        # 是否进行检测校正。true（是），false（否），默认为true
        data += "&is_detect_rectify=true"

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
        'feature_name': 'FEATURE_VIS_IMG_OCR_CPU_IDCARD_V1',
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
        python FEATURE_VIS_IMG_OCR_CPU_IDCARD_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_OCR_CPU_IDCARD_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/ocr.png')  # ./image_dir/img_file 本地图片
        # feature_calculate('./tmp/test.jpg')  # ./image_dir/img_file 本地图片
