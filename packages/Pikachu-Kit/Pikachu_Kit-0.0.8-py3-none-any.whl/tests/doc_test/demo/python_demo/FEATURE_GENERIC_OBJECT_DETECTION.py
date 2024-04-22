#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_GENERIC_OBJECT_DETECTION Demo, 以及压测数据生成的DEMO
Author: wuyongjun01(wuyongjun01@baidu.com)
Date: 2019-12-22
Filename: FEATURE_GENERIC_OBJECT_DETECTION.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os

from proto.protobuf_to_dict import protobuf_to_dict
from proto.FEATURE_GENERIC_OBJECT_DETECTION import imgfeature_pb2


class FeatureReq(XvisionDemo):
    """
    FEATURE_GENERIC_OBJECT_DETECTION demo  
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        texts = [
            {
                "key": "featureids",
                "value": "codfv",
            },
        ]

        info = {
            "texts": texts,
        }

        new_data = {
            "query_sign": "xvision",
            "image": base64.b64encode(data["image"]),
            "info": info,
        }

        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(json.dumps(new_data)),
        })

    def parse_response(self, res):
        try:
            res_json = json.loads(res)
            if res_json.get("code", -1) != 0:
                print res_json.get("status", "unknown error.")
                return

            cal_str = res_json.get("feature_result", {}).get("value", None)
            if not cal_str:
                print "failed to get feature result."
                return

            cal_json = json.loads(cal_str)
            if cal_json.get("err_no", -1) != 0:
                print cal_json.get("err_msg", "unknown error.")
                return

            cal_data = base64.b64decode(cal_json.get("result", ""))

            final_json = json.loads(cal_data)
            final_result = {
                "feature": [],
            }

            for key, values in final_json.items():
                if key == "features":
                    new_items = {}
                    for feature in values:
                        new_items["fea_id"] = feature["fea_id"]

                        proto_result = imgfeature_pb2.LogoFeature()
                        fea_data = base64.b64decode(feature.get("fea_data", ""))

                        proto_result.ParseFromString(fea_data)
                        new_items["fea_data"] = protobuf_to_dict(proto_result)

                    final_result["feature"].append(new_items)
                else:
                    final_result[key] = values
            print final_result
        except Exception as ex:
            print "Failed to parse response: " + str(ex)
            return


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

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_GENERIC_OBJECT_DETECTION',
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
    feature_demo.parse_result(res_data)
    feature_demo.parse_response(res_data)


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
        python FEATURE_GENERIC_OBJECT_DETECTION.py 
    生成压测数据：
        python FEATURE_GENERIC_OBJECT_DETECTION.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/img_file')  # ./image_dir/img_file 本地图片
