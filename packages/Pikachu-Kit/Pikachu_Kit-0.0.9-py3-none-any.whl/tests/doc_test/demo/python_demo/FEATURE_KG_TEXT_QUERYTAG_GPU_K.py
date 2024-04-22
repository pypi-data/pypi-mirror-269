# !/usr/bin/env python3
# coding=utf-8
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide configure file management service in i18n environment.

Authors: Guoxin Zhang(zhangguoxin@baidu.com)
Date:    2022年02月24日 星期四 17时16分52秒
"""

import sys 
import json 
import time
import asyncio 
import logging 
import urllib
import random
import base64
import argparse

from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class QuerytagFeatureReq():
    """ QuerytagFeatureReq 
    """
    def __init__(self):
        """ __init__
        """
        self.xvision_online_url = 'http://xvision-api.sdns.baidu.com'       # 百度视频中台高可用型作业集群
        self.xvision_sync_path = '/xvision/xvision_sync'                    # 百度视频中台接口的path，不同算子不同，具体算子demo中写清楚
        self.headers = {'Content-Type': 'application/json; charset=UTF-8'}  # 添加请求头
        self.logid = random.randint(100000000, 10000000000)                 # initialize logid

    def prepare_request(self, data):
        """ 构建算子的输入数据
        input = {
            'data': {
                'text': '百度科技园在哪里',  @必填项
                'emb': ['cls'],           @可选项, 可选择['cls', 'last_avg', 'last2avg', 'first_last_avg']输出对应embedding结果
            }
        }
        """
        return json.dumps({'data': {'text': data}})

    def gen_xvision_data(self, argv_dict):
        """ 生成百度视频中台输入(适用于/xvision/xvision_sync接口)
        """
        return {
            "business_name": argv_dict['business_name'],    #作业名
            "resource_key": argv_dict['resource_key'],
            "auth_key": argv_dict['auth_key'],              # token
            "feature_name": argv_dict['feature_name'],      # 算子名
            "data": base64.b64encode(argv_dict['feature_input_data'].encode()).decode()
        }


async def feature_calculate(feature_req, url, xvision_data):
    """ calcluate querytag feature.
    """
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X_BD_LOGID": f"{feature_req.logid}"
    }
    req = HTTPRequest(
        url=url, method="POST", headers=headers, body=xvision_data
    )
    http_client = AsyncHTTPClient()
    try:
        for _ in range(10):
            resp = await http_client.fetch(req)
            if resp.code == 200:
                resp_data = json.loads(resp.body.decode("utf-8"))
                if resp_data["code"] == 0:
                    return resp_data
                    break
            time.sleep(1)
    except Exception as e:
        logging.debug(f'err mes:{e}, xvision_data:{xvision_data}, feature_req:{feature_req}')
    finally:
        http_client.close()


async def run(feature_reqs, url, input_data):
    """ run
    """
    res_list = await asyncio.gather(
        *(feature_calculate(r, url, d) for r, d in zip(feature_reqs, input_data))
    )
    return res_list 


def gene_async_data(input_data_raw, job_name, token, feature_name):
    """ gene async data
    """
    input_data, req_list, logid_list = ([] for _ in range(3))
    for text in input_data_raw:
        feature_req = QuerytagFeatureReq()
        feature_input = feature_req.prepare_request(text)
        xvision_date = feature_req.gen_xvision_data({
            'business_name': job_name, 
            'resource_key': 'test.txt',
            'auth_key': token, 
            'feature_name': feature_name,
            'feature_input_data': feature_input
        })
        input_data.append(json.dumps(xvision_date))
        logid_list.append(feature_req.logid)
        req_list.append(feature_req)
    return input_data, req_list, logid_list


def querytag_predict(job_name, feature_name, token):
    """ querytag predict
    """
    params = {
        "business_name": job_name,
        "feature_name": feature_name
    }
    params = urllib.parse.urlencode(params)
    tmp_feature_req = QuerytagFeatureReq()
    url = f"{tmp_feature_req.xvision_online_url}{tmp_feature_req.xvision_sync_path}?{params}"

    batch_size = 10
    input_data_raw = []
    for line in sys.stdin:
        if line.strip() == '':
            continue 
        query = line.strip()
        input_data_raw.append(query)
        if len(input_data_raw) < batch_size:
            continue 
        else:
            input_data, req_list, _ = gene_async_data(input_data_raw, job_name, token, feature_name)
            input_data_raw = []
            predict_result = asyncio.run(run(req_list, url, input_data))
            assert len(predict_result) == len(input_data)
            for res in predict_result:
                if res is None:
                    continue
                res = json.loads(res["feature_result"]["value"])
                print(json.dumps(res["results"][0], ensure_ascii=False))
    if len(input_data_raw) > 0:
        input_data, req_list, _ = gene_async_data(input_data_raw, job_name, token, feature_name)
        input_data_raw = []
        predict_result = asyncio.run(run(req_list, url, input_data))
        assert len(predict_result) == len(input_data)
        for res in predict_result:
            if res is None:
                continue
            res = json.loads(res["feature_result"]["value"])
            print(json.dumps(res["results"][0], ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_name", default=None, type=str, required=True)
    parser.add_argument("--feature_name", default=None, type=str, required=True)
    parser.add_argument("--token", default=None, type=str, required=True)
    args = parser.parse_args()

    querytag_predict(args.job_name, args.feature_name, args.token)