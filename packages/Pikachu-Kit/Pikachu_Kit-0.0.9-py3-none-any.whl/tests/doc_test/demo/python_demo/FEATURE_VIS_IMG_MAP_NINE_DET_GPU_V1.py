#!/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:
@Author: zhangweiming
@Date:   2023-4-11
@Filename: FEATURE_VIS_IMG_MAP_NINE_DET_GPU_V1.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import sys
import os
import random
import commands
class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_LKCLS_GPU_V1 demo
    """
    def prepare_img_data(self, img_name):
        """ prepare img_data for request

        Args:
            conf: conf file

        Returns:
            img_data: data read from file
        """
        with open(img_name, "rb") as f:
            img_data = f.read()
        #img_data = util.read_file(img_name, 'rb')

        return img_data

    def prepare_request(self, img_name):
        """ prepare data for request

        Args:
            conf: conf file

        Returns:
            data: protobuf
        """
        img_data = self.prepare_img_data(img_name)
        data = {
                'image': base64.b64encode(img_data),
                }

        return json.dumps(data)


def prepare_data(data): 
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输出数据
        """
        req_data = {
            "appid": "xvision_job_name",  # 填写视频中台的作业名, 方便排查问题
            "logid": random.randint(1000000, 100000000),
            "format": "json",
            "from": "xvision",
            "cmdid": "123",
            "clientip": commands.getoutput("hostname"),  # 请求 IP, 用户发送请求的 IP 地址, 方便排查问题
            "data": base64.b64encode(data)
        }
        #print(data)
        return json.dumps(req_data)


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
    # data = {
    #     "img": Util.read_file(input_data['img']),
    #     "name": "20200418241165ra00000141"
    # }
    feature_req = featureDemo.prepare_request(input_data)
    feature_data = prepare_data(feature_req)
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': '4e6a4805-f515-5839-8b54-db1d262e5543',  
        'business_name': 'STRESSJOBFEATURE_VIS_IMG_MAP_NINE_DET_GPU_V1', 
        'feature_name': 'FEATURE_VIS_IMG_MAP_NINE_DET_GPU_V1',
        #'auth_key': '040963ac-cbc9-5edb-9e95-09c0dca79638',  #"afab6a9e-ec63-5e4d-90a3-4afb306eb446",
        #'business_name': 'MAP_LUKUANG_CLS', #"STRESSJOBFEATURE_VIS_IMG_LKCLS_GPU_V4", #job_name,
        #'feature_name': 'FEATURE_VIS_IMG_LKCLS_GPU_V4',
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
    # featureDemo.parse_result(res_data)
    # 打印输出
    # print('===res', base64.b64decode(json.loads(json.loads(res_data)['feature_result']['value'])['result']))
    
def gen_stress_data(input_data):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_data['img']))  # img_dir里边是图片列表，用于生成压测词表
    with open('img_file', 'a') as f:
        for i in xrange(len(img_file_list)):
            data = {
                "name": img_file_list[i].split(".")[0],
                "img": Util.read_file(input_data['img'] + '/' + img_file_list[i]),
            }
            f.write(featureDemo.prepare_request(data))
            f.write('\n')
if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_LKCLS_GPU_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_LKCLS_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        input_data = {
            'img': 'stress_image/',
        }
        gen_stress_data(input_data)
    else:
        file_path = sys.argv[1]
        print(file_path)    
        feature_calculate(file_path)        
