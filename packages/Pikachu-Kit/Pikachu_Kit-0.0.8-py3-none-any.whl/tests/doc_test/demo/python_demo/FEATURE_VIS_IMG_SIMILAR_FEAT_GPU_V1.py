# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_SIMILAR_FEAT_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: gongzhenting(gongzhenting@baidu.com)
Date: 2019-08-22
Filename: FEATURE_VIS_IMG_SIMILAR_FEAT_GPU_V1.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import os
from proto import imgfeature_pb2
import numpy as np


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_SIMILAR_FEAT_GPU_V1 demo  
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """

        new_data = {
            "image": base64.b64encode(data['image']),
            # all below items are optional.
            "info": "demo info",
            "featname": "",
            "topk": 3,
            "filter_thr": 0.95,
        }

        req_data = {
            "appid": "123456",
            "logid": 1,
            "format": "json",
            "from": "test-python",
            "cmdid": "123",
            "clientip": "clientip",
            "data": base64.b64encode(json.dumps(new_data))
        }
        return json.dumps(req_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_SIMILAR_FEAT_GPU_V1',
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

    def _createprotobufdata(imagestr, info):
        """create protobuf from image and info"""
        proto_data = imgfeature_pb2.FeatureRequest()
        proto_data.image = imagestr
        proto_data.query_sign = '0,0'

        def addinfo(key, value):
            """add info to proto"""
            infoele = proto_data.info.texts.add()
            infoele.key = key
            infoele.value = value

        if info is not None:
            for key, value in info.iteritems():
                addinfo(key, value)
        data = proto_data.SerializeToString()
        return data
    
    infos = {"featureids": "1164,1132,1108"}
    imagedata = Util.read_file(input_data)
    protodata = _createprotobufdata(imagedata, infos)
    protodata = base64.b64encode(protodata)
    req_json = {
        'appid': '123456',
        'logid': 123456,
        'format': 'json',
        'from': 'test-python',
        'cmdid': '123',
        'clientip': '0.0.0.0',
        'data': protodata,
    }
    # conn = urllib2.urlopen(serverurl, data=json.dumps(req_json))
    res_data = feature_demo.request_feat_new(params, json.dumps(req_json), url, headers)
    print("xvision's res_data:", res_data)

    ### 解析输出     
    # 1.1164号特征是600个通用聚类中心 
    # 2.1132特征号特征是256维度float类型的通用相似特征
    # 3.1108号特征是1132号特征的量化的char类型特征
    # print("===== parse_result xvision's res_data:")
    # print parse_result(res_data)

def parse_result(res_data):
    """
    功能：解析算子的输出结果
    输入：
        res_data：算子的输出结果
    输出：
        算子输出结果
    """
    res_data = json.loads(res_data)
    if res_data['status'].find('fail') >= 0:
        return res_data
    feature_result = res_data['feature_result']
    service_result = json.loads(feature_result['value']) 
    if service_result['result'] == '':
        return service_result
    res_data = base64.b64decode(service_result['result'])
    proto_result = imgfeature_pb2.FeatureResponse()
    proto_result.ParseFromString(res_data)
    features = {fea.fea_id: fea.fea_data for fea in proto_result.features}
    print("features:", features)
    feature_1164 = np.fromstring(features[1164], dtype=np.int32)
    feature_1132 = np.fromstring(features[1132], dtype=np.float32)
    feature_1108 = np.fromstring(features[1108], dtype=np.uint8)
    print("feature_1164.shape:", feature_1164.shape)
    print("feature_1132.shape:", feature_1132.shape)
    print("feature_1108.shape:", feature_1108.shape)
    features['width'] = proto_result.width
    features['height'] = proto_result.height
    return features

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    f = open("img_file", 'a')
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            "image": Util.read_file(input_dir + '/' + image_file)
        }
        f.write(feature_demo.prepare_request(data))
        f.write('\n')
        # print feature_demo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_DISH_GPU_V1.py 
    生成压测数据：
        python FEATURE_VIS_IMG_DISH_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/places2items_tiananmen_1.jpeg')  # ./image_dir/img_file 本地图片
