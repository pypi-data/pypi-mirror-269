#!/usr/bin/env python3
# coding=utf-8

"""
Author: wangqi31@baidu.com
since: 2022-02-01 11:12:11
LastTime: 2022-02-01 11:12:11
LastAuthor: wangqi31@baidu.com
message: FEATURE_KG_CMSIM_IT_TEXT_V1 Demo
Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved 
"""

import json
import random
import requests


class XvisionOperator(object):
    """
    FEATURE_KG_CMSIM_IT_TEXT_V1 demo
    """

    def __init__(self, job_name, token, feature_name='FEATURE_KG_CMSIM_IT_TEXT_V1'):
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

        # 添加请求头
        self.headers = {'Content-Type': 'application/json; charset=UTF-8'}

        # initializelogid
        self.logid = random.randint(100000000, 10000000000)

        # jobid
        self.job_name = job_name
        # token
        self.token = token
        # feature_name
        self.feature_name = feature_name

        # 获取url，高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
        self.url = self.xvision_online_url + self.xvision_sync_path

        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'resource_key': 'test.txt',
            'auth_key': self.token,
            'business_name': self.job_name,
            'feature_name': self.feature_name,
            'X_BD_LOGID': str(random.randint(1000000, 100000000))
        }

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        Args:
            data：string类型，待计算的文本
        Returns:
            返回算子的输入数据
        """
        return json.dumps(data)

    def gen_cmsim(self, data):
        """
        功能：请求远端算子服务
        Args:
            xvision_data：dict, 百度视频中台的输入数据
        Returns:
            特征计算结果
        """
        # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
        feature_data = self.prepare_request(data)
        if self.xvision_online_url in self.url:
            params = {
                "business_name": self.headers["business_name"],
                "feature_name": self.headers["feature_name"]
            }
        else:
            params = {}

        # 请求百度视频中台特征计算服务
        patience = 3
        for i in range(patience):
            try:
                res = requests.post(self.url, params=params,
                                    data=feature_data, headers=self.headers)
                return res.text
            except Exception as e:
                if i == patience - 1:
                    raise e

    def analysis_result(self, data):
        """获取cmsim解析结果

        Args:
            data ([json]): [xvision return data]

        Returns:
            [json]: [cmsim result]
        """
        try:
            data = json.loads(data)
            if 'code' in data and data['code'] == 0:
                feature_result = data['feature_result']['value']
                return json.loads(feature_result)
        except Exception as e:
            return {}


if __name__ == '__main__':
    # xvision job name
    job_name = ''
    # xvision token
    token = ''
    operator = XvisionOperator(job_name,
                               token,
                               feature_name='FEATURE_KG_CMSIM_IT_TEXT_V1')
    line = {"@id": "10003", "text": ["汽车车漆怎么保养"], "meta": {}}
    xvison_ret = operator.gen_cmsim(json.loads(line.strip()))
    cmsim_ret = operator.analysis_result(xvison_ret)
    print(cmsim_ret)
