#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_SUPER_RESOLUTION_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: work(work@baidu.com)
Date: 2019-08-22
Filename: FEATURE_VIS_IMG_SUPER_RESOLUTION_GPU_V1.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import util
import json
import base64
import random
import sys
import os
import time

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_SUPER_RESOLUTION_GPU_V1 demo  
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
            "appid": "123456",
            "logid": "logid",
            "format": "json",
            "from": "test-python",
            "cmdid": "123",
            "clientip": "clientip",
            "data": base64.b64encode(data)
        }
        return json.dumps(req_data)

def prepare_img_data(input_path):
    """ prepare img_data for request

    Args:
        conf: conf file
        input_path: path

    Returns:
        img_data: data read from file
    """

    img_data = util.read_file(input_path, 'rb')
    print(len(img_data))
    return img_data

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
    # data = {
    #             "image": base64.b64encode(Util.read_file(input_data)), 
    #             "type_name": "image_restoration",
    #             "option": "super_resolution"
    #         }
    img_data = prepare_img_data(input_data)
    # param = {'input_shadows':125,"input_highlights":255,"midtones":1.0,"output_shadows":0,"output_highlights":255}
    # param = base64.b64encode(param)
    print(len(base64.b64encode(img_data)))
    data = {'image': base64.b64encode(img_data), 
                    'operate': {'brightness': 70, "contrast": 20}}
    feature_data = featureDemo.prepare_request(json.dumps(data))

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_CPU_AIPE_BANCAI_V1',
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
    print(len(feature_data))
    start = time.time()
    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    # featureDemo.parse_result(res_data)
    res_data_json = json.loads(res_data)
    print(res_data_json['feature_result']['calc_time_ms'])
    end = time.time()
    print(end - start)
    res_json = json.loads(res_data_json[u'feature_result'][u'value'])
    res_json = json.loads(base64.b64decode(res_json[u'result']))
    image_data = base64.b64decode(res_json['image'])

    with open(os.path.join("test.jpg"), 'wb') as f:
        f.write(image_data)
    # # print(type(image_data))
    # # print(base64res_data)

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
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
        python FEATURE_VIS_IMG_SUPER_RESOLUTION_GPU_V1.py 
    生成压测数据：
        python FEATURE_VIS_IMG_SUPER_RESOLUTION_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/wangpan.jpg') #./image_dir/img_file 本地图片
        
