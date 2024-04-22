#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
"""
# Authors: fuyi03(@baidu.com)
# Date:    2018/08/30
# Brief:
#    人脸预测服务视频中台调用脚本
#    服务接口文档：http://wiki.baidu.com/display/idlface/FeatureService+V3.0
#    脚本中的参数含义请看接口文档
"""

import urllib2
import json
import time
import base64
import random
import sys


def prepare_image(path, calc_type=3):
    """ read image, set params """
    with open(path, 'rb') as img:
        b64img = base64.b64encode(img.read())
    image = {
        'calc_type': calc_type,
        'live_map_type': 1,
        'imageid': path,
        'image': b64img
    }
    return image


def prepare_input(scene_type=7):
    """ construct input dict """
    input = {
        'logid': 'test_9527',
        'model_version': 'v2',
        'format': 'json',
        'imagesnum': 1,
        'targetfacenum': 1,
        'scene_type': scene_type
    }
    return input


def prepare_req(input, info):
    """ construct request """
    demo = {
        'provider': info['provider'],
        'input': json.dumps(input)
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': info['token'],
        'business_name': info['job'],
        'feature_name': info['feature'],
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }
    url = 'http://' + info['server'] + '/xvision/xvision_sync'
    # 目前版本的视频中台请求必须将作业名和算子名拼在url中，否则就近访问无效
    url += '?business_name=%s&feature_name=%s' % (headers['business_name'], headers['feature_name'])
    req = urllib2.Request(url, data=json.dumps(demo), headers=headers)
    return req


def prepare_info():
    """ return xvision params dict """
    """
    百度视频中台高可用型作业集群: xvision-api.sdns.baidu.com
    百度视频中台高吞吐型作业集群: group.xvision-xvisionproxyoffline.xVision.all.serv:8089
    百度视频中台测试作业集群:group.xvision-xvisionproxytest.xVision.all.serv:8089
    """
    server_info = 'xvision-api.sdns.baidu.com'  # 百度视频中台高可用型作业集群
    return {
        'server': server_info,
        'provider': 'get_feature',  # 根据需求填写，可填内容参考接口文档
        'feature': 'FEATURE_VIS_IMG_FEATURE_FRAME_GPU_OFFLINE',
        'job': '',  # 视频中台上申请的作业名
        'token': ''  # 视频中台申请的作业对应的token
    }


def simple_test(img_path):
    """ one pic test demo """
    xvision_info = prepare_info()
    input = prepare_input(7)  # 不涉及提特征和活体该数字无需关心
    time_start = time.time()
    img = prepare_image(img_path, 1 + 2)  # 需求功能的bitmask,参考接口文档中的calc_type取值,1+2表示检测+72关键点
    images = [img]
    input['images'] = images
    input['imagesnum'] = 1
    req = prepare_req(input, xvision_info)
    res = urllib2.urlopen(req).read()
    time_end = time.time()
    json_data = json.loads(res)
    feature = json_data['feature_result']
    value = json.loads(feature['value'])
    result = value['output']
    print result
    cost_ms = (time_end - time_start) * 1000
    print 'cost(ms):%f' % cost_ms


if __name__ == '__main__':
    simple_test(sys.argv[1])
