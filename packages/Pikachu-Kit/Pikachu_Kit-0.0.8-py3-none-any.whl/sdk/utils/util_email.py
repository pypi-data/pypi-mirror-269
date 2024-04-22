# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_email.py
@time: 2024/3/7 11:29 
@desc: 

"""
import smtplib
from email.mime.text import MIMEText

class EmailSend(object):
    """

    """
    def __init__(self, recv_list, title_list, content_list):
        self.mail_host = "smtp.163.com"
        self.password = "VRLOQJOUKANMYZEX"
        self.sender = "JHC000abc@163.com"
        self.title_list = title_list
        self.content_list = content_list
        if recv_list:
            self.recv_list = recv_list

    def init_message(self, receiver, title, content):
        """

        :return:
        """
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = title
        message['From'] = self.sender
        message['To'] = receiver
        return message

    def send_email(self , receiver, message):
        """

        :param receiver:
        :param message:
        :return:
        """
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(self.mail_host, 25)
            # 登录到服务器
            smtpObj.login(self.sender, self.password)
            # 发送
            smtpObj.sendmail(
                self.sender, receiver, message.as_string())
            # 退出
            smtpObj.quit()
            print(f'{receiver} send success')
        except smtplib.SMTPException as e:
            print(f'{receiver} send failed')
            print('error', e)  # 打印错误


    def main(self):
        """

        :return:
        """
        for recv, title, content in zip(self.recv_list,self.title_list,self.content_list):
            message = self.init_message(recv, title, content)
            self.send_email(recv, message)


if __name__ == '__main__':
    recv_list, title, content = ["JHC000abc@gmail.com", "v_jiaohaicheng@baidu.com"],["警告","提示"],["严重错误","严重错误2"]
    es = EmailSend(recv_list, title, content)
    es.main()