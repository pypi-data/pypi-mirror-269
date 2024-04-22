#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief: encrpt DEMO
Author: lixin41(lixin41@baidu.com)
Date: 2020-05-26
Filename: bdes.py
"""
import requests

host = 'http://cp01-rd-dongdong01.epc.baidu.com:8126'

def encode(data, binary=1):
    """
    功能: 加密
    输入: 任意文件
    输出: 加密后的文件
    """
    #def encode(data, binary=0):
    url = host + '/bdes/encode?binary=' + ('1' if binary else '0')
    res = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    return res.content, res.headers['X-MIPS-BDES-META']


def decode(dataEncode, dataEncodeMeta, binary=1):
    """
    功能: 解密
    输入: 加密文件
    输出: 解密后的文件
    """
    url = host + '/bdes/decode?binary=' + '1' if binary else '0'
    res = requests.post(url, data=dataEncode, headers={'Content-Type': \
        'application/octet-stream', 'X-MIPS-BDES-META': dataEncodeMeta})
    return res.content


def main():
    """
    功能:
    输入：
    输出:
    """
    data = requests.get('http://cp01-rd-dongdong01.epc.baidu.com:8100/img/test.jpg').content
    print len(data)
    dataEncode, dataEncodeMeta = encode(data)
    print len(dataEncode)
    dataDecode = decode(dataEncode, dataEncodeMeta)
    print len(dataDecode)
    print 'data == dataDecode: ', data == dataDecode


if __name__ == '__main__':
    main()
