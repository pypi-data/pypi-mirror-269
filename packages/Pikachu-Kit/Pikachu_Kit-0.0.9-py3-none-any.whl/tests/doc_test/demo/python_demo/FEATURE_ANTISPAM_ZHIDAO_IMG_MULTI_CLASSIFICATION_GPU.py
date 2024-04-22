#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_ANTISPAM_ZHIDAO_IMG_MULTI_CLASSIFICATION_GPU Demo, �Լ�ѹ���������ɵ�DEMO
Author: niushixiong(niushixiong01@baidu.com)
Date: 2023-11-01
Filename: FEATURE_ANTISPAM_ZHIDAO_IMG_MULTI_CLASSIFICATION_GPU.py
"""
import os

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import requests


def feature_calculate(url="", xvision_online_url="", job_name="", 
                      feature_name="", qid="", rid='', cont="", image_arr=None):
    """
    ���ܣ���������
    ���룺
        url,xvision_online_url,job_name,feature_name,title,cont
    �����
        none        
    """
    token = ''
    logid = str(random.randint(1000000, 100000000))
    request_ip = ""

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': feature_name,
    }
    # �߿����͡���������ҵ�轫job_name��feature_name�ŵ� url ��
    if xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {
            "business_name": job_name,
            "feature_name": feature_name
        }

    data = {
        "req": {"text": cont, "image_arr": image_arr, "qid": qid, "rid": rid},
        "model_type": "IrrelevantBertBlendCNNModel",
        "business_name": job_name,
        "feature_name": feature_name,
        "logid": logid,
        "request_ip": request_ip
    }
    try:
        request_json = json.dumps(data)
    except:
        request_json = json.dumps(data, encoding='gb18030')
    res = requests.post(url, params=params, data=request_json, headers=headers)
    # ��ӡ���
    print(res.json())


def prepare_request(qid, rid, cont, image_arr, job_name="", feature_name=""):
    """
    ���ܣ��������ӵ���������
    ���룺qid, rid, cont, image_arr, job_name, feature_name
    ����� requst_json
    """
    logid = str(random.randint(1000000, 100000000))
    request_ip = "10.23.4.55"
    data = {
        "req": {"text": cont, 
                "image_arr": image_arr,
                "qid": qid,
                "rid": rid
                },
        "model_type": "IknowMultModalBertVitModel",
        "business_name": job_name,
        "feature_name": feature_name,
        "logid": logid,
        "request_ip": request_ip
    }
    try:
        request_json = json.dumps(data)
    except:
        request_json = json.dumps(data, encoding='gb18030')
    return request_json


def gen_stress_data():
    """
    ���ܣ�����ѹ������
    �����
        ѹ������
    """
    job_name = ""
    feature_name = ""
    for line in sys.stdin:
        sp = line.split("\t")
        qid = sp[0]
        rid = sp[1]
        cont = sp[2]
        cont = cont.decode("gb18030", "ignore")
        image_base64data = sp[3]
        image_arr = [image_base64data]
        print(prepare_request(qid, rid, cont, image_arr,
              job_name=job_name, feature_name=feature_name))


if __name__ == '__main__':
    """
    main
    """
    # �߿����͡���������ҵ��xvision_online_url������������ҵ��xvision_offline_url��������ҵ��xvision_test_url
    xdemo = XvisionDemo()
    url = xdemo.xvision_online_url + xdemo.xvision_sync_path
    job_name = ""
    feature_name = ""

    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # ����ѹ������
        gen_stress_data()
    else:
        # ��������Demo
        qid = "1111111"
        rid = "222222"
        cont = "����Ѷ������ƵAPP�汾:8.2.78.21637Ϊ����������Ѷ��Ƶ�ڲ�ͬ�˺�֮���Ա\
            Ȩ�治��ͨ��ʹ�ÿ�ͨ�Ļ�Ա�˺ŵ�¼��Ѷ��Ƶ��Ӱ������ʾ�ǻ�Ա�����˳��ʺ����µ�\
            ¼�鿴���ͻ��˰汾����Ҳ�ᵼ�»�Ա״̬��ʾ����ȷ��������Գ����������ذ���\
            ��װ����Ѷ��Ƶ�ͻ����ٵ�¼�鿴�˴ֲᡣ��fh.ihzg.com.cn/news/30591.mp3����vq.51mg.cn/news/01267.mp3��"
        image_base64_arr = ['f+QRnHHmlr1HU+jj8X2bh2NX0MNGPIVqLOWK7eBgPT/g+aspNb2AH5rr6']
        feature_calculate(url, xdemo.xvision_online_url,
                          job_name, feature_name, qid=qid, rid=rid, cont=cont, image_arr=image_base64_arr)
