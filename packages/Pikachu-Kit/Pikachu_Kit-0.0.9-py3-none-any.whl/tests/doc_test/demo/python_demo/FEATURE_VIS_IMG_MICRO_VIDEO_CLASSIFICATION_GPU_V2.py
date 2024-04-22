#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V2 Demo
Author: zhouzhichao01(zhouzhichao01@baidu.com)
Author update: zhouzhichao01(zhouzhichao01@baidu.com)
Date: 2021-03-10
Filename: FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V2.py
"""

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import urllib
import sys
import os
import random
import commands
import glob

from proto.FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V1 import video_pb2
from proto.FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V1.protobuf_to_dict import protobuf_to_dict


class FeatureReq(XvisionDemo):
    """
    FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V2 demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """

        def prepare_data(frame_list, audio_file):
            """
            功能：读取帧序列和音频文件
            输入：
                frame_list: 视频帧序列
                audio_file: 音频文件
            输出：
                proto序列化的文件
            """
            proto_data = video_pb2.VideoData()
            with open(audio_file, 'rb') as f:
                proto_data.audio = f.read()

            for idx, fname in enumerate(frame_list):
                frame = proto_data.frames.add()
                with open(fname, 'rb') as f:
                    frame.frame_data = f.read()
                frame.frame_id = idx
            data = proto_data.SerializeToString()

            return data

        logid = random.randint(1000000, 100000000)
        data = prepare_data(data['frame_list'], data['audio_file'])
        clientip = commands.getoutput("hostname")

        req_array = {
            'appid': '123456',
            'logid': logid,
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': clientip,
            'data': base64.b64encode(data),
        }

        req_json = json.dumps(req_array)
        return req_json

    def parse_result(self, resp_json):
        """
        功能：解析算子的输出结果
        输入：
            resp_json：算子的输出结果
        输出：
            算子输出结果
        """
        # resp_json = json.loads(res_data)
        if resp_json['err_no'] == 0:
            res_json = json.loads(base64.b64decode(resp_json['result']))
        else:
            print('Request failed with err_no: %d, err_msg: %s...' % (resp_json['err_no'], resp_json['err_msg']))
            return 0
        
        label = res_json.get('label', '')
        for lab in label:
            subcid_list = []
            for kk, vv in lab.items():
                if kk != "sub_label":
                    cid = kk.encode('utf-8')
                    cid_prob = vv
                else:
                    for subcid in vv:
                        subcid_label = subcid.keys()[0]
                        subcid_prob = subcid[subcid_label]
                        subcid_list.append(subcid_label.encode('utf-8'))
                        subcid_list.append(str(subcid_prob))
            print("Predict labels: %s, probility: %.4f" % (cid, cid_prob))
            print("Predict sublabels: %s" % (",".join(subcid_list)))

        feature = res_json.get('feature_512', [])
        print("Feature_512: ")
        print(len(feature), feature[:3], feature[-3:])

        feature = res_json.get('feature_256', [])
        print("Feature_256:")
        print(len(feature), feature[:3], feature[-3:])

        feature = res_json.get('feature_audio', [])
        print("Feature_audio: ")
        print(len(feature), feature[:3], feature[-3:])


def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:本地图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    # 生成算子输入
    feature_data = featureDemo.prepare_request(input_data)

    job_name = ""  # 申请的作业名
    token = ""   # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V2',
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
    res_data = json.loads(res_data)
    print(res_data)
    if (("code" in res_data)
            and (res_data["code"] == 0)
            and ("feature_result" in res_data)
            and ("value" in res_data['feature_result'])):
        res_json = json.loads(res_data['feature_result']['value'])

    # 打印输出
    featureDemo.parse_result(res_json)


def gen_stress_data(input_dir):
    """
    功能：生成压测数据
    输入：
        input_data:（视频/图片/音频）
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    # 压测数据生成demo
    infile = './image_dir/FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V1/images_audios_list.txt'
    images_audios_list = open(infile, 'r').readlines()
    for line in images_audios_list:
        frame_dir, audio_file = line.strip().split()
        frame_list = sorted(glob.glob(os.path.join(frame_dir, "*.jpg")))
        data = {'frame_list': frame_list, 'audio_file': audio_file}
        print(featureDemo.prepare_request(data))  # 压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_VIS_IMG_MICRO_VIDEO_CLASSIFICATION_GPU_V2.py
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('')  # ./image_dir/ 是本地的图片数据
    else:
        # 特征计算Demo
        frame_list = sorted(glob.glob("image_dir/frames/1/*.jpg"))
        audio_file = "wav_dir/1.wav"
        feature_calculate({'frame_list': frame_list, 'audio_file': audio_file})

