# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: tt5.py
@time: 2023/12/20 17:02 
@desc: 

"""
import json
import base64
from PIL import Image
from io import BytesIO
from sdk.utils.util_network import NetWorkRequests
from sdk.utils.util_folder import FolderProcess


class CreateModuleHuman(object):
    """

    """

    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        self.url_upload = "https://akhaliq-animeganv2.hf.space/api/queue/push/"
        self.url_download = "https://akhaliq-animeganv2.hf.space/api/queue/status/"
        self.net = NetWorkRequests()
        self.folder = FolderProcess()

    def __image_to_base64(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_string = base64.b64encode(image_data).decode("utf-8")
                base64_with_header = f"data:image/jpeg;base64,{base64_string}"
                return base64_with_header
        except Exception as e:
            print(f"转换图像为 Base64 编码时出错：{e}")

    def __base64_to_image(self, base64_string, save_path):
        # 解码Base64字符串为字节数据
        image_data = base64.b64decode(base64_string)

        # 将字节数据转换为图像
        image = Image.open(BytesIO(image_data))

        # 保存图像到本地
        image.save(save_path)

    def upload(self, file, mode=None):
        """

        :param file:
        :param mode:
        :return:
        """
        if mode:
            module_name = "version 2 (🔺 robustness,🔻 stylization)"
        else:
            module_name = "version 1 (🔺 stylization, 🔻 robustness)"

        data = {
            "fn_index": 0,
            "data": [
                f"{self.__image_to_base64(file)}",
                module_name
            ],
            "action": "predict",
            "session_hash": "rabdv2l41a"
        }
        data = json.dumps(data, separators=(',', ':'))

        status, response = self.net._requests(self.url_upload, headers=self.headers, data=data, method="POST")
        return response.json()["hash"]

    def download_result(self, _hash):
        """

        :param _hash:
        :return:
        """
        data = {
            "hash": _hash
        }
        data = json.dumps(data, separators=(',', ':'))
        status, response = self.net._requests(self.url_download, headers=self.headers, data=data, method="POST")
        return response.json()["data"]["data"][0]

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_file = kwargs["in_file"]
        out_file = kwargs["save_file"]
        module_name = kwargs["save_file"]
        _hash = self.upload(in_file, module_name)
        result = None
        while not result:
            result = self.download_result(_hash)
        self.__base64_to_image(result[21:], out_file)


if __name__ == '__main__':
    cmh = CreateModuleHuman()
    in_file = R"D:\Desktop\图片2.JPG"
    out_file = R"D:\Desktop\1\result.png"
    cmh.process(in_file=in_file, save_file=out_file)
