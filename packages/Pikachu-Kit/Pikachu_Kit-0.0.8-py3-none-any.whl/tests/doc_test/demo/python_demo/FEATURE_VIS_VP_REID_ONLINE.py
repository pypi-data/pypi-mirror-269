#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VP_REID_ONLINE Demo, 以及压测数据生成的DEMO
Author: Wu Yongjun(wuyongjun01@baidu.com)
Date: 2020-03-14
Filename: FEATURE_VIS_VP_REID_ONLINE.py
"""

import os
import sys
import json
import base64
import random
import urllib

from util import Util
from xvision_demo import XvisionDemo
#from proto.FEATURE_VIS_VP_REID_ONLINE import reid_paddle_service_pb2, TYPE_CALLABLE_MAP
from proto.FEATURE_VIS_VP_REID_ONLINE import reid_paddle_service_pb2
from proto.protobuf_to_dict import protobuf_to_dict


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VP_REID_ONLINE demo
    """
    def prepare_request(self, imgData):
        """ prepare data for request

        Args:
            conf: conf file

        Returns:
            data: protobuf
        """


        proto_data = reid_paddle_service_pb2.ReidServiceRequest()
        proto_data.image = imgData
        proto_data.info = "test"

        data = proto_data.SerializeToString()

        return json.dumps({
                'appid': 'xvision_job_name',
                'logid': random.randint(1000000, 100000000),
                'format': 'json',
                'from': 'xvision',
                'cmdid': '123',
                'client': '0.0.0.0', 
                'data': base64.b64encode(data)
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
        'feature_name': 'FEATURE_VIS_VP_REID_ONLINE',
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
    res_data = json.loads(res_data)

    if (("code" in res_data)
            and (res_data["code"]==0)
            and ("feature_result" in res_data)
            and ("value" in res_data['feature_result'])):
            res_json=json.loads(res_data['feature_result']['value'])
            # 解pb
            proto_result = reid_paddle_service_pb2.ReidServiceResponse()
            proto_result.ParseFromString(base64.decodestring(res_json['result']))
            res_json['result'] = protobuf_to_dict(proto_result)
            res_data['feature_result']['value'] = res_json

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
        python FEATURE_VIS_VP_REID_ONLINE.py
    生成压测数据：
        python FEATURE_VIS_VP_REID_ONLINE.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/ocr.png')  # ./image_dir/img_file 本地图片
