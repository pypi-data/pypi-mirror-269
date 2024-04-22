#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1 Demo, 以及压测数据生成的DEMO
Author:  wuyongjun01
Date: 2020-01-13
Filename: FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1.py
"""

import os
import sys
import json
import base64
import random
import urllib

from util import Util
from xvision_demo import XvisionDemo

from google.protobuf import text_format
from proto.protobuf_to_dict import protobuf_to_dict
from proto.FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1 import common_request_pb2


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1 demo
    """

    def prepare_common_request_param(self, para_file):
        with open(para_file, 'rb') as f:
            req_param_str = f.read()
            req_param = common_request_pb2.CommonRequest()
            text_format.Merge(req_param_str, req_param)
            data = req_param.SerializeToString()

            return data

    def prepare_request(self, img, para_file="./text_dir/ads_full_request.prototxt"):
        """ prepare data for request

        Args:
            img: binary image data
            para_file: parameter config file

        Returns:
            data: json data
        """

        logid = random.randint(1000000, 100000000)

        reqparam = self.prepare_common_request_param(para_file)
        requestinfo = {
            "log_id": logid,
            "image": base64.b64encode(img),
            "param": base64.b64encode(reqparam),
        }

        data = json.dumps(requestinfo)

        return json.dumps({
            'appid': 'xvision_job_name',
            'logid': logid,
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
    para_file = "./text_dir/ads_full_request.prototxt"

    # 生成算子输入
    feature_data = featureDemo.prepare_request(Util.read_file(input_data), para_file)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1',
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
    # parse the output
    json_data = json.loads(res_data)
    if json_data["code"] != 0:
        print "calculator return errors: %s" % json.dumps(json_data, indent=4)
    else:
        data = json.loads(json_data["feature_result"]["value"])
        data = base64.b64decode(data["result"])

        json_data = json.loads(data)
        responses = json_data["Response"]
        for size_name, response in responses.iteritems():
            fail_code = int(response["fail_code"])
            thumb_path = "file_path" + "_" + size_name + ".jpg"
            if fail_code != 0:
                print "Failed to generate thumb for %s with code: %d" % (size_name, fail_code)
            else:
                imgdata = base64.b64decode(response["thumbnail"]["data"])
                # open(thumb_path, "w").write(imgdata)
                print "Succed to generate thumb for %s: %s" % (size_name, thumb_path)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()

    # may need new parameters for each picture.
    para_file = "./text_dir/ads_full_request.prototxt"

    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = Util.read_file(input_dir + '/' + image_file)
        print featureDemo.prepare_request(data, para_file)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_SMARTTAILOR_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/ocr.png')  # ./image_dir/img_file 本地图片
