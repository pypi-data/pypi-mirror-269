#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
"""
# Authors: fuyi03(@baidu.com)
# Date:    2018/08/30
# Brief:
#    人脸预测服务视频中台调用脚本
#    服务接口文档：http://wiki.baidu.com/display/idlface/FeatureService+V3.0
#    脚本中的参数含义请看接口文档
"""

import requests
import json
import time
import base64
import os
import sys
import cv2


def prepare_image(path):
    """ read image, set params """
    with open(path, 'rb') as img:
        b64img = base64.b64encode(img.read())
    image = {
        'imageid': path,
        'image': b64img.decode('utf-8')
    }
    return image


def do_request(img_path):
    """ request params """

    # 需求功能的bitmask,参考接口文档中的calc_type取值,1+2表示检测+72关键点
    img = prepare_image(img_path)
    params = {
        'provider': 'skindisease',
        'input': json.dumps({
            'logid': 'test_9527',
            'format': 'json',
            'imagesnum': 1,
            'targetfacenum': 1,
            'images': [img]
        })
    }

    job_name = " "  # 申请的作业名
    token = " "  # 作业的token
    feature_name = 'FEATURE_VIS_IMG_SKINDISEASE_GPU'


    data = {
        'business_name': job_name,  # 申请的作业名
        'resource_key': '',
        'auth_key': token,  # 作业的token
        'feature_name': feature_name,
        'data': base64.b64encode(json.dumps(params).encode('utf-8')).decode()
    }

    url = 'http://xvision-api.sdns.baidu.com/xvision/xvision_sync'
    # 目前版本的视频中台请求必须将作业名和算子名拼在url中，否则就近访问无效
    # url += '?business_name=%s&feature_name=%s' % ('aa_yy_test', 'FEATURE_VIS_IMG_SKINDISEASE1_GPU')
    url += '?business_name=%s&feature_name=%s' % (job_name, feature_name)
    headers = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    print(resp.content)


if __name__ == '__main__':
    image = "23.jpg"
    do_request(image)


