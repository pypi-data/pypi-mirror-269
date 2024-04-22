#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_CLIP_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: yangmin09(yangmin09@baidu.com)
Date: 2022-05-12
Filename:FEATURE_VIS_IMAGE_FP_S_DELF_GPU_V1.py 
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import sys
import os
import numpy as np
import random
from proto.FEATURE_VIS_VIDEO_CLIP_GPU_V1 import imgfeature_pb2
from proto.FEATURE_VIS_VIDEO_CLIP_GPU_V1.protobuf_to_dict import protobuf_to_dict


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_CLIP_GPU_V1 demo
    """
               
    def prepare_request(self, data):
        """create protobuf"""
        def _createprotobufdata(imagestr, info):
            """create protobuf from image and info"""
            proto_data = imgfeature_pb2.FeatureRequest()
            proto_data.image = imagestr
            proto_data.query_sign = '0,0'

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
        params = {"detect": "2"}
        protodata = _createprotobufdata(data["image"], params)

        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-proto',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(protodata),
        })


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

    feature_data = feature_demo.prepare_request(data)

    job_name = ""  # 替换为申请的作业名
    token = ""  # 替换为申请作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_FP_S_DELF_GPU_V1',
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
    # 打印输出
    res_data = json.loads(res_data)
    if (("code" in res_data)
            and (res_data["code"] == 0)
            and ("feature_result" in res_data)
            and ("value" in res_data['feature_result'])):
        res_json = json.loads(res_data['feature_result']['value'])
        # 解pb
        proto_result = imgfeature_pb2.FeatureResponse()
        proto_result.ParseFromString(base64.decodestring(res_json['result']))
        res_json['result'] = protobuf_to_dict(proto_result)
        feature_data = res_json['result']

        res_data['feature_result']['value'] = res_json
    # 打印输出
    feature_demo.parse_result(json.dumps(res_data))
    # 解析输出
    features = {fea.fea_id: fea.fea_data for fea in proto_result.features}
    feat = np.fromstring(features[0], dtype=np.float32)
    print (0, "recall feature len and dim: ", len(feat), feat.shape)
    delf = features[3]
    print (3, "samedelf feature len: ", len(delf))


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
        print feature_demo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_CLIP_GPU_V1.py 
    生成压测数据：
        python FEATURE_VIS_VIDEO_CLIP_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/img_file')  # ./image_dir/img_file 本地图片
