#!/usr/bin/env python
# coding=utf-8
"""
Author: gaoyangfan@baidu.com
since: 2022-06-20 21:15:09
LastTime: 2022-06-20 21:33:43
LastAuthor: gaoyangfan@baidu.com
message: FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU Demo, �Լ�ѹ���������ɵ�DEMO
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
    FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU demo
    """

    def prepare_request(self, data):
        """
        ���ܣ��������ӵ���������

        Args:
            data (dict): ���������ı��ʹ�ת�����, key is (text, style), style is optional

        Returns:
            [str]: �������ӵ���������
        """
        return json.dumps(data)


def feature_calculate(input_data):
    """
    ���ܣ���������

    Args:
        input_data (dict): ���������ı��ʹ�ת�����, key is (text, style), style is optional
    Returns:
        ���ת����Ľ��
    """
    feature_demo = FeatureReq()
    # ������������
    feature_data = feature_demo.prepare_request(input_data)

    job_name = ""  # Ӧ����
    token = ""  # token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': '',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    # ��ȡurl
    # �߿����͡���������ҵ��xvision_online_url������������ҵ��xvision_offline_url��������ҵ��xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path
    # url = feature_demo.xvision_test_url + feature_demo.xvision_sync_path

    # �߿����͡���������ҵ�轫job_name��feature_name�ŵ� url ��
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    # ����ٶ���Ƶ��̨�����������
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)

    res_data = json.loads(res_data)
    res_data['feature_result']['value'] = json.loads(res_data['feature_result']['value'])
    return res_data


def gen_stress_data(input_file):
    """
    ���ܣ�����ѹ������
    ���룺
        input_file:����ָ���ı���json ��ʽ�� dict, key �� text �� style(��ѡ)��ÿһ����һ��json�ַ���
    �����
        ѹ������
    """
    featureDemo = FeatureReq()
    # ѹ����������demo
    with open(input_file, 'r') as f:
        for line in f:
            line = json.loads(line.strip())
            print(featureDemo.prepare_request(line))


if __name__ == '__main__':
    """
    main
    ��������ִ�У�
        python FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU.py
    ����ѹ�����ݣ�
        python FEATURE_UNIT_TEXT_STYLE_TRANSFER_GPU.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        # ����ѹ��ʱ�
        gen_stress_data('./text_dir/dialog_style_transfer_test_data')  # ���صĲ�������
    else:
        # ���ת��Demo
        feature_calculate({'text': '���Ƿ��ת������', 'style': 0})
