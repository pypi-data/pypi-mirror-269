#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_VIS_IMG_FEED_POSTER_RENDER_V1_A30 Demo, 以及压测数据生成的DEMO
Author: RongKang (rongkang@baidu.com)
Date: 2023-12-14
Filename: FEATURE_VIS_IMG_FEED_POSTER_RENDER_V1_A30.py
"""

import json
import base64
import random
import urllib
import sys
import os
import requests

# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
assert IS_PY3 == True, 'ONLY SUPPOSE PY3!'

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus



class XvisionDemo():
    """
    XvisionDemo 
    """
    def __init__(self):
        """
        __init__
        """
        # 百度视频中台集群，高可用型、均衡型作业用xvision_online_url，高吞吐型作业使用xvision_offline_url
        self.xvision_online_url = 'http://xvision-api.sdns.baidu.com'  # 百度视频中台高可用型作业集群
        self.xvision_offline_url = 'http://group.xvision-xvisionproxyoffline.xVision.all.serv:8089'  # 百度视频中台高吞吐型作业集群
        self.xvision_test_url = 'http://group.xvision-xvisionproxytest.xVision.all.serv:8089'  # 百度视频中台测试作业集群

        # 百度视频中台接口的path，不同算子不同，具体算子demo中写清楚
        self.xvision_sync_path = '/xvision/xvision_sync'
        self.xvision_callback_path = '/xvision/xvision_callback'
        self.feat_sync_path = '/xvision/feat_sync'
        self.feat_callback_path = '/xvision/feat_callback'
        self.image_rank_path = '/xvision/high_level/image_rank'

        # 添加请求头
        self.headers = {'Content-Type': 'application/json; charset=UTF-8'}

        # initializelogid
        self.logid = random.randint(100000000, 10000000000)
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据，每个算子demo需要重写此方法
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        pass

    def request_feat(self, params, xvision_data, xvision_url):
        """
        功能：请求远端算子服务
        输入：
            xvision_data：dict, 百度视频中台的输入数据
            xvision_url：百度视频中台集群url
        返回：
            特征计算结果
        """
        try:
            self.headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                "X_BD_LOGID": "%d" % self.logid,
            }

            res = requests.post(xvision_url, params=params, data=json.dumps(xvision_data), headers=self.headers)
            return res.text
        except Exception as e:
            print("post request error[{error}]".format(error=str(e)))
            return ""

    def request_feat_new(self, params, xvision_data, xvision_url, headers):
        """
        功能：请求远端算子服务(新版本)
        输入：
            xvision_data：dict, 百度视频中台的输入数据
            xvision_url：百度视频中台集群url
        返回：
            特征计算结果
        """
        try:
            res = requests.post(xvision_url, params=params, data=json.dumps(
                xvision_data).encode('utf-8'), headers=headers)
            return res.text
        except Exception as e:
            print("post request error[{error}]".format(error=str(e)))
            return ""

    def parse_result(self, res_data):
        """
        功能：解析算子的输出结果
        输入：
            res_data：算子的输出结果
        输出：
            算子输出结果
        """
        
        print(res_data)
        res_data=json.loads(res_data)
        result = res_data['feature_result']['value']
        result = json.loads(result)
        print('result', result)
        # result = 

    def gen_xvision_data(self, argv_dict):
        """
        功能：生成百度视频中台输入(适用于/xvision/xvision_sync接口)
        输入：
            argv_dict = {
                'business_name': '',#作业名
                'resource_key': '',#数据标记，可以是图片/视频/音频的title
                'auth_key': '',#token
                'feature_name',#算子名，比如FEATURE_xxxx
                'feature_input_data': ''#算子输入数据
            }
        输出：
            百度视频中台的输入
        """
        return {
            "business_name": argv_dict['business_name'],
            "resource_key": argv_dict['resource_key'],
            "auth_key": argv_dict['auth_key'],  # token
            "feature_name": argv_dict['feature_name'],  # 算子名
            "data": base64.b64encode(argv_dict['feature_input_data'])
        }

    def gen_xvision_data_input_img(self, argv_dict):
        """
        功能：生成百度视频中台输入(输入base64，适用于/xvision/feat_sync接口)
        输入：
            argv_dict = {
                'business_name': '',#作业名
                'resource_key': '',#数据标记，可以是图片/视频/音频的title
                'auth_key': '',#token
                'feature_name',#算子名，比如FEATURE_xxxx
                'feature_input_data': ''#算子输入数据
            }
        输出：
            百度视频中台的输入
        """
        return {
            "business_name": argv_dict['business_name'],
            "resource_key": argv_dict['resource_key'],
            "input_message": {
                "passthrough_field": "key",
                "img_base64": argv_dict['feature_input_data']
            },
            "auth_key": argv_dict['auth_key'],
            "feature_list": [{
                "feature_name": argv_dict['feature_name']
            }]
        }

    def gen_xvision_data_input_url(self, argv_dict):
        """
        功能：生成百度视频中台输入(输入url，适用于/xvision/feat_sync接口)
        输入：
            argv_dict = {
                'business_name': '',#作业名
                'resource_key': '',#数据标记，可以是图片/视频/音频的title
                'auth_key': '',#token
                'feature_name',#算子名，比如FEATURE_xxxx
                'feature_input_data': ''#算子输入数据
            }
        输出:
            百度视频中台输入
        """
        return {
            "business_name": argv_dict['business_name'],
            "resource_key": argv_dict['resource_key'],
            "input_message": {
                "content_passthrough_url": argv_dict['feature_input_data'],
                "passthrough_field": "key"
            },
            "auth_key": argv_dict['auth_key'],
            "feature_list": [{
                "feature_name": argv_dict['feature_name']
            }]
        }


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_TERROR_GPU_V9 demo  
    """

    def prepare_request(self, img=None, article_content=''):
        """prepare request
        """
        
        assert img is not None, "img is none"
        assert len(article_content) > 0, "article_content is empty"
        
        imgstr = base64.b64encode(img_data).decode('utf-8')
        # imgstr = base64.b64encode(img).decode('utf-8')
        req_array = {
            'image':imgstr,
            'session_id':'00001-test000000',
            'article_content':''            
        }
        reqstr = json.dumps(req_array)
        reqstr = reqstr.encode("utf-8") if IS_PY3 else reqstr
        datastr = base64.b64encode(reqstr)
        datastr = datastr.decode('utf-8') if IS_PY3 else datastr
        req_json = {
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'data': datastr,
                }
        return req_json

def feature_calculate(input_data):
    """
    功能：请求图生文服务
    输入：
        input_data:本地图片文件
    输出：
        图片描述
    """
    featureDemo = FeatureReq()
    # 生成算子输入

    img_data = open('00000.png', 'rb').read()
    article_content = '' #正文内容
    feature_data = featureDemo.prepare_request(img= img_data, article_content = article_content)
    

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_IMG_IMAGECAPTION_GPU_A30_V2_1',
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
    # print("AAA:{}".format(res_data.encode("utf-8")))
    # print(res_data.encode("utf-8"))




if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_FEED_POSTER_RENDER_V1_A30.py 
    生成压测数据：
        python FEATURE_VIS_IMG_FEED_POSTER_RENDER_V1_A30.py GEN_STRESS_DATA
    """
    img_data = "https://bjh-pixel.bj.bcebos.com/out-117-seq0-0-25006"
    feature_calculate(img_data)  # ./image_dir/img_file 本地图片
