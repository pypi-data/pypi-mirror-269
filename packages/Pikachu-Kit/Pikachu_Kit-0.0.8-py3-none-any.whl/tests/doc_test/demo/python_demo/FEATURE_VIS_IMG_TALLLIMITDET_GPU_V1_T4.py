#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_TALLLIMITDET_GPU_AIPE Demo, 以及压测数据生成的DEMO
Author: gongchenting(gongchenting@baidu.com)
Date: 2022-02-18
Filename: FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4.py
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


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4 demo
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
        clientip = commands.getoutput("hostname")
        req_array = {
            'appid': '123456',
            'logid': logid,
            'format': 'json',
            'from': 'test',
            'cmdid': '123',
            'clientip': clientip,
            'data': base64.b64encode(json.dumps(data)),
        }
        return json.dumps(req_array)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    #import pdb; pdb.set_trace()
    data = {
        "image": base64.b64encode(Util.read_file(input_data))
    }
    feature_data = feature_demo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4',
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

    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    # 打印输出
    feature_demo.parse_result(res_data)

    ## parse out
    # result = json.loads(json.loads(res_data)['feature_result']['value'])['result']
    # result = json.loads(base64.b64decode(result))
    # num_kpts = result['num_kpts']
    # state_result = result['tall_limit_state']
    # det_result = result['det_res']
    # print(result)
    # import pdb;pdb.set_trace()
    # for k in det_result:
    #     tmp_dic = {}
    #     tmp_dic['x1'] = k['x1']
    #     tmp_dic['y1'] = k['y1']
    #     tmp_dic['score1'] = k['score1']
    #     tmp_dic['x2'] = k['x2']
    #     tmp_dic['y2'] = k['y2']
    #     tmp_dic['score2'] = k['score2']
    #     tmp_dic['x3'] = k['x3']
    #     tmp_dic['y3'] = k['y3']
    #     tmp_dic['score3'] = k['score3']
    #     tmp_dic['x4'] = k['x4']
    #     tmp_dic['y4'] = k['y4']
    #     tmp_dic['score4'] = k['score4']

def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    feature_demo = FeatureReq()
    # 压测数据生成demo
    img_file_list = sorted(os.listdir(input_dir))  # image_dir里边是图片列表，用于生成压测词表

    for image_file in img_file_list:
        data = {
            "image": base64.b64encode(Util.read_file(input_dir + '/' + image_file))
        }
        print feature_demo.prepare_request(data)  # 压测词表数据



if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4.py
    生成压测数据：
        python FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        feature_calculate('./image_dir/FEATURE_VIS_IMG_TALLLIMITDET_GPU_V1_T4.jpg')  # ./image_dir/img_file 本地图片
