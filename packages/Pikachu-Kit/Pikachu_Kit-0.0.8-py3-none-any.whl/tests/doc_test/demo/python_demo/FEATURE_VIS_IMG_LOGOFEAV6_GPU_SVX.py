#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_LOGOFEAV6_GPU_SVX Demo, 以及压测数据生成的DEMO
Author: Wang Hui(wanghui48@baidu.com)
Date: 2022-06-29
Filename: FEATURE_VIS_IMG_LOGOFEAV6_GPU_SVX.py
"""

import os
import sys
import json
import base64
import random
import urllib

from util import Util
from xvision_demo import XvisionDemo

sys.path.append("./proto/FEATURE_VIS_IMG_LOGOFEAV6")
import vue_proto_pb2
import vue_common_pb2


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_LOGOFEAV6_GPU_SVX demo
    """
   
    def prepare_request(self, image):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_pb = vue_proto_pb2.FeatureRequest()
        req_pb.query_sign = "query_sign_id"
        req_pb.image = image
        data = req_pb.SerializeToString()
        
        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',    #必须
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(data),   #必须
                })
     
    def parse_result(self, res_data):
        """ parse_result
        """
        # 打印输出
        res_json = json.loads(res_data)
        feat_res_str = res_json["feature_result"]["value"]
        feat_res = json.loads(feat_res_str)
        result_str = base64.b64decode(feat_res["result"])
        res_pb = vue_proto_pb2.FeatureResponse()
        res_pb.ParseFromString(result_str)
        print(res_pb)
        

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
    image = Util.read_file(input_data),
    feature_data = featureDemo.prepare_request(Util.read_file(input_data))

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_LOGOFEAV6_GPU_SVX',
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

    #print(url, headers, params, feature_data)
    print(url, headers, params)
    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)
    print("res_data", res_data)
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
        data = Util.read_file(input_dir + '/' + image_file)
        print (featureDemo.prepare_request(data))  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_LOGOFEAV6_GPU_SVX.py
    生成压测数据：
        python FEATURE_VIS_IMG_LOGOFEAV6_GPU_SVX.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        #feature_calculate('./image_dir/test.jpg')  # 本地图片
        feature_calculate('./image_dir/logo_starbucks.jpg')  # 本地图片
 
