#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_VDA_SINGLE_GPU Demo, 以及压测数据生成的DEMO
Author: pengmian
Date: 2020-8-31
Filename: FEATURE_VIS_IMG_VDA_SINGLE_GPU.py 
"""
from __future__ import print_function
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
    FEATURE_VIS_IMG_VDA_SINGLE_GPU demo  
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
                'cmd': data['cmd'],              #"check" or "result"
                'step': 5, 
                'case_id': int(data["case_id"]), #非0，int32范围
                'image': base64.b64encode(data["image"]),
                'type_name': "VDA_SINGLE",
                'car_type': "Lavida",
                'crop_type': "middle",
                'user_id': "xiaoming"
                }

        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(json.dumps(new_data)),
                })


def parse_result(res_data):
    """
    功能：解析算子的输出结果
    输入：
        res_data：算子的输出结果
    输出：
        算子输出结果
    """
    if res_data['status'].find('fail') >= 0:
        return res_data
    feature_result = res_data['feature_result']
    service_result = json.loads(feature_result['value']) 
    if service_result['result'] == '':
        return service_result
    res = json.loads(base64.b64decode(service_result['result']))
    return res


def process(image_data, case_id, cmd):
    """
    功能：特征计算
    输入：
        image_data:本地图片文件
        case_id:   每张图片对应一个id，注意不要重复
        cmd:       请求命令：check：发送check请求，check成功才进行后续处理
                             result：发送获取结果的请求
    输出：
        图片特征
    """
    featureDemo = FeatureReq()

    #生成算子输入
    data = {
                "image": image_data,
                "case_id": case_id,
                "cmd": cmd
           }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_VDA_SINGLE_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    #请求百度视频中台特征计算服务
    res_data = featureDemo.request_feat_new(params, feature_data, url, headers)

    return json.loads(res_data)


def feature_calculate(input_dir):
    """
    功能：特征计算
    输入：
        input_dir:本地图片文件夹
    输出：
        图片特征
    """
    if not os.path.exists(input_dir):
        print(input_dir, ' no exist')
        return

    img_file_list = sorted(os.listdir(input_dir))
    for i in range(len(img_file_list)):
        case_id = i + 1
        image_data = Util.read_file(os.path.join(input_dir, img_file_list[i]))

        print('##############################################') 
        print('case_id:', case_id, ' send check command ...')
        res_data = process(image_data, case_id, 'check')
        check_res = parse_result(res_data)
        if not 'description' in check_res or check_res['description'].find('Very good') < 0:
            print(check_res)
            return
        print(check_res['description'])

        print('case_id:', case_id, 'getting result ...')
        result = process(image_data, case_id, 'result')
        cnt = 0
        while cnt < 100 and result['status'].find('fail') >= 0:
            result = process(image_data, case_id, 'result')
            cnt += 1
        print(parse_result(result))


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
    for i in range(len(img_file_list)):
        image_data = Util.read_file(os.path.join(input_dir, img_file_list[i]))
        check_data = {"image": image_data, "case_id": i + 1, "cmd": "check"}
        print(featureDemo.prepare_request(check_data))#压测词表数据-check命令
        
        result_data = {"image": image_data, "case_id": i + 1, "cmd": "result"}
        print(featureDemo.prepare_request(result_data))#压测词表数据-result命令


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_VDA_SINGLE_GPU.py 
    生成压测数据：
        python FEATURE_VIS_IMG_VDA_SINGLE_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./image_dir/FEATURE_VIS_IMG_VDA_SINGLE_GPU') #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        feature_calculate('./image_dir/FEATURE_VIS_IMG_VDA_SINGLE_GPU') #./image_dir/ 本地图片夹
