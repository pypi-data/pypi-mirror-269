#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_OCR_GPU_IDCARDS2 Demo, 以及压测数据生成的DEMO
Author: v_tanjinxiang(v_tanjinxiang@baidu.com)
Date: 2019-09-20
Filename: FEATURE_VIS_IMG_OCR_GPU_IDCARDS2.py
"""
import base64
import json
import os
import sys
import random
from util import Util
from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_OCR_GPU_IDCARDS2 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
	"""
        dataTmp = "type=st_ocrapi&appid=10005&clientip=x.x.x.x&fromdevice=pc&version=1.0.0&detecttype=LocateRecognize&encoding=1&recg_type=seq&international=1&languagetype=CHN_ENG&locate_type=v2&imgDirection=setImgDirFlag&object_type=id_card&accuracy_type=high&direction=horizontal&fromproduct=graphtransplugin&is_detect_risk=true&is_detect_rectify=false&image=" + base64.b64encode(data['image'])
        return json.dumps({
            'appid': 'xvision-app',
            'logid': 1234567,
            'from': 'xvision',
            'format': 'json',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(dataTmp)
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
    data = {"image": Util.read_file(input_data)}
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_OCR_GPU_IDCARDS2',
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
        data = {"image": Util.read_file(input_dir + '/' + image_file)}
        print featureDemo.prepare_request(data)  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_OCR_GPU_IDCARDS2.py
    生成压测数据：
        python FEATURE_VIS_IMG_OCR_GPU_IDCARDS2.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/ocr.png')  # ./image_dir/img_file 本地图片

