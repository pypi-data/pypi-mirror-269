#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Author: yangbing05
Date: 2022-03-14 15:21:43
Description: 网盘图片匹配文案
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import requests
import urllib
import sys
import os

feature_name = 'FEATURE_NETDISK_IMG_MATCH_TEXT_GPU_V3'

class FeatureReq(XvisionDemo):
    """
    prepare request param 
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子处理对象（image，video_url，audio等）以及必须的额外字段
        输出：
            返回算子的输入数据
        """
        logid = str(random.randint(1000000, 100000000))
        ecrypted_str, meta_str = bdes_encode(json.dumps(data), 0)
        data_str = base64.b64encode(ecrypted_str).decode()
        req_data = {
            'appid': '123456',
            'logid': logid,
            'format': 'json',
            'from': 'test-python',
            'cmdid': '123',
            'clientip': '127.0.0.1',
            'data': data_str,
        }
        return json.dumps(req_data), meta_str
    
    def parse_result(self, res_data):
        """
        功能：解析算子的输出结果
        输入：
            res_data：算子的输出结果
        输出：
            算子输出结果
        """
        res_json = {}
        try:
            res_json = json.loads(res_data)
        except Exception as e:
            print 'response json format or content error:{}'.format(e)
            return
        if res_json['err_no'] == 0:
            if res_json.get("encrypted") == "bdes":
                reseult_data = base64.b64decode(res_json['result'].encode()).decode()
                reseult_data = bdes_decode(reseult_data, res_json.get("metainfo"), 0)
                res_json['result_decode'] = json.loads(reseult_data)
            else:
                reseult_data = json.loads(res_json['result'])
                res_json['result_decode'] = reseult_data
            return res_json
        else:
            print "err_no = %d, err_msg = %s" % (res_json['err_no'], res_json['err_msg'])
            
        return None


bdes_host = 'http://10.24.4.208:8305'

def bdes_encode(data, binary=1):
    """
    功能: 加密
    输入: 任意文件
    输出: 加密后的文件
    """
    #def encode(data, binary=0):
    url = bdes_host + '/bdes/encode?binary=' + ('1' if binary else '0')
    res = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    return res.content, res.headers['X-MIPS-BDES-META']
 
 
def bdes_decode(dataEncode, dataEncodeMeta, binary=1):
    """
    功能: 解密
    输入: 加密文件
    输出: 解密后的文件
    """
    url = bdes_host + '/bdes/decode?binary=' + ('1' if binary else '0')
    res = requests.post(url, data=dataEncode, headers={'Content-Type': \
        'application/octet-stream', 'X-MIPS-BDES-META': dataEncodeMeta})
    
    return res.content


def feature_calculate(dlink, topk=10):
    """
    功能：特征计算
    输入：
        input_data: 本地图片文件
        out_file: 处理后，保存的图片文件
    输出：
        图片特征
    """
    featureDemo = FeatureReq()
    #生成算子输入
    data = {
        'dlink': dlink,
        'k': topk,
    }
    feature_data, bdes_meta = featureDemo.prepare_request(data)
    job_name = ""  # 申请的作业名
    token = ""  # 作业的token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.jpg',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': feature_name,
        'X_BD_LOGID': str(random.randint(1000000, 100000000)),
        'X-VIS-DATA-ENCRYPTED': 'bdes',
        'X-VIS-ENCRYPT-METAINFO': bdes_meta,
        'X-VIS-RESPONSE-ENCRYPTED': 'bdes',
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
    result = featureDemo.parse_result(res_data)
    if not result is None:
        print 'service response ok'
        print json.dumps(result)
    else:
        print 'service response error'


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
    img_file_list = sorted(os.listdir(input_dir)) #input_dir里边是图片列表，用于生成压测词表
    for i in range(12):
        for image_file in img_file_list:
            data = {
                'dlink': 'http://yangbing05.bcc-bdbl.baidu.com:8100/image_match_text/{}'.format(image_file), # 图片文件的下载地址
                'k': 20
            }
            print featureDemo.prepare_request(data)#压测词表数据

if __name__ == '__main__':
    """
    main
    特征计算执行：
        python filename.py 
    生成压测数据：
        python filename.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # 生成压测词表
        gen_stress_data('./image_dir/{}/'.format(feature_name))
    else:
        # 特征计算Demo
        feature_calculate('http://yangbing05.bcc-bdbl.baidu.com:8100/image_match_text/1.jpg')
