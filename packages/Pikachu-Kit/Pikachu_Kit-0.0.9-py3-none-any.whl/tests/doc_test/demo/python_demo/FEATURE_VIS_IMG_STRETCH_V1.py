#!/usr/bin/env python
#coding=utf-8
import base64
import urllib2
import json
 
if __name__ == "__main__":
    #url = "http://xvision-api.sdns.baidu.com" #在线业务使用的bns
    #url = "http://group.xvision-xvisionproxy.xVision.all.serv:8089"  #近线业务使用的bns
    url = "http://group.xvision-xvisionproxyoffline.xVision.all.serv:8089" #离线业务使用的bns

    with open('img_file', 'r') as fp: #img_file是图片文件
        img = fp.read()
    data_dict = {
                "business_name": "", #必填，jobname
                "resource_key": "test.jpg", #用于标记图片
                "input_message": {
                        "passthrough_field": "key", #用于标记图片
                        "img_base64": base64.b64encode(img)
                    },
                "auth_key": "", #必填，token
                "feature_list": [
                        {"feature_name": "FEATURE_VIS_IMG_STRETCH_V1"} #算子名称
                    ]
                }
    data = json.dumps(data_dict)
    headers = {"Content-Type": "application/json"}
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    print response.read()
    response.close()
