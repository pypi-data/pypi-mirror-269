#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_MOBILE1000_CPU_V1 Demo, 以及压测数据生成的DEMO
Author: zhangbin33(zhangbin33@baidu.com)
Date: 2021-04-02
Filename: FEATURE_VIS_IMG_MOBILE1000_GPU_V1.py
"""
from proto.FEATURE_VIS_IMG_MOBILE1000_GPU_V1 import imgfeature_pb2
from xvision_demo import XvisionDemo
from util import Util
import numpy as np
import json
import base64
import random
import urllib
import sys
import os


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_MOBILE1000_CPU_V1 demo
    """
    def prepare_request(self, imgData):
        """ prepare data for request
        Args:
            conf: conf file
        Returns:
            data: protobuf
        """
        proto_data = imgfeature_pb2.FeatureRequest()
        proto_data.image = imgData
        proto_data.query_sign = '0,0'
        def addinfo(key, value):
            """add info to proto"""
            infoele = proto_data.info.texts.add()
            infoele.key = key
            infoele.value = value
        info = {'featureids': '7'}

        if info is not None:
            for key, value in info.iteritems():
                addinfo(key, value)
        data = proto_data.SerializeToString()
        data = base64.b64encode(data)
        req_json = {
            'appid': '123456',
            'logid': 0,
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': data,
        }

        return json.dumps(req_json)

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
    feature_data = featureDemo.prepare_request(Util.read_file(input_data))

    job_name = ""
    token = ""
    #生成百度视频中台输入
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_MOBILE1000_CPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    #获取url
    #高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_test_url + featureDemo.xvision_sync_path
    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    #请求百度视频中台特征计算服务
    #url = "http://10.155.243.12:35036/GeneralClassifyService/classify"
    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    #打印输出
    res_json = json.loads(res_data)
    result = json.loads(res_json["feature_result"]["value"])
    if result['err_no'] != 0:
        res_data = '%s:%s' % (result['err_no'], result['err_msg'])
    else:
        res_data = result['result'].decode('base64')
        proto_result = imgfeature_pb2.FeatureResponse()
        proto_result.ParseFromString(res_data)
    #feat_value = json.loads(base64.b64decode(value["result"]))
    features = {fea.fea_id: fea.fea_data for fea in proto_result.features}
    for feaname in features:
        if feaname == 7:
            label_score = np.fromstring(features[feaname], np.float32)
            print feaname, label_score
        else:
            print feaname, features[feaname]


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
        python FEATURE_VIS_IMG_MOBILE1000_CPU_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_MOBILE1000_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/tmp.jpg') #./image_dir/img_file 本地图片
