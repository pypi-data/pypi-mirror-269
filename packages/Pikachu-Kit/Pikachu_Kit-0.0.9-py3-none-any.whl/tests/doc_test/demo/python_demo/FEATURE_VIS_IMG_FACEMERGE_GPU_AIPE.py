#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE Demo, 以及压测数据生成的DEMO
Author: work(work@baidu.com)
Date: 2020-06-28
Filename: FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import urllib
import sys
import os
import random
import commands
import cv2

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        req_data = {
            "appid": "xvision_job_name", #填写视频中台的作业名，方便排查问题
            "logid": random.randint(1000000, 100000000),
            "format": "json",
            "from": "xvision",
            "cmdid": "123",
            "clientip": commands.getoutput("hostname"), #请求ip，用户发送请求的ip地址，方便排查问题
            "data": base64.b64encode(data)
        }
        return json.dumps(req_data)


def feature_calculate(input_data, is_alpha_channel=False):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    demo = FeatureReq()
    user_img = input_data['user']
    template_img = input_data['template']
    if is_alpha_channel:
        user_img = cv2.imread(user_img, cv2.IMREAD_UNCHANGED)
        user_img_data = base64.b64encode(cv2.imencode(".png", user_img)[1].tostring())
        template_img = cv2.imread(template_img, cv2.IMREAD_UNCHANGED)
        template_img_data = base64.b64encode(cv2.imencode(".png", template_img)[1].tostring())
    else:
        with open(template_img, 'r') as imgfile:
            template_img_data = base64.b64encode(imgfile.read())
        with open(user_img, 'r') as imgfile:
            user_img_data = base64.b64encode(imgfile.read())

    #生成算子输入
    data = "object_type=convert_facesw" + \
           "&image=" + user_img_data + \
           "&template_image=" + template_img_data + \
           "&landmark=" + "" + \
           "&template_landmark=" + ""

    feature_data = demo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = demo.xvision_online_url + demo.xvision_sync_path

    # 高可用型、均衡型作业将job_name、feature_name放到 url 中
    if demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res_data = demo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    demo.parse_result(res_data)


def gen_stress_data(input_data):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    demo = FeatureReq()
    #压测数据生成demo
    user_img_file_list = sorted(os.listdir(input_data['user']))
    template_img_file_list = sorted(os.listdir(input_data['template']))
    #image_dir里边是图片列表，用于生成压测词表
    for i in range(len(img_file_list)):
        template_img = input_data['template'] + '/' + template_img_file_list[i]
        user_img = input_data['user'] + '/' + user_img_file_list[i]
        with open(template_img, 'r') as imgfile:
            template_img_data = base64.b64encode(imgfile.read())
        with open(user_img, 'r') as imgfile:
            user_img_data = base64.b64encode(imgfile.read())

        data = "object_type=convert_facesw" + \
               "&image=" + user_img_data + \
               "&template_image=" + template_img_data + \
               "&landmark=" + "" + \
               "&template_landmark=" + ""

        print demo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE.py
    生成压测数据：
        python FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        input_data = {
                'user': './image_dir/FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE/user/',
                'template': './image_dir/FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE/template/'
        }
        gen_stress_data(input_data) #./image_dir/ 是本地的图片数据
    else:
        #特征计算Demo
        input_data = {
                'user': './image_dir/FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE/user/test_img1.jpg',
                'template': './image_dir/FEATURE_VIS_IMG_FACEMERGE_GPU_AIPE/template/test_img1.jpg'
        }
        feature_calculate(input_data) #./image_dir/img_file 本地图片
