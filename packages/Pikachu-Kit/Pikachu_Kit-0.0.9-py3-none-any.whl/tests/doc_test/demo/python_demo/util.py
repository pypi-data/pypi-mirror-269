#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Brief:百度视频中台特征计算工具类
Author: wanghua11(wanghua11@baidu.com)
Date: 2019-07-29
Filename: util.py
"""
import urllib3 as urllib2
# import urllib.request as urllib2

class Util():
    """
    工具类
    """
    @staticmethod
    def read_file(file_name):
        """
        功能：从本地文件中读取内容
        输入：
            file_name(本地文件名)
        输出：
            file_name中的内容,异常返回None
        """
        try:
            print("file_name",file_name)
            with open(file_name, 'rb') as fp:
                image = fp.read()
            return image
        except Exception as e:
            print( 'Failed read file:{}. Exception:{}'.format(file_name, str(e)))
            return None

    @staticmethod
    def read_video_image_file(file_name):
        """
        功能：从本地文件中读取内容
        输入：
            file_name(本地文件名)
        输出：
            file_name中的内容,异常返回None
        """
        try:
            video_info_list = []
            with open(file_name, 'r') as fp:
                for line in fp:
                    if len(line.split()) != 2:
                        continue
                    video_info_list.append({
                        'image_url': line.split()[0],
                        'video_url': line.split()[1]
                    })
            return video_info_list
        except Exception as e:
            print ('Failed read file:{}. Exception:{}'.format(file_name, str(e)))
            return None


    @staticmethod
    def read_video_file(file_name):
        """
        功能：从本地文件中读取内容
        输入：
            file_name(本地文件名)
        输出：
            file_name中的内容,异常返回None
        """
        try:
            video_info_list = []
            with open(file_name, 'r') as fp:
                for line in fp:
                    video_info_list.append({
                        'title': line.split()[0],
                        'video_url': line.split()[1]
                    })
            return video_info_list
        except Exception as e:
            print('Failed read file:{}. Exception:{}'.format(file_name, str(e)))
            return None

    


    @staticmethod
    def read_url(url, t=3):
        """
        功能：url下载
        输入：
            url（视频/图片/音频）
        输出：
            视频/图片/音频的内容,异常返回None
        """
        try:
            req = urllib2.Request(url)
            req.add_header('Referer', 'http://www.baidu.com')
            url_bytes = urllib2.urlopen(req, timeout=t).read()
            if url_bytes is None or len(url_bytes) <= 0:
                return None
            return url_bytes
        except Exception as e:
            print("Retrieve {} Exception:{}".format(url, str(e)))
            return None
