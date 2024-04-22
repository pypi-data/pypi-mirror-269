#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Author: yangshuguang
Date: 2022-06-08
Description: 网盘文档去水印GPU版, 无bdes加解密
"""

import os
import sys

import json
import base64
import random
import requests
import urllib

from xvision_demo import XvisionDemo
from util import Util


class FeatureReq(XvisionDemo):
    """
    FEATURE_NETDISK_IMG_DOCDEWATERMARK_GPU_V1 demo  
    """
    
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        
        logid = random.randint(1000000, 100000000)
        
        data = {
            "image_buffer": base64.b64encode(data['image']),
            "filter_type": 1
        }

        req_array = {
            'appid': '123456',
            'logid': logid,
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '127.0.0.1',
            'data': base64.b64encode(data),
        }

        return json.dumps(req_array)
    
    def parse_result(self, res_data):
        """
        功能：解析算子的输出结果
        输入：
            res_data：算子的输出结果
        输出：
            算子输出结果
        """
        res_json = {}
        try:
            res_json = json.loads(res_data)
        except Exception as e:
            print 'response json format or content error:{}'.format(e)
            return
        
        if res_json['err_no'] == 0:
            result = base64.b64decode(res_json['result'])
            if "image_buffer" in result:
                image_buffer = base64.b64decode(result["image_buffer"])
                with open("result_img.jpg", "wb") as fid:
                    fid.write(image_buffer)
        else:
            print "err_no = %d, err_msg = %s" % (res_json['err_no'], res_json['err_msg'])


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: 本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
        'image': Util.read_file(input_data)
    }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NETDISK_IMG_DOCDEWATERMARK_GPU_V1',
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
    img_file_list = sorted(os.listdir(input_dir)) #input_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            'image': Util.read_file(os.path.join(input_dir, image_file))
        }
        print featureDemo.prepare_request(data)#压测词表数据

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NETDISK_IMG_DOCDEWATERMARK_GPU_V1.py 
    生成压测数据：
        python FEATURE_NETDISK_IMG_DOCDEWATERMARK_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('/path/to/image/dir')
    else:
        # 特征计算Demo
        feature_calculate('img.jpg')
