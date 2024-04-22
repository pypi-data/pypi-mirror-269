#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_PLANT_GPU_V9_WP Demo, 以及压测数据生成的DEMO
Author: wuyongjun01(wuyongjun01@baidu.com)
Date: 2019-11-05
Filename: FEATURE_VIS_IMG_PLANT_GPU_V9_WP.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import requests

import numpy as np
import json
import base64
import random
import urllib
import sys
import os
import bdes

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_PLANT_GPU_V9_WP demo  
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
                "value": "8",
            },
            {
                "key": "topn",
                "value": "3",
            },
        ]

        info = {
            "texts": texts,
        }

        data = {
            "query_sign": "xvision",
            "image": base64.b64encode(data["image"]),
            "info": info,
        }
        newdata, meta = bdes_encode(data)
        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(json.dumps(newdata)),
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
        'feature_name': 'FEATURE_VIS_IMG_PLANT_GPU_V9_WP',
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

    top = []
    toptag = []

    res_json = json.loads(res_data)
    value = json.loads(res_json["feature_result"]["value"])
    feat_value = json.loads(base64.b64decode(value["result"]))

    features = {fea["fea_id"]: base64.b64decode(fea["fea_data"]) for fea in feat_value["features"]}
    for feaname in features:
        if feaname == 8:
            label_score_info = np.fromstring(features[feaname], np.float32)
            for i, item in enumerate(label_score_info):
                top = top + [str(item)]
        else:
            tag_info = features[feaname]
            for i, item in enumerate(tag_info.split('|*|')[1:21]):
                toptag = toptag + [item]

    for i in range(len(top)):
        print toptag[i] + ':' + top[i] + ' ',
    print


def bdes_encode(data):
    """ bdes_encode """
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
        print feature_demo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_PLANT_GPU_V9_WP.py 
    生成压测数据：
        python FEATURE_VIS_IMG_PLANT_GPU_V9_WP.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/img_file')  # ./image_dir/img_file 本地图片
