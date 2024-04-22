#!/usr/bin/env python
# coding=utf-8
"""
Author: changwanli@baidu.com
since: 2021-02-03 19:55:39
LastTime: 2021-12-17 14:50:41
LastAuthor: changwanli@baidu.com
message: FEATURE_KG_TEXT_TAG_GPU_V2 Demo, 以及压测数据生成的DEMO
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
    FEATURE_KG_TEXT_TAG_GPU_V2 demo
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
        NER 结果
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
        'feature_name': 'FEATURE_KG_TEXT_TAG_GPU_V2',
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
    data = {"data": [{"text_list": [u"太暖了！俄罗斯家养小薮猫遇上人类幼崽，会轻轻地贴贴", u"米奇! 过来吧 过来我的小帅哥 弟弟来和你交朋友了\
         你很小的时候见过他呀 旗真南 就是要小心些好吗 和弟弟玩儿要注意好吗米奇 想我了吗 米奇不要咬人啊小心些 小拉机 布黄你为什么在沙发下面呀\
              事在外运 大家都在外边 我的小乖乖 米奇不可以这样 你在那儿干嘛呢? 它拿不到 它能爬进去吗我觉得只有布茜能爬进去 它可以的就是不怎么舒服\
                   去呀 爱丽丝好像没有数猫大 猫猫在和你贴贴呢 米奇和爱丽丝贴贴爱丽丝就被撞倒了 在比爱丽丝重 米奇不明白你比它还小呢 轻轻地抚摸它吧\
                        爱丽丝弟弟和发动机鼓猫在这边米莎和库恩坐着很漂亮 那个格子很少有猫去 米奇和我们在沙发上 好着"],
                      "entity_list":[u"弟弟", u"小拉机", u"发动机", u"爱丽丝", u"布茜", u"薮猫"]}]}

    # print()
    print(json.dumps(feature_calculate(data), ensure_ascii=False, indent=4))
