#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU Demo, 以及压测数据生成的DEMO
Author: wanxingyu(wanxingyu@baidu.com)
Date: 2022-08-11
Filename: FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU.py 
"""
from xvision_demo import XvisionDemo
#from util import Util
import json
import base64
import random
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import uuid
import time
import requests

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        request_data = {
            'appid': 'wanxingyu',
            'logid': 20220805,
            'bjh_nid': data.get('nid'),#'4759560811239185009',
            'video_url': data.get('video_url'), # data
            'max_frame': 20,
            'batch_size': 4,
            'max_object': 4,
            'title': data.get('title'),
            'category': data.get('category'),
            'authen': json.dumps([{'appid': '16a413aaa55b54a6d6b8c54d61c2dbb3', 
            'ak': '', 'sk': ''}]),
        }
        return json.dumps(request_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: {'video_url': ''}
    输出：
        检索结果
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)
    #print 'request_data:', feature_data
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = 'FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU'

    # 异步任务url
    url = featureDemo.xvision_online_url + featureDemo.xvision_callback_path
    params = {
        "business_name": job_name,
        "feature_name": feature_name,
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X_BD_LOGID': "%d" % 20220815,#str(random.randint(1000000, 100000000)),
    }
    data = json.dumps({
        "business_name": job_name,
        "resource_key": 'test_baijiahao_asy', # 建议自定义值，中台会原样传回
        "auth_key": token,
        "feature_name": feature_name,
        "data": base64.b64encode(feature_data),
        # callback 信息，可选参数
        'callback': json.dumps({
            "host": "10.153.103.17",
            "port": 8100,
            "path": "/",
            "retry_times": 3,
            "connect_timeout": 20000,
            "read_timeout": 20000,
            "write_timeout": 20000,
        })
    })

    res_data = featureDemo.request_feat_new(params, data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)


def gen_stress_data(video_input_file):
    """
    功能：生成压测数据
    输入：
        video_input_file: 视频url文件
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(video_input_file, 'r') as f:
        lines = f.readlines()[1:]
    for i_vid, line in enumerate(lines):
        items = line.strip().split('\t')
        vid = items[-1] # 视频名称.***
        first_cate = items[1].encode('utf8') # 视频一级垂类
        second_cate = items[2].encode('utf8') # 视频二级垂类
        vid_title = items[3] # 文章标题
        vid_name = vid.split('.')[0] # 视频名称
        nid = items[0] # 文章nid
        vid_url = items[-2] # 视频url

        data = {
                "video_url": vid_url,
                "title": vid_title,
                "category": '{}>{}'.format(first_cate, second_cate),
                "nid": nid,
            }

        print featureDemo.prepare_request(data)

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU.py GEN_STRESS_DATA
    """
    # 执行流程：
    # 1. 读取视频
    # 2. 视频在线切帧
    # 3. 图片帧提取视觉特征和文本特征
    # 4. 调用商品检索服务
    # 5. 商品精排序
    # 6. 返回检索结果

    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    #print op_type
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据    
        gen_stress_data('./video_url_dir/FEATURE_VIS_VIDEO_BAIJIAHAO_ASY_GPU/
        shi_he_dai_huo_case100_sampled_list-vid_url.txt')
    else:
        # 合成视频
        data = {
            "video_url": 
            "http://10.153.103.17:8188/baijiahao_online/data/shi_he_dai_huo_case100_video/mda-naagwp8zm9kiinp2.mp4",
            "nid": "10218521652613781072",
            "title": "OPPO Reno7红丝绒新年版开箱！红色机身+丝绒手感，颜值手感满分",
            "category": '{}>{}'.format('数码'.encode('utf8'), '数码综合'.encode('utf8'))
        }
        feature_calculate(data)




