#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xuguojin
# @Date:   2022-04-01
"""
Brief:FEATURE_KG_EVENT_GENERAL_EXTRACT_GPU_V1 Demo, 以及压测数据生成的DEMO
Author: xuguojin(xuguojin@baidu.com)
Date: 2022-04-01
Filename: FEATURE_KG_EVENT_GENERAL_EXTRACT_GPU_V1.py
"""
from xvision_demo import XvisionDemo
from util import Util
import json
import base64
import random
import sys
import os

class FeatureReq(XvisionDemo):
    """
    FEATURE_KG_EVENT_GENERAL_EXTRACT_GPU_V1 demo
    """
    def prepare_request(self, data):
        """
        功能：构建算子的输入数据
        输入：
            data：dict类型，算子输入格式
        输出：
            返回算子的输入数据
        """
        return data

def feature_calculate(input_data):
    """
    功能：特征计算
    输入：
        input_data:待计算的文本
    输出：
        切分好的文本特征
    """
    feature_demo = FeatureReq()
    #生成算子输入
    feature_data = feature_demo.prepare_request(input_data)

    job_name = "" #应用名
    token = "" #token
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'resource_key': 'test.txt',
        'auth_key': token,
        'business_name': job_name,
        'feature_name': 'FEATURE_KG_EVENT_GENERAL_EXTRACT_GPU_V1',
        'X_BD_LOGID': str(random.randint(1000000, 100000000))
    }

    #获取url
    #高可用型、均衡型作业：xvision_online_url，高吞吐型作业：xvision_offline_url，测试作业：xvision_test_url
    url = feature_demo.xvision_online_url + feature_demo.xvision_sync_path

    # 高可用型、均衡型作业需将job_name、feature_name放到 url 中
    if feature_demo.xvision_online_url in url:
        params = {
            "business_name": headers["business_name"],
            "feature_name": headers["feature_name"]
        }
    else:
        params = {}

    #请求百度视频中台特征计算服务
    res_data = feature_demo.request_feat_new(params, feature_data, url, headers)
    #打印输出
    feature_demo.parse_result(res_data)

def gen_stress_data(input_file):
    """
    功能：生成压测数据
    输入：
        input_file:待切分文本文件，每一行是一个json字符串
    输出：
        压测数据
    """
    featureDemo = FeatureReq()
    #压测数据生成demo
    with open(input_file, 'r') as f:
        for line in f:
            line = json.loads(line.strip())
            print featureDemo.prepare_request(line)#压测词表数据


if __name__ == '__main__':
    """
    main
    特征计算执行：
        python FEATURE_KG_EVENT_GENERAL_EXTRACT_GPU_V1.py
    生成压测数据：
        python FEATURE_KG_EVENT_GENERAL_EXTRACT_GPU_V1.py GEN_STRESS_DATA
    """
    op_type = sys.argv[1] if len(sys.argv) == 2 else 'FEATURE_CALCULATE'
    if op_type == 'GEN_STRESS_DATA':
        #生成压测词表
        gen_stress_data('./demo.txt')
    else:
        #特征计算Demo

        data = {'data': [{
                        "title": u"芦溪县芦溪镇第二中心学校落实“五项管理”和“双减”工作",
                        "text": u"""芦溪县芦溪镇第二中心学校落实“五项管理”和“双减”工作 新学期教师会(李忠平 供图)\n
                        大江网/萍乡头条客户端讯李忠平报道:为贯彻落实国家“五项管理”“双减”工作要求,进一步实现立德树人的
                        根本任务,近期,芦溪县芦溪镇第二中心学校秉承“幸福教育培育幸福的人”办学理念,积极推进“五项管理”和
                        “双减”工作常态化。\n暑期会议重宣传\n该校积极响应号召,暑假期间专门召开“五项管理”“双减”工作布置
                        会,校长李瑞根在会上详细讲述了“五项管理”和“双减”工作的相关政策。学校通过公众号发布“致家长一封信”、
                        班级微信群等多种形式,大力宣传“五项管理”“双减”工作要求。\n开学会议重强调\n新学期教师会上,李瑞根
                        强调,要准确把握“五项管理”“双减”工作的核心要义。要明确新学期工作重点,在日常教学中,教师要进一步抓
                        实“五项管理”,规范作业布置,创新作业方式,提高课堂教学质量,在“控量”“提质”上下功夫,实现作业“减负增
                        效”的同时“减负不减质”。要根据学校实际制定切实可行的作业管理制度、作业公示制度等措施,全力搭建家校
                        合作平台,确保此项工作落实到位。\n教研会上抓落实\n9月6日,学校召开了新学年教学教研工作专题会。校长
                        李瑞根、党总支书记刘世辉、副校长颜红,教务处全体成员以及各学科教研组长、各年级备课组长参加了本次会议。\n
                        颜红结合当前的“五项管理”和“双减”工作相关文件精神进行了《助力减负提质 促进专业成长》专题培训,明确了
                        教研组长、备课组长的职责,阐述了“五Q幸福树”课程依托“幸福课堂”,实施“求上”“求智”“求健”“求美”“求新”的
                        新理念;提出了年级管理模式下“单周+双周”的教研新特色。她提出,在日常教学中唯有做到“教学五认真”,即认真备
                        课、认真上课、认真批改、认真辅导、认真评价是老师追求专业成长的必由之路。她强调,要加强各学科作业统筹,科
                        学合理布置作业,注重作业形式的多样性和趣味性,以达到轻负担、高质量的目的;强化教师作业批改与反馈的育人功能
                        ,适时展评,力行“减负、降压、增效”。\n最后,李瑞根对本次会议作总结性发言。他充分肯定了教务处、各教研组和备
                        课组的教学教研工作。同时,他提出教育教学质量是学校发展的生命线。他希望各教研组长、备课组长带领老师们认真落
                        实好“双减”与“五项管理”各项要求,凝聚团队的力量,大胆创新,取得实效,为学校教育教学的发展作出贡献。\n制度完善
                        有保障\n开学以来,该校制定了《芦溪镇第二中心学校减轻学生作业负担实施方案》《芦溪镇第二中心学校课后服务实施方案》
                        《芦溪镇第二中心学校作业管理制度》《芦溪镇第二中心学校作业公示制度》等,各教研组和备课组集中学习,力争“双减”工作落实
                        有效。下发了“课后服务致家长的一封信”,自愿参加课后服务的学生上交了申请表,并于第二周开启服务。""",
                        }],
                'mode': 'event'}

        feature_calculate(data)