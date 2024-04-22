#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Brief:FEATURE_VIS_IMG_SAMEFEA_VIT_EXTRACT_A30 Demo, 以及压测数据生成的DEMO
Author: songyuxin02(songyxin02@baidu.com)
Date: 2022-11-07
Filename: FEATURE_VIS_IMG_SAMEFEA_VIT_EXTRACT_A30.py
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
from PIL import Image
import numpy as np
from proto.FEATURE_VIS_IMG_DETECTION_GPU_AIPE import imgfeature_pb2
from proto.FEATURE_VIS_IMG_DETECTION_GPU_AIPE.protobuf_to_dict import protobuf_to_dict

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_SAMEFEA_VIT_EXTRACT_A30 demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
        """
        #pid = '45'
        #dettype = '4'
                     
        proto_data = imgfeature_pb2.FeatureRequest()
        proto_data.image = data['image']
        proto_data.query_sign = '0,0'

        #info_texts = proto_data.info.texts.add()
        ##info_texts.key = 'featureids'
        ##info_texts.value = 'shihuo_obj_1_det'
        #info_texts.key = 'detect'
        #info_texts.value = '1'       
        #
        #info_texts = proto_data.info.texts.add()
        #info_texts.key = 'usedb'
        #info_texts.value = '0' 

        new_data = proto_data.SerializeToString()
        
        logid = random.randint(1000, 10000)
        #logid = random.randint(1000000, 100000000)

        return json.dumps({
                    'appid': '123456',
                    'logid': logid,
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
    imagedata = cv2.imread(input_data)
    ret, imagedata = cv2.imencode('.jpg', imagedata)
    imagedata = Image.fromarray(np.uint8(imagedata)).tobytes()
    
    data = {
                #"image": Util.read_file(input_data)
                "image": imagedata
            }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_SAMEFEA_VIT_EXTRACT_A30',
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
    
    result = feature_result['result'].decode('base64')
    # serialize the result
    
    proto_result = imgfeature_pb2.FeatureResponse()
    proto_result.ParseFromString(result)
    #print proto_result
    res_json = protobuf_to_dict(proto_result)
    
    features = {fea.fea_id:fea.fea_data for fea in proto_result.features}
    
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
        python FEATURE_VIS_IMG_SAMEFEA_VIT_EXTRACT_A30.py
    生成压测数据：
        python FEATURE_VIS_IMG_SAMEFEA_VIT_EXTRACT_A30.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        features = feature_calculate('./image_dir/product_img.jpg') #./image_dir/img_file 本地图片

        #解码特征
        for feaid, feadata in features.items():
            print >> sys.stderr, 'fea id:', feaid, 'fea len:', len(feadata)
    
        print >> 'features keys: ', features.keys()  
        fea0 = np.fromstring(features[0], dtype=np.float32)
        print fea0.shape 