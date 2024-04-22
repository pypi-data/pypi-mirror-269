#!/usr/bin/env python
# coding=utf-8
"""
Author: zhanghuimeng@baidu.com
since: 2023-01-03 19:55:39
LastTime: 2023-01-19 10:43:23
LastAuthor: zhanghuimeng@baidu.com
message: FEATURE_KG_TEXT_EGL_GPU Demo, 以及压测数据生成的DEMO
Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import random
import sys
import os
import base64

class FeatureReq(XvisionDemo):
    """
    FEATURE_KG_TEXT_EGL_GPU demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据

        Args:
            data (dict): key is [line,mention], mention is optional

        Returns:
            [str]: 返回算子的输入数据
        """
        return json.dumps(data)


def feature_calculate(input_data):
    """
    功能：特征计算

    Args:
        input_data (dict): key is data
    输出：
        kger 结果
    """
    feature_demo = FeatureReq()
    # 生成算子输入
    feature_data = feature_demo.prepare_request(input_data)

    job_name = ""  # 应用名
    token = ""  # token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_KG_TEXT_NER_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # 获取url
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path
    # url = feature_demo.xvision_test_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    # 请求百度视频中台特征计算服务
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)

    res_data = json.loads(res_data)
    res_data['feature_result']['value'] = json.loads(res_data['feature_result']['value'])
    return res_data


def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待链指的文本，json 形式的 dict, key 是 line 和 mention(可选)，每一行是一个json字符串
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            line = json.loads(line.strip())
            print featureDemo.prepare_request(line)


if __name__ == '__main__':
    # 特征计算Demo
    text_a = u'“清明上河图”牦牛角立体微雕亮相兰州 5月10日，牦牛角立体微雕“清明上河图”亮相甘肃兰州。' \
            u'为创作蓝本，长8米，宽1.6米，涵盖人物728名、船只29艘、房屋152栋等。 新甘肃·甘肃经济日报记者　陈功章　摄特别声明：以上文章内容仅代表作者本人观点，' \
            u'不代表新浪网观点或立场。如有关于作品内容、版权或其它问题请于作品发表后的30日内与新浪网联系。'
    text_b = u'这幅核酸版《清明上河图》火了,震撼! 这幅核酸版《清明上河图》火了,震撼! ' \
            u'2022 05/06 07:27 侃名著的小火柴 企鹅号 分享 评论 0 在广东佛山,一位90后小伙 根据自己的亲身经历 ' \
            u'创作了一幅"核酸检测上河图", 许多网友看后纷纷点赞 00:00 / 00:00 480p 倍速 hls格式需要hls.js内核播放,但当前环境不支持此内核 你可以 刷新试试 70011114-815b5f918cb7b8dafff62bfd93a673fe 免责声明:本文来自腾讯新闻客户端创作者,不代表腾讯网的观点和立场.'
        
    req_dict = {
        "text_a": text_a,
        "text_b": text_b}

    input = {'data': [req_dict]}

    print(json.dumps(feature_calculate(input), ensure_ascii=False, indent=4))
