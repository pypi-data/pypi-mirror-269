#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_VIDEOMERGE_DISTRIBUTE Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2022-05-13
Filename: FEATURE_VIS_VIDEOIMG_VIDEOMERGE_DISTRIBUTE.py 
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

class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_VIDEOIMG_VIDEOMERGE_DISTRIBUTE demo  
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
            "action": "distribute",  # merge 动作，固定值
            "task_id": str(uuid.uuid4()),   # 业务唯一ID，自定义，回调会传递回
            "req_image_id": data.get('req_image_id'),
            "req_video_id": data.get('req_video_id'),
            "alpha": data.get("alpha"),
        }
        return json.dumps(request_data)


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data: {'req_image_id': '', 'req_video_id': '', 'version': '', 'track_url': ''}
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    feature_name = 'FEATURE_VIS_VIDEOIMG_VIDEOMERGE_DISTRIBUTE'

    # 异步任务url
    url = featureDemo.xvision_online_url + featureDemo.xvision_callback_path
    params = {
        "business_name": job_name,
        "feature_name": feature_name,
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X_BD_LOGID': str(random.randint(1000000, 100000000)),
    }
    data = json.dumps({
        "business_name": job_name,
        "resource_key": 'test', # 建议自定义值，中台会原样传回
        "auth_key": token,
        "feature_name": feature_name,
        "data": base64.b64encode(feature_data),
        # callback 信息，可选参数
        'callback': json.dumps({
            "host": "10.88.152.25",
            "port": 8100,
            "path": "/",
            "retry_times": 3,
        })
    })

    res_data = featureDemo.request_feat_new(params, data, url, headers)
    # 打印输出
    featureDemo.parse_result(res_data)


def gen_stress_data(image_input_file):
    """
    功能：生成压测数据
    输入：
        image_input_file: 图片url文件
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(image_input_file, 'r') as fp:
        image_urls = fp.readlines()
    
    for index, image_url in enumerate(image_urls):
        if index % 2 == 0:
            data = {
                "req_image_id": image_url,
                "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/QA_test/video/10.mp4",
                "alpha": 0
            }
        else:
            data = {
                "req_image_id": image_url,
                "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/QA_test/video/rgba.webm",
                "alpha": 1
            }
        print featureDemo.prepare_request(data)


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEOIMG_VIDEOMERGE_DISTRIBUTE.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_VIDEOMERGE_DISTRIBUTE.py GEN_STRESS_DATA
    """
    # 执行流程：
    # 1. 下载图片
    # 2. 下载视频
    # 3. 视频提取音频转码
    # 4. 视频分段
    # 5. 调用server将分段视频融合
    # 6. 合并分段结果视频和音频
    # 7. 结果视频上传返回链接

    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        # image.txt: 图片url列表文件
        gen_stress_data('./video_url_dir/FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU/image.txt')
    else:
        # 合成视频
        data = {
            "req_image_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/QA_test/14da0a180743627a8521b913b.jpg",
            # "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/QA_test/video/10.mp4",
            # "alpha": 0,
            # 注意，alpha:1 时，视频模版需要是透明通道的视频，否则融合不成功
            "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/QA_test/video/rgba.webm",
            "alpha": 1,
        }
        feature_calculate(data)




