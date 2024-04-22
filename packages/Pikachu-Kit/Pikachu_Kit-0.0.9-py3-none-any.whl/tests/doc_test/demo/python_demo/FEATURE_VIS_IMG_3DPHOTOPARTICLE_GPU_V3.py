#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_IMG_3DPHOTOPARTICLE_GPU_V3 Demo, 以及压测数据生成的DEMO
Author: yuanweihang(yuanweihang@baidu.com)
Date: 2023-01-10
Filename: FEATURE_VIS_IMG_3DPHOTOPARTICLE_GPU_V3.py
"""
from xvision_demo import XvisionDemo
from util import Util
import random
import base64
import urllib
import sys
import os
import json

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_3DPHOTOPARTICLE_GPU_V3 demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_data = {
            'image': base64.b64encode(data['image']),
            'type_name': 'inpainting3d',
            'traj_type': 0, #[0,1,2,3,4,5,6]
            'strength': 1.0, # 0.5~1.5
            'duration': 3,
            'front_blur': 0, #[0, 1]
            'particle_idx': 0, #[0,1,2,3,4,5,6,7,8]
            'particle_w': 0.5, # 0.0~1.0
            'particle_h': 0.5, # 0.0~1.0
            'use_url': 1, #[0, 1]
        }
        req_data = json.dumps(req_data)
        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'from': 'xvision',
                    'cmdid': '123',
                    'format': 'json',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(req_data),
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
        "image": Util.read_file(input_data)
    }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_3DPHOTOPARTICLE_GPU_V3',
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
    result = json.loads(res_data)
    result_str = result['feature_result']['value'] #['result']
    result = json.loads(result_str) 
    print(result['err_no'])
    result = result['result'] #['value']['result']
    result = json.loads(result)   
    video_url = result['video_url']
    is_valid = result['valid']
    # file_name = os.path.basename(input_data)
    # with open(os.path.join(file_name + '.mp4'), 'wb') as f:
    #     f.write(video_data)

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_dir:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir)) #image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            "image": Util.read_file(input_dir + '/' + image_file)
        }
        print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_3DPHOTOPARTICLE_GPU_V3.py
    生成压测数据：
        python FEATURE_VIS_IMG_3DPHOTOPARTICLE_GPU_V3.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/FEATURE_VIS_IMG_3DPHOTO_GPU_V2.jpg') #./image_dir/img_file 本地图片