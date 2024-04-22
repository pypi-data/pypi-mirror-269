#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2021-04-16
Filename: FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU.py 
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
    FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        # request_data = {
        #     "action": "track",
        #     "task_id": str(uuid.uuid4()),
        #     "req_video_id": data.get('req_video_id'),
        #     "version": data.get("version"),
        # }
        request_data = {
            "action": "merge",
            "task_id": str(uuid.uuid4()),
            "req_image_id": data.get('req_image_id'),
            "req_video_id": data.get('req_video_id'),
            "version": data.get("version"),
            "track_url": data.get("track_url"), 
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
    feature_name = 'FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU'

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
        "resource_key": 'test',
        "auth_key": token,
        "feature_name": feature_name,
        "data": base64.b64encode(feature_data),
        # callback 信息，可选参数
        'callback': json.dumps({
            "path": "/face-api/vmfacedrive/task/callback",
            "host": "yq01-sys-hic-k8s-k40-qm-0019.yq01.baidu.com",
            "port": 8090,
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
    
    for image_url in image_urls:
        data = {
            "req_image_id": image_url,
            "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/template/MaYiYaHei.mp4",
            "version": 1,
            "track_url": "https://facefusion-2021-peoplesdaily.cdn.bcebos.com/track/MaYiYaHei_v1_extract.tar.gz",
        }
        print featureDemo.prepare_request(data)


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU.py GEN_STRESS_DATA
    """
    # 执行流程：
    # 1. 下载图片
    # 2. 根据视频来判断服务所在机器是否有视频数据包缓存（缓存目录：MaYiYaHei_v1）
    #     若有则直接进行融合，生成视频
    #     若无则通过track_url下载数据包缓存到本地目录，然后再合成视频
    # 3. 上传视频到BOS，回调返回url信息

    # 服务支持两种动作：
    # 1. action: merge 融合视频
    # 2. action: track 生成视频数据包
    # 拆分的目的是
    #   生成数据包一个视频只需执行一次，因此只需在准备阶段调用即可
    #   简化执行的流程步骤，并且可以针对视频数据帧数据做定制修改，融合动作时传入指定的数据包地址即可
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测数据
        # image.txt: 图片url列表文件
        gen_stress_data('./video_url_dir/FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU/image.txt')
    else:
        # 合成视频
        data = {
            "req_image_id": "http://facefusion-2021-peoplesdaily.bj.bcebos.com/image/\
                16184763335989_8e714455eb32c030f1a5beef13cc7e92",
            "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/template/MaYiYaHei.mp4",
            "version": 1,
            "track_url": "https://facefusion-2021-peoplesdaily.cdn.bcebos.com/track/MaYiYaHei_v1_extract.tar.gz", 
        }
        feature_calculate(data)




