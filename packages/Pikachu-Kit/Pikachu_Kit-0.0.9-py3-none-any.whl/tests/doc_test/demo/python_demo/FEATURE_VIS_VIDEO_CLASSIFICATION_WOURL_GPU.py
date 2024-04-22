#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU Demo, 以及压测数据生成的DEMO
Author: wanghua11(wanghua11@baidu.com)
Date: 2019-07-29
Filename: FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU.py 
"""
from xvision_demo import XvisionDemo
import urllib
import sys
import random


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU demo  
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
            "logid": random.randint(1000000, 100000000),
            "video_url": data['video_url'],
            "svc_name": "FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU",
        }
        return urllib.urlencode(req_data)


def feature_calculate():
    """
    功能：特征计算
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
            "video_url": "http://vd3.bdstatic.com/mda-jf0kg11xhwufc43d/mda-jf0kg11xhwufc43d.mp4?playlist=%5B%22hd%22%2C%22sc%22%5D"
            #"video_url": "http://bj.bcebos.com/videolize-search/50903e82d1f5e15133bbec724f4babb1.mp4"
            }
    feature_data = featureDemo.prepare_request(data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU',
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
    with open(input_dir, 'r') as fp:
        video_url_file = fp.readlines()
    for video_url in video_url_file:
        data = {
                    "video_url": video_url.rstrip('\n') 
                }
        print featureDemo.prepare_request(data)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEO_CLASSIFICATION_WOURL_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./video_url_dir/url_file')#./video_url_dir/url_file 是视频url文件
    else:
        #特征计算Demo
        feature_calculate() #./image_dir/img_file 本地图片

