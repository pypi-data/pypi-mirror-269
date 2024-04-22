#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_BAIJIAHAO_OFFLINE_FEATURE_GPU.py Demo, 以及压测数据生成的DEMO
Author: wanglongchao(wanglongchao@baidu.com)
Date: 2022.4.13
Filename: FEATURE_VIS_BAIJIAHAO_OFFLINE_FEATURE_GPU.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import sys
import os
import random
from proto.FEATURE_VIS_TEXT_GPU_ROBERTA import imgfeature_pb2
from proto.FEATURE_VIS_TEXT_GPU_ROBERTA.protobuf_to_dict import protobuf_to_dict




class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_GPU_HUAWEI_3C
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        return json.dumps({
            'appid': '123456',
            'logid': random.randint(1000000, 100000000),
            'format': 'json',
            'from': 'xvision',
            'cmdid': '123',
            'clientip': '0.0.0.0',
            'data': base64.b64encode(data),
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
    # 生成算子输入
    #data = {
    #    'image': Util.read_file(input_data)
    #}

    pid = '45'
    dettype = '4'
    img_data = Util.read_file(input_data)
    proto_data = imgfeature_pb2.FeatureRequest()
    proto_data.image = img_data
    proto_data.query_sign = '123,321'
    info_texts = proto_data.info.texts.add()
    info_texts.key = 'searchsource'
    info_texts.value = pid
    info_texts = proto_data.info.texts.add()
    info_texts.key = 'dettype'
    info_texts.value = dettype

    info_texts = proto_data.info.texts.add()
    info_texts.key = 'featureids'
    info_texts.value = 'obj_det'
    #info_texts.value = 'general_obj_1_det'
    #info_texts.value = 'general_fea_det'
    #info_texts.value = 'shihuo_obj_1_det'
    #info_texts.value = 'shihuo_fea_det'
    #"""
    info_texts = proto_data.info.texts.add()
    info_texts.key = 'title'
    info_texts.value = '韩版宽松百搭女士白色短袖t恤夏季2021年新款女装上衣ins潮打底衫'
    info_texts = proto_data.info.texts.add()
    info_texts.key = 'category_level1'
    info_texts.value = '服饰内衣'
    info_texts = proto_data.info.texts.add()
    info_texts.key = 'category_level2'
    info_texts.value = '女装'
    info_texts = proto_data.info.texts.add()
    info_texts.key = 'category_level3'
    info_texts.value = 'T恤'
    #"""

    #info_texts = proto_data.info.texts.add()
    #info_texts.key = 'featureids'
    #info_texts.value = 'shihuo_fea_det'

    data = proto_data.SerializeToString() 


    feature_data = featureDemo.prepare_request(data)
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_BAIJIAHAO_OFFLINE_GPU',
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
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表
    for image_file in img_file_list:
        data = {
            "image": Util.read_file(input_dir + '/' + image_file)
        }
        print featureDemo.prepare_request(data)  # 压测词表数据
if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_OCR_GPU_DRIVING_V2_NEW_ARCH
    生成压测数据：
        python FEATURE_VIS_IMG_OCR_GPU_DRIVING_V2_NEW_ARCH GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/img_file')  # ./image_dir/img_file 本地图片
