#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU Demo, 以及压测数据生成的DEMO
Author: weixiang01(weixiang01@baidu.com)
Date: 2020-12-14
Filename: FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os

from proto.FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU import imgfeature_pb2
from proto.FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU.protobuf_to_dict import protobuf_to_dict


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
        """
        pid = '45'
        dettype = '4'
                     
        proto_data = imgfeature_pb2.FeatureRequest()
        proto_data.image = data['image']
        proto_data.query_sign = '123,321'
        info_texts = proto_data.info.texts.add()
        info_texts.key = 'searchsource'
        info_texts.value = pid
        info_texts = proto_data.info.texts.add()
        info_texts.key = 'dettype'
        info_texts.value = dettype
        new_data = proto_data.SerializeToString()

        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(new_data),
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
        'feature_name': 'FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU',
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
    res_data = json.loads(res_data.encode('utf-8'))
   
    feature_result = json.loads(res_data['feature_result']['value'].encode('utf-8'))
    
    # error information
    if feature_result['err_no'] != 0:
        print("err_no : %d, err_msg: %s" % (feature_result['err_no'], feature_result['err_msg']))
        return
    
    result = base64.b64decode(feature_result['result'])
    
    # serialize the result
    proto_result = imgfeature_pb2.FeatureResponse()
    proto_result.ParseFromString(result)
    res_json = protobuf_to_dict(proto_result)
    
    features = {fea.fea_id:fea.fea_data for fea in proto_result.features}
    #print features

    return features


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
        print featureDemo.prepare_request(data) #压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU.py 
    生成压测数据：
        python FEATURE_VIS_IMG_IMAGE_TEXT_FEATURE_EXTRACT_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/baoziji.jpg') #./image_dir/img_file 本地图片
