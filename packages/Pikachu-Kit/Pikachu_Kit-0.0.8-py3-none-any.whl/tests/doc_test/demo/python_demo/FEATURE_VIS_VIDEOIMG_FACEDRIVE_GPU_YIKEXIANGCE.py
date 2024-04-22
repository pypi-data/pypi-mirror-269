#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE Demo, 以及压测数据生成的DEMO
Author: caijinhai(caijinhai@baidu.com)
Date: 2021-05-19
Filename: FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE.py 
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
    FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE demo
    表情驱动一刻相册专版
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        task_id = str(uuid.uuid4())
        request_data = {
            "action": "merge",
            "task_id": task_id,
            # 图片base64
            "req_image_id": data.get('req_image_id'),
            "req_video_id": data.get('req_video_id'),
            "version": data.get("version"),
            "track_url": data.get("track_url"),
            # 指定上传路径
            "upload_url": data.get("upload_url")
        }
        # 参数加密
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
        encrypt_res = encrypt(request_data)
        request_params = {
            "task_id": task_id,
            "cipher_text": encrypt_res.get("cipher_text"),
            "meta_info": encrypt_res.get("meta_info")
        }
        return json.dumps(request_params)


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
    feature_name = 'FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE'

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
    # callback 返回结果，带加密
    # {
    #   'source_key': '', 
    #   'status': 'Succeeded.', 
    #   'code': 0, 
    #   'logid': 8962231798, 
    #   'feature_result': {
    #       'feature': 'FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE', 
    #       'value': '{
    #           "meta_info": "BAkAAAAAAAA=", 
    #           "task_id": "40f512b5-1ecf-460d-aabd-64cb0fe6d137", 
    #           "cipher_text": "", # 加密字符串
    #           "err_msg": ""
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
    
    for _ in range(10):
        data = {
            "req_image_id": image.decode('utf-8'), # 图片BASE64
            "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/template/MaYiYaHei.mp4",
            "version": 1,
            "track_url": "https://facefusion-2021-peoplesdaily.cdn.bcebos.com/track/MaYiYaHei_v1_extract.tar.gz",
            "upload_url": "http://yq.poms.bae.baidu.com/rest/2.0/poms/bcs?sign=MBO:N2Q4YTRjYzE1ODJmMj:cZBzdM2MlDGVsAUqzvp/\
            nrDehMg=&method=upload&bucket=netdisk-pms-make&object=/2871298235-dev-5bd65ede25d0c2b869b0c429923bf263" #自定义url
        }
        print featureDemo.prepare_request(data)


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE.py 
    生成压测数据：
        python FEATURE_VIS_VIDEOIMG_FACEDRIVE_GPU_YIKEXIANGCE.py GEN_STRESS_DATA
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
        gen_stress_data('./image_dir/demo_img/FEATURE_FACE.png')
    else:
        # 合成视频
        data = {
            "req_image_id": "", # 图片BASE64
            "req_video_id": "https://facefusion-2021-peoplesdaily.bj.bcebos.com/template/MaYiYaHei.mp4",
            "version": 1,
            "track_url": "https://facefusion-2021-peoplesdaily.cdn.bcebos.com/track/MaYiYaHei_v1_extract.tar.gz",
            "upload_url": "http://yq.poms.bae.baidu.com/rest/2.0/poms/bcs?sign=MBO:N2Q4YTRjYzE1ODJmMj:cZBzdM2MlDGVsAUqzvp/\
            nrDehMg=&method=upload&bucket=netdisk-pms-make&object=/2871298235-dev-5bd65ede25d0c2b869b0c429923bf263" #自定义url
        }
        feature_calculate(data)




