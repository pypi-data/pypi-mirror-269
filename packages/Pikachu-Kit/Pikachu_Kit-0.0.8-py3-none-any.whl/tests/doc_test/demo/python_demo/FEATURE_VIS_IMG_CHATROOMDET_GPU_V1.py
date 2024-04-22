#!/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:
@Author: yejin03
@Date:   2022-01-24
@Filename: FEATURE_VIS_IMG_CHATROOMDET_GPU_V1.py
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
    FEATURE_VIS_IMG_CHATROOMDET_GPU_V1 demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子输入数据的data字段部分
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子data字段值
        """
        req_json = {
            "image_id": 1,
            'image': base64.b64encode(data['img']),  # 图片的base64编码
            "speed": 100.0,
            "latitude": 39.1,
            "longtitude": 266.5,
            "pic_time": 1606536000
            # 'image': base64.b64encode(data['img']),  # 图片的base64编码
        }
        return json.dumps(req_json)

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
        print(data)
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
    data = {
        "img": Util.read_file(input_data),
        "name": "20200418241165ra00000141"
    }
    feature_req = featureDemo.prepare_request(data)
    feature_data = prepare_data(feature_req)
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': '',
        'business_name': '',
        'feature_name': '',
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
    # print("res_data ", res_data)
    # import pdb; pdb.set_trace()
    # 打印输出
    featureDemo.parse_result(res_data)

    result = json.loads(res_data)['feature_result']['value']
    det_res = base64.b64decode(json.loads(result)['result'])
    print (det_res)

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
    img_file_list = sorted(os.listdir(input_data))  # img_dir里边是图片列表，用于生成压测词表
    with open('img_file', 'a') as f:
        for i in xrange(len(img_file_list)):
            data = {
                "name": img_file_list[i].split(".")[0],
                "img": Util.read_file(input_data + '/' + img_file_list[i]),
            }
            f.write(featureDemo.prepare_request(data))
            f.write('\n')
if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_CHATROOMDET_GPU_V1.py
    生成压测数据：
        python FEATURE_VIS_IMG_CHATROOMDET_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        input_data = 'stress_image/'
        gen_stress_data(input_data)
    else:
        input_data = sys.argv[1]
        print(input_data)    
        feature_calculate(input_data)
