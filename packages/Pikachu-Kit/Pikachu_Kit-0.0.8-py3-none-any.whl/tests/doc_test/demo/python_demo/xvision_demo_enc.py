#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:百度视频中台特征计算Demo基类
Author: wanghua11(wanghua11@baidu.com)
Date: 2019-07-29
Filename: XvisionDemoEnc.py
"""
from abc import ABCMeta, abstractmethod
import base64
import random
import requests
import json


class XvisionDemoEnc(object):
    """
    XvisionDemoEnc
    """
    __metaclass__ = ABCMeta

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

    @abstractmethod
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据，每个算子demo需要重写此方法
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        pass

    def request_feat(self, xvision_data, xvision_url, meta):
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
                'X-VIS-ENCRYPT-METAINFO': meta,
                'X-VIS-DATA-ENCRYPTED': 'BDES_BINARY'
            }

            res = requests.post(xvision_url, json.dumps(xvision_data), headers=self.headers)
            return res.text
        except Exception as e:
            print "post request error[{error}]".format(error=str(e))
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
            res = requests.post(xvision_url, params=params, data=xvision_data, headers=headers)
            return res.text
        except Exception as e:
            print "post request error[{error}]".format(error=str(e))
            return ""

    def parse_result(self, res_data):
        """
        功能：解析算子的输出结果
        输入：
            res_data：算子的输出结果
        输出：
            算子输出结果
        """
        print res_data

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
