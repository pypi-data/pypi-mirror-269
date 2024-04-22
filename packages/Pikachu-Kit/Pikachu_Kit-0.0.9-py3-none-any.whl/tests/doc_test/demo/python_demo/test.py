#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: yexiang02@baidu.com
Date: 2020-02-26
"""
from util import Util
from xvision_demo import XvisionDemo
import json
import base64
import urllib2
import sys
import os

if __name__ == '__main__':
    """
    main
    """
    package = sys.argv[1]
    port = sys.argv[2]
    model = __import__(package)
    func = getattr(model, 'FeatureReq')
    demo_img_list = os.listdir('./image_dir/demo_img')
    demo_name_type = [package + x for x in ['.jpg', '.png']]
    img_path = './image_dir/test.jpg'
    for img in demo_name_type:
        if img in demo_img_list:
            img_path = './image_dir/demo_img/' + img
            break
        else:
            continue
    input_data = img_path
    print input_data
    data = {
        "image": Util.read_file(input_data),
        "video_url": "https://xvision-media.bj.bcebos.com/small_video/small_test1.mp4",
        "video_title": "video_title",
        "title": "title"
    }
    feature_data = func().prepare_request(data)
    # url = 'http://0.0.0.0:' + str(port) + '/GeneralClassifyService/classify'
    url = 'http://0.0.0.0:' + str(port) + sys.argv[3]
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    try:
        request = urllib2.Request(url=url, headers=headers, data=feature_data)
        response = urllib2.urlopen(request, timeout=10)
        res = response.read()
        print res
    except Exception as e:
        print "post request error[{error}]".format(error=str(e))
