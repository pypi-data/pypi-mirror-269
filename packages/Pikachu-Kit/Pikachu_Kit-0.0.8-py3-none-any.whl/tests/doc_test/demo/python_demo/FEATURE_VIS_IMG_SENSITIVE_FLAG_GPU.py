#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_SENSITIVE_FLAG_GPU Demo, 以及压测数据生成的DEMO
Author: wenyiming(wenyiming@baidu.com)
Date: 2021-02-03
Filename: FEATURE_VIS_IMG_SENSITIVE_FLAG_GPU.py
"""

from xvision_demo import XvisionDemo
from proto.FEATURE_VIS_IMG_WATERMARKREC_GPU_V2_AIPE import imgfeature_pb2
from proto.protobuf_to_dict import protobuf_to_dict
from util import Util
import json
import base64
import urllib
import sys
import os
import random
import commands

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_SENSITIVE_FLAG_GPU demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据 V4
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
        """
        def _pack(image, info):
            """create protobuf from image and info"""
            proto_data = imgfeature_pb2.FeatureRequest()
            proto_data.image = image

            def addinfo(key, value):
               """add info to proto"""
               infoele = proto_data.info.texts.add()
               infoele.key = key
               infoele.value = value

            if info is not None:
                for key, value in info.iteritems():
                   addinfo(key, value)
            data = proto_data.SerializeToString()
            return data

        feaids='14'
        params = {'featureids': feaids}
        protodata = base64.b64encode(_pack(data["image"], params))

        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': protodata,
                })

    def parse_result(self, res_data):
        """
        功能：解析算子的输出结果
        输入：
            res_data：算子的输出结果
        输出：
            算子输出结果
        """
        res_json = json.loads(res_data)
        res = res_json['feature_result']['value']
        res = json.loads(res)['result']
        proto_data = imgfeature_pb2.FeatureResponse()
        proto_data.ParseFromString(base64.decodestring(res))
        print protobuf_to_dict(proto_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
                "image": Util.read_file(input_data)
            }
    #feature_data = featureDemo.prepare_request_v3(data)
    feature_data = featureDemo.prepare_request(data)
    #生成百度视频中台输入

    job_name = ""
    token = ""

    xvision_data = featureDemo.gen_xvision_data({
            'business_name': job_name,
            'resource_key': 'test.jpg',
            'auth_key': token,
            'feature_name': 'FEATURE_VIS_IMG_SENSITIVE_FLAG_GPU',#算子名
            'feature_input_data': feature_data
        })
    #获取url
    #高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": xvision_data["business_name"],
            "feature_name": xvision_data["feature_name"]
        }
    else:
        params = {}

    #请求百度视频中台特征计算服务
    res_data = featureDemo.request_feat(params, xvision_data, url)
    #打印输出
    print(res_data.encode("utf-8"))
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
    img_file_list = sorted(os.listdir(input_dir)) #image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
                    "image": Util.read_file(input_dir + '/' + image_file)
                }
        print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_SENSITIVE_FLAG_GPU.py
    生成压测数据：
        python FEATURE_VIS_IMG_SENSITIVE_FLAG_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/img_file') #./image_dir/img_file 本地图片

