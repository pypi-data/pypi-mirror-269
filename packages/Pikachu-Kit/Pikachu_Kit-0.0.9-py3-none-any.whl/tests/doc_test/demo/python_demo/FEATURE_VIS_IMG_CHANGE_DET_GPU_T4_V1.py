#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1 Demo, 以及压测数据生成的DEMO
Author: v_chenhaonan01@baidu.com
Date: 2022-08-04
Filename: FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'data': base64.b64encode(json.dumps(data)),
        })


def infer_mode_req(imagefilename1, imagefilename2):
    """
    infer_mode_req
    """
    imagedata1 = open(imagefilename1, 'rb').read()
    img1 = base64.b64encode(imagedata1)
    imagedata2 = open(imagefilename2, 'rb').read()
    img2 = base64.b64encode(imagedata2)
    dir_name, full_file_name = os.path.split(imagefilename1)
    print(full_file_name)
    input_json = {
        "log_id": full_file_name,
        "image_inputs": [
            {
                "image": img1, #图片
            },
            {
                "image": img2, #图片
            }
        ],
    }
    return input_json


def feature_calculate(imagefilename1, imagefilename2):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    input_json = infer_mode_req(imagefilename1, imagefilename2)
    # data = {
    #     "image_arr":[Util.read_file(imagefilename1), Util.read_file(imagefilename2)]
    # }
    feature_data = feature_demo.prepare_request(input_json)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1',
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
    # feature_demo.parse_result(res_data)
    print
    res_data.encode("utf-8")
    result = json.loads(json.loads(res_data.encode("utf-8"))['feature_result']['value'])['result']
    print(json.loads(base64.b64decode(result).decode('utf-8')))


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
    img_file_list = sorted(os.listdir(input_dir))  # input_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            "image": Util.read_file(input_dir + '/' + image_file)
        }
        print
        feature_demo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1.py GEN_STRESS_DATA
    """
    base_dir = './image_dir/FEATURE_VIS_IMG_CHANGE_DET_GPU_T4_V1/'
    path1 = base_dir + 'images1'
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        for dirpath, dirnames, filenames in os.walk(path1):
            for filename in filenames:
                dir1 = base_dir + 'images1/' + filename
                dir2 = base_dir + 'images2/' + filename
                feature_calculate(dir1, dir2)  # ./image_dir/img_file 本地图片
                break
            break