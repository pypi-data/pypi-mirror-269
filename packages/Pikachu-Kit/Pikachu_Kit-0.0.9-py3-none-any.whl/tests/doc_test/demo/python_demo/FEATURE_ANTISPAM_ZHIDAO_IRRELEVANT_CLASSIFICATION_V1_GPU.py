#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
Brief:FEATURE_ANTISPAM_ZHIDAO_IRRELEVANT_CLASSIFICATION_V1_GPU Demo, �Լ�ѹ���������ɵ�DEMO
Author: niushixiong(niushixiong01@baidu.com)
Date: 2023-09-01
Filename: FEATURE_ANTISPAM_ZHIDAO_IRRELEVANT_CLASSIFICATION_V1_GPU.py
"""
import os

from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import requests


def feature_calculate(url="", xvision_online_url="", job_name="", feature_name="", title="", cont=""):
    """
    ���ܣ���������
    ���룺
        url,xvision_online_url,job_name,feature_name,title,cont
    �����
        none        
    """
    token = ''
    logid = str(random.randint(1000000, 100000000))
    request_ip = "10.23.4.55"

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
        "req": {"text_a": title, "text_b": cont},
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


def prepare_request(title, cont, job_name="", feature_name=""):
    """
    ���ܣ��������ӵ���������
    ���룺tile, content, job_name, feature_name
    ����� requst_json
    """
    logid = str(random.randint(1000000, 100000000))
    request_ip = "10.23.4.55"
    data = {
        "req": {"text_a": title, "text_b": cont},
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
        title = sp[0]
        cont = sp[1]
        title = title.decode("gb18030", "ignore")
        cont = cont.decode("gb18030", "ignore")
        print(prepare_request(title, cont,
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
        title = "ɽ�����ն�����Һѹ������QQ���Ƕ��٣�"
        cont = "����Ѷ������ƵAPP�汾:8.2.78.21637Ϊ����������Ѷ��Ƶ�ڲ�ͬ�˺�֮���Ա\
            Ȩ�治��ͨ��ʹ�ÿ�ͨ�Ļ�Ա�˺ŵ�¼��Ѷ��Ƶ��Ӱ������ʾ�ǻ�Ա�����˳��ʺ����µ�\
            ¼�鿴���ͻ��˰汾����Ҳ�ᵼ�»�Ա״̬��ʾ����ȷ��������Գ����������ذ���\
            ��װ����Ѷ��Ƶ�ͻ����ٵ�¼�鿴�˴ֲᡣ��fh.ihzg.com.cn/news/30591.mp3����vq.51mg.cn/news/01267.mp3��"
        feature_calculate(url, xdemo.xvision_online_url,
                          job_name, feature_name, title=title, cont=cont)
