#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_AR_IMG_VTRYON_CPU_V2 Demo, 以及压测数据生成的DEMO
Author: cuixiankun01(cuixiankun01@baidu.com)
Date: 2022-11-28
Filename: FEATURE_AR_IMG_VTRYON_CPU_V2.py
"""
import os

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys


class FeatureReq(XvisionDemo):
    """
    FEATURE_AR_IMG_VTRYON_CPU_V2 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """

        return json.dumps(
            {
                "log_id": data['log_id'],
                "mode":  data['mode'],
                "img_object_key": data['img_object_key'],
                "video_object_key": data['video_object_key'],
                "img_base64": str(base64.b64encode(data["img_base64"]), "utf-8"),
                "cloth_param": data['cloth_param'],
                "measure_param": data['measure_param'],
                "background_code": data['background_code'],
            })


def load_json(json_pth):
    """load_json"""
    return json.load(open(json_pth))


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    # data = json.dumps(data).encode()
    # 生成算子输入
    log_id = str(random.randint(1000000, 100000000))
    data = {
        "log_id": log_id,
        "mode": "vtryon_animate",
        'img_object_key': 'temp/' + log_id + '_body.png',
        'video_object_key': 'temp/' + log_id + '_animate.mp4',
        "img_base64": Util.read_file(input_data["body_person"]),
        "cloth_param": load_json(input_data["cloth_param"]),
        'measure_param': load_json(input_data["measure_param"]),
        'background_code': input_data["background_code"],
        # "background_url": background_url
    }

    feature_data = featureDemo.prepare_request(data)

    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_online_url + featureDemo.xvision_sync_path

    job_name = 'STRESSJOBFEATURE_AR_IMG_VTRYON_CPU_V2'
    token = '749b54e1-df94-595b-8975-eeab19c5f2f6'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_AR_IMG_VTRYON_CPU_V2',
        'logid': str(random.randint(1000000, 100000000)),
    }

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if featureDemo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    res = featureDemo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    # print(res)
    featureDemo.parse_result(res)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    for body_person_name in os.listdir(input_dir['body_person']):
        if body_person_name.find('.png') < 0:
            continue
        body_person_pth = os.path.join(input_dir['body_person'], body_person_name)
        
        for cloth_name in os.listdir(input_dir['cloth_param']):
            if cloth_name.find('.json') < 0:
                continue
            
            cloth_pth = os.path.join(input_dir['cloth_param'], cloth_name)

            for measure_name in os.listdir(input_dir['measure_param']):
                if measure_name.find('.json') < 0:
                    continue
                measure_pth = os.path.join(input_dir['measure_param'], measure_name)

                log_id = str(random.randint(1000000, 100000000))
                data = {
                    "log_id": log_id,
                    "mode": "vtryon_animate",
                    'img_object_key': 'temp/' + log_id + '_body.png',
                    'video_object_key': 'temp/' + log_id + '_animate.mp4',
                    "img_base64": Util.read_file(body_person_pth),
                    "cloth_param": load_json(cloth_pth),
                    'measure_param': load_json(measure_pth),
                    'background_code': 1,
                    # "background_url": background_url
                }


            # print featureDemo.prepare_request(data)  # 压测词表数据


   

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_AR_IMG_VTRYON_CPU_V2.py
    生成压测数据：
        python FEATURE_AR_IMG_VTRYON_CPU_V2.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    # op_type = 'GEN_STRESS_DATA'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        input_data = {
            'body_person': './image_dir/FEATURE_AR_IMG_VTRYON_CPU_V2/body_person',  # 图片目录
            'cloth_param': './image_dir/FEATURE_AR_IMG_VTRYON_CPU_V2/cloth_param',  # 服装参数目录
            'measure_param': './image_dir/FEATURE_AR_IMG_VTRYON_CPU_V2/measure_param', # 人体身材参数
        }
        gen_stress_data(input_data)
    else:
        # 特征计算Demo
        input_data = {
            'body_person': './python_demo/image_dir/FEATURE_AR_IMG_VTRYON_CPU_V2/body_person/body_person4.png',
            'cloth_param': './python_demo/image_dir/FEATURE_AR_IMG_VTRYON_CPU_V2/cloth_param/1306170_1306169.json',
            'measure_param': './python_demo/image_dir/FEATURE_AR_IMG_VTRYON_CPU_V2/measure_param/female_0031.json',
            'background_code': 1,
        }

        feature_calculate(input_data)  # 本地图片与参数配置
