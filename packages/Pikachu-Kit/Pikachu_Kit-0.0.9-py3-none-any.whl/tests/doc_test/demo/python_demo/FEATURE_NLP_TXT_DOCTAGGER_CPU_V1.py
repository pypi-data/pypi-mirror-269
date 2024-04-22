#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:FEATURE_NLP_TXT_DOCTAGGER_CPU_V1 Demo, 以及压测数据生成的DEMO
Author: liqinrui(liqinrui@baidu.com)
Date: 2021-05-07
Filename: FEATURE_NLP_TXT_DOCTAGGER_CPU_V1.py 
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import urllib
import sys
import os

class FeatureReq(XvisionDemo):
    """
    FEATURE_NLP_TXT_DOCTAGGER_CPU_V1 demo  
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：json串，参考示例
        输出：
            返回算子的输入数据
        """

        return json.dumps({
                    'appid': '123456',
                    'logid': random.randint(1000000, 100000000),
                    'format': 'json',
                    'from': 'test-python',
                    'cmdid': '123',
                    'clientip': '0.0.0.0',
                    'data': base64.b64encode(data),
                })


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_NLP_TXT_DOCTAGGER_CPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    # 高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = featureDemo.xvision_test_url + featureDemo.xvision_sync_path
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
    file_list = sorted(os.listdir(input_dir)) #dir里边是文本列表，用于生成压测词表
    for file in file_list:
        with open(input_dir + '/' + file, "r") as fd:
            for line in fd:
                print featureDemo.prepare_request(line)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_NLP_TXT_DOCTAGGER_CPU_V1.py 
    生成压测数据：
        python FEATURE_NLP_TXT_DOCTAGGER_CPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./text_dir/') #./dir/ 是本地的文本数据
    else:
        #特征计算Demo
        feature_calculate('{"title": "苹果WWDC 2018将在6月4日开幕 今年有何惊喜？","content": \"3月14日消息，据《福布斯》网站报道，\
            第29届苹果全球开发者大会（WWDC）将在2018年6月4日至8日举办。地点与同去年一样，仍在美国加州圣何塞的McEnery会议中心。通常， 苹果\
            会在大会中发布新一代iOS系统以及Apple TV、 watchOS和macOS的软件更新。 去年大会发布的更新包括iPhone的“ 驾驶时勿扰（ Do Not \
            Disturb While Driving）” 功能、 全新设计的应用商店、 游戏《 纪念碑谷2》 的iOS版本、 iPad版的iOS 11 更新以及在表盘融入《 \
            玩具总动员》 角色的watchOS 4。除了软件， 去年苹果还一口气推出三款新产品： iMac Pro、 10.5 英寸iPadPro和智能音箱HomePod。\
            今年的WWDC大会将带来怎样的期待？软件方面， 大会上很可能将发布macOS 10.14、 watchOS 5、 tvOS 12 以及iOS 12。如果传闻确切，\
            一款新iPad很快将亮相。 不过发布时间上有两种可能。 一是在WWDC大会前发布， 就像去年4月初苹果就发布了一款入门级平板。 iPad Pro \
            10.5 就是在去年大会中亮相的， 从这一点来看， 今年的大会也有可能新推一款带人脸识别功能FaceID的iPad。Mac方面也是猜测多多。 或许\
            会推出一款Mac Pro升级版本。 有消息爆出会有一款全新的入门级MacBook,可能是配备Retina屏的MacBook Air。有传闻称此次大会将发布新\
            款iPhone SE。 不过上一款在WWDC大会上公布的是iPhone 4， 鉴于这一点， 这一传闻并不可信。谁将参加？开发项目成员或开发企业成员才有\
            资格注册参与， 而且门票售价高达1599美元， 但按照往年情况门票很快就会一售而空。在主题演讲之后， 大会将举办动手实验活动、 互动交流环\
            节以及100多场技术和设计会议。想要参加今年的WWDC大会， 现在就可以注册购买门票。 注册时间截止到3月22日早上10点（ 太平洋时间）。 苹果\
            会从所有注册者随机选择一些人发放门票， 结果将在3月23日下午5点前公布。苹果向学生开放了350个免费参加名额。 苹果表示，“ 学生是苹果开发\
            者群体不可或缺的一部分。 今年将向350名学生开发者和STEM组织成员提供WWDC奖学金,他们将获得免费参加WWDC大会的机会。" }') # 本地文本
