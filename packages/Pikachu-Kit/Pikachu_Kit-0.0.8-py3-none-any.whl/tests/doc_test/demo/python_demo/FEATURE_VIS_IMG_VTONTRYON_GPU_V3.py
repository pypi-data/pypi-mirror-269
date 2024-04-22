#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_VTONTRYON_GPU_V3 Demo, 以及压测数据生成的DEMO
Author: mamingming(mamingming@baidu.com)
Date: 2020-05-09
Filename: FEATURE_VIS_IMG_VTONTRYON_GPU_V3.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os
import cv2
class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_INPAINTING_GPU_V1 demo
    """
    def prepare_data_single(self, src_path, ref_path):
        """
        功能：构建算子的输入数据
        输入：
            src_path：string，
            ref_path：string，
        输出：
            返回算子的data输入数据
        """
        src = cv2.imread(src_path, 1)
        tmp = cv2.imencode(".jpg", src)[1].tostring()
        src_data = base64.b64encode(tmp).decode()
    
        ref = cv2.imread(ref_path, 1)
        tmp = cv2.imencode(".jpg", ref)[1].tostring()
        ref_data = base64.b64encode(tmp).decode()
        data = "object_type=vtonTryon" + \
               "&action=transfer" + \
               "&reference=" + ref_data.rstrip() + \
               "&source=" + src_data.rstrip()
    
        return data


    def prepare_request(self, src_path, ref_path):
        """
        功能：构建算子的输入数据
        输入：
            src_path：string，
            ref_path：string，
        输出：
            返回算子的输入数据
        """
        logid = random.randint(1000000, 100000000)
        data = self.prepare_data_single(src_path, ref_path)
        req_array = {
                        'appid': '123456',
                        'logid': logid,
                        'format': 'json',
                        'from': 'test-python',
                        'cmdid': '123',
                        'clientip': '0.0.0.0',
                        'data': base64.b64encode(str.encode(data)).decode(),
                    }
        req_json = json.dumps(req_array)
        return req_json
    
def feature_calculate(src_path, ref_path):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(src_path, ref_path)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_VTONTRYON_GPU_V3',
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


def gen_stress_data(src_dir, ref_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    img_src_list = sorted(os.listdir(src_dir)) #image_dir里边是图片列表，用于生成压测词表
    img_ref_list = sorted(os.listdir(ref_dir)) #image_dir里边是图片列表，用于生成压测词表
    for i in range(min(len(img_src_list), len(img_ref_list))):
        print featureDemo.prepare_request(img_src_list[i], img_ref_list[i])#压测词表数据

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_INPAINTING_GPU_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_INPAINTING_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/FEATURE_VIS_IMG_VTONTRYON_GPU_V3/src/', 
                './image_dir/FEATURE_VIS_IMG_VTONTRYON_GPU_V3/ref/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/FEATURE_VIS_IMG_VTONTRYON_GPU_V3/src/vton_srf5.jpg', 
                './image_dir/FEATURE_VIS_IMG_VTONTRYON_GPU_V3/ref/vton_ref4.jpg') #./image_dir/img_file 本地图片
