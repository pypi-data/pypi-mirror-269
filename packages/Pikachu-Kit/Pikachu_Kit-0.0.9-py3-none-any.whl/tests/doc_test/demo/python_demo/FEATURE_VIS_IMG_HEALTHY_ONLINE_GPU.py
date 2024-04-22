#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_IMG_HEALTHY_ONLINE_GPU.py.py Demo, 以及压测数据生成的DEMO
Author: chenkehua(weixiang01@baidu.com)
Date: 2022.8.1
Filename: FEATURE_VIS_IMG_HEALTHY_ONLINE_GPU.py.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import sys
import os
import random




class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_HEALTHY_ONLINE_GPU
    """
    def prepare_request(self, frames, title, category):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        querycontsign = '123,321'
        query_template = {
            'appid': '123456',
            "format": "json",
            "from": "test-python",
            'query_sign': querycontsign,
            'logid': 12345789,
            'frames': frames,
            'max_frame': 20,
            'batch_size': 4,
            'max_object': 4,
            'title': title,
            'category': category,
            #'authen': json.dumps([{'appid': 'xxx', 'ak': 'xxx', 'sk': 'xxx'}]), # 申请的VMS appid
            'authen': json.dumps([{'appid': 'xxx', 'ak': 'xxx', 'sk': 'xxx',
                    'appid_ocr':'xxx', 'ak_ocr':'xxx', 'sk_ocr':'xxx'}]),
        }

        jdata = json.dumps(query_template)
        return jdata


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
    frames = [] 
    file_names = os.listdir(input_data)
    for file_name in file_names:
        file_path = os.path.join(input_data, file_name)
        image = open(file_path).read()
        query_img = base64.b64encode(image)
        frame_id = int(file_name.split('.')[0])
        frame = {
            'frame_data': query_img,
            'frame_id': frame_id,
        }
        frames.append(frame)
    frames = json.dumps(frames)
    title = ''
    category = ''
    feature_data = featureDemo.prepare_request(frames, title, category)
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test_healthy',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_HEALTHY_ONLINE_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path
    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if featureDemo.xvision_test_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}
    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_HEALTHY_ONLINE_GPU.py
    """
    # 特征计算Demo
    feature_calculate('./baijiahao_video_frames')  # ./image_dir/img_file 本地图片
