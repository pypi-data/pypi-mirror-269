#!/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:
@Author: yuanruiting
@Date:   2020-07-21
@Filename: FEATURE_VIS_IMG_GPU_MONODEPTH_ZY.py
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_MONODEPTH_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        feat_args = {}
        feat_args['ext_info'] = json.dumps(data['ext_info'])
        feat_args['img_data'] = base64.b64encode(data['image'])
        new_data = {
             "image": "",#, base64.b64encode(data['image']),
             "feat_args": json.dumps(feat_args)
         }
        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'req': new_data,
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
    #生成算子输入
    data = {
                "image": Util.read_file(input_data["image"]),
                "ext_info": input_data["ext_info"]
            }
    
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_GPU_MONODEPTH_ZY',
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
        input_data:（图片）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir)) #image_dir里边是图片列表，用于生成压测词表
    img_file_list = [img_file for img_file in img_file_list if img_file.endswith(".jpg")]
    for image_file in img_file_list:
        ext_info = {"focal": "1130.4", "height": "1080"}
        data = {
                    "image": Util.read_file(input_dir + '/' + image_file),
                    "ext_info":  ext_info
                }
        print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_GPU_MONODEPTH_ZY.py 
    生成压测数据：
        python FEATURE_VIS_IMG_GPU_MONODEPTH_ZY.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        ext_info = {"focal": "1130.4", "height": "1080"}
        input_data = {
            "image": "./image_dir/FEATURE_VIS_IMG_GPU_MONODEPTH_ZY.jpg",
            "ext_info": ext_info
        }
        feature_calculate(input_data) #./image_dir/img_file 本地图片
        #最终结果需要用base64.b64decode(res_data["res"])解码 再存成图片
