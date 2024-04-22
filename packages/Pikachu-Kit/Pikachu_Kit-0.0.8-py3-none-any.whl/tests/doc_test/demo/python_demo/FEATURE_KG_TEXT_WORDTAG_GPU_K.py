#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Huapeng Qin
# @Date:   2020-12-22 19:28:40
# @Last Modified by:   Huapeng Qin
# @Last Modified time: 2020-12-23 18:28:56
"""
Brief:FEATURE_KG_TEXT_WORDTAG_GPU_K Demo, 以及压测数据生成的DEMO
Author: Huapeng Qin(qinhuapeng@baidu.com)
Date: 2020-12-22
Filename: FEATURE_KG_TEXT_WORDTAG_GPU_K.py
"""
import asyncio
import json
import time

import tornado

from xvision_demo import XvisionDemo


class FeatureReq(XvisionDemo):
    """
    FEATURE_KG_TEXT_WORDTAG_GPU demo
    """

    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：string类型，待计算的文本
        输出：
            返回算子的输入数据
        """

        return json.dumps({
            'data': [data]
        })


async def feature_calculate(feature_req: str, url, xvision_data):
    """Calcluate wordtag feature.

    Arguments:
        input_data {typing.List[str]} -- input text data.
    """
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X_BD_LOGID": f"{feature_req.logid}"
    }

    req = tornado.httpclient.HTTPRequest(
        url=url, method="POST", headers=headers, body=xvision_data
    )
    http_client = tornado.httpclient.AsyncHTTPClient()
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
        print(e)
    finally:
        http_client.close()


async def run(feature_reqs, url, input_data):
    res_list = await asyncio.gather(
        *(feature_calculate(r, url, d) for r, d in zip(feature_reqs, input_data))
    )
    return res_list


def gen_async_data(input_data_raw, job_name, token, feature_name):
    input_data, req_list, logid_list = ([] for _ in range(3))
    for text in input_data_raw:
        feature_req = FeatureReq()
        feature_input = feature_req.prepare_request(text)
        xvision_data = feature_req.gen_xvision_data({
            "business_name": job_name,
            "resource_key": "test.jpg",
            "auth_key": token,
            "feature_name": feature_name,
            "feature_input_data": feature_input
        })
        input_data.append(json.dumps(xvision_data))
        logid_list.append(feature_req.logid)
        req_list.append(feature_req)
    return input_data, req_list, logid_list


if __name__ == "__main__":
    import urllib

    JOB_NAME = ""
    TOKEN = ""
    FEATURE_NAME = "FEATURE_KG_TEXT_WORDTAG_GPU_K"

    params = {
        "business_name": JOB_NAME,
        "feature_name": FEATURE_NAME
    }
    params = urllib.parse.urlencode(params)
    tmp_feature_req = FeatureReq()
    url = f"{tmp_feature_req.xvision_online_url}{tmp_feature_req.xvision_sync_route}?{params}"
    # url = f"http://wordtag.paddle.baidu.com{tmp_feature_req.xvision_sync_route}?{params}"

    input_data_raw = ["美人鱼是周星驰导演的电影"]
    input_data, req_list, logid_list = gen_async_data(
        input_data_raw, JOB_NAME, TOKEN, FEATURE_NAME
    )
    res_list = asyncio.run(run(req_list, url, input_data))
    res = json.loads(res_list[0]["feature_result"]["value"])
    print(json.dumps(res["results"][0], ensure_ascii=False, indent=4))
