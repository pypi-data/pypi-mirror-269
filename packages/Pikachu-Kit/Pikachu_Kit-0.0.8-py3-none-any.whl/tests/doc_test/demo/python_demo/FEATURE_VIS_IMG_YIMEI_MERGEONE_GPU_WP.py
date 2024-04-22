#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2022-01-25
Filename: FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os
import uuid
import time
import requests
import hashlib

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP demo
    ai修图-特效医美-黑头皱纹合并
    """
    def prepare_request(self, images):
        """
        功能：构建算子的输入数据
        输入：
            images:
                image: 图片base64
                imageid: 唯一ID
        输出：
            返回算子的输入数据
        """
        # 参数input
        input = {
            "logid": "123",  # 必须，string，最好唯一，方便排查问题
            "format": "json",
            "model_version": "2.0",
            "imagesnum": len(images),
            "images": images,
            "targetfacenum": 1,  # 可选，int，每张图期望保留的人脸数，不传默认为1
            "scene_type": 0,  # 生活照场景
            "face_sort_type": 0,  # 人脸排序模式：默认值0，按人脸框面积排序；设为1代表使用近图像中心点策略
            "image_type": -1  # 人脸检测模型：公有云模型
        }

        # 参数外层
        params = {
            "provider": "get_feature",
            "input": json.dumps(input)
        }
        return params


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: [{'image': '', 'imageid': ''}]
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)
    # BDES加密：对input部分进行加密
    def encrypt(params):
        """
        功能：bdes加密函数
        输入：
            params：dict类型，算子需要的参数
        输出：
            加密参数返回，cipher_text，meta_info
        """
        # 业务自己实现BDES加密
        return {
            "cipher_text": "",
            "meta_info": ""
        }
    encrypt_res = encrypt(feature_data.get("input"))
    request_params = {
        "provider": "get_feature",
        "input": encrypt_res.get("cipher_text"),
    }

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = 'FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP'

    # 异步任务url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path
    params = {
        "business_name": job_name,
        "feature_name": feature_name,
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X_BD_LOGID': str(random.randint(1000000, 100000000)),
        'X-VIS-DATA-ENCRYPTED': 'BDES',
        'X-VIS-ENCRYPT-METAINFO': encrypt_res.get("meta_info"),
        'X-VIS-RESPONSE-ENCRYPTED': 'BDES',
    }
    data = json.dumps({
        "business_name": job_name,
        "resource_key": 'test',
        "auth_key": token,
        "feature_name": feature_name,
        "data": base64.b64encode(json.dumps(request_params).encode()).decode('utf-8'),
    })

    res_data = featureDemo.request_feat_new(params, data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)
    # callback 返回结果，带加密
    # {
    #   'source_key': '', 
    #   'status': 'Succeeded.', 
    #   'code': 0, 
    #   'logid': 8962231798, 
    #   'feature_result': {
    #       'feature': 'FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP', 
    #       'value': '{
    #           "metainfo": "BAkAAAAAAAA=", 
    #           "output": "xxx", 
    #       }', 
    #       'status': '', 
    #       'calc_time_ms': 46992
    #   }, 
    # }


def gen_stress_data(image_input_file):
    """
    功能：生成压测数据
    输入：
        image_input_file: 图片文件
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(image_input_file, 'rb') as fp:
        image = base64.b64encode(fp.read())
    
    for i in range(10):
        data = {
            "image": image.decode('utf-8'), # 图片BASE64
            "imageid": "%s" % i,
            "calc_type": 1 + 2147483648 + 4294967296 + 8589934592,
        }
        print featureDemo.prepare_request([data])


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP.py 
    生成压测数据：
        python FEATURE_VIS_IMG_YIMEI_MERGEONE_GPU_WP.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        gen_stress_data('./image_dir/demo_img/FEATURE_FACE.png')
    else:
        params = []
        with open('./image_dir/demo_img/FEATURE_FACE.png', 'rb') as fp:
            image = base64.b64encode(fp.read())
            md5 = hashlib.md5()
            md5.update(image)
            params.append({
                "image": image.decode('utf-8'),
                "imageid": md5.hexdigest(),
                "calc_type": 1 + 2147483648 + 4294967296 + 8589934592,
            })
        feature_calculate(params)




