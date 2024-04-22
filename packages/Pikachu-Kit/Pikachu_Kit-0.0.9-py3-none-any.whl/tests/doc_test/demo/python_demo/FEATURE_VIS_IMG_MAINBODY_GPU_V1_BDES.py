#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_MAINBODY_GPU_V1_BDES Demo, 以及压测数据生成的DEMO
Author: wanghui48(wanghui48@baidu.com)
Date: 2022-08-23
Filename: FEATURE_VIS_IMG_MAINBODY_GPU_V1_BDES.py
"""
import requests
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os
from proto import object_detect_pb2
from proto import protobuf_to_dict

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_MAINBODY_GPU_V1_BDES demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        """create protobuf"""
        def _createprotobufdata(imagestr):
            """create protobuf from image"""
            proto_data = object_detect_pb2.ObjectDectectRequest()
            proto_data.image = imagestr
            proto_data.with_face = 1
            data = proto_data.SerializeToString()
            return data

        protodata = _createprotobufdata(data["image"])
        newdata, meta = bdes_encode(protodata)

        request_data = json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(newdata),
        })
        return request_data, meta


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    data = {
        "image": Util.read_file(input_data)
    }
    feature_data, meta = feature_demo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-VIS-ENCRYPT-METAINFO': meta,
        'X-VIS-DATA-ENCRYPTED': 'BDES_BINARY',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_MAINBODY_GPU_V1_BDES',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    res_data = json.loads(res_data)
    result = json.loads(res_data['feature_result']['value'])
    result = base64.b64decode(result['result'])
    print(result)


def bdes_encode(data):
    """
    bdes encode binary mode
    """
    host = "http://10.198.17.24:2020"
    url = host + '/bdes/encode?binary=1'
    res = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    return res.content, res.headers['X-MIPS-BDES-META']

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            "image": Util.read_file(input_dir + '/' + image_file)
        }



if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_MAINBODY_GPU_V1_BDES.py 
    生成压测数据：
        python FEATURE_VIS_IMG_MAINBODY_GPU_V1_BDES.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./images/img_file')  # ./image_dir/img_file 本地图片

