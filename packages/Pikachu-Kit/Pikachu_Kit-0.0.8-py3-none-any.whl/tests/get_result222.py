# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: get_result.py
@time: 2024/4/1 18:22 
@desc: 

"""
import io
from tests.doc_test.demo.python_demo.vil import *
import json
import os
import shutil
import traceback
import base64


class FileProcess():
    """
    文件处理类
    """

    def __init__(self):
        pass

    def get_file_lines(self, file, status=1):
        """
        获取文件总行数
        :param file:
        :param status:0:大文件、1小文件
        :return:
        """
        if status == 1:
            return sum(1 for _ in open(file, 'rb'))
        else:
            with open(file, 'rb') as f:
                for count, _ in enumerate(f, 1):
                    pass
            return count

    def rename_file(self, old, new):
        """
        重命名文件
        :param old:
        :param new:
        :return:
        """
        try:
            if os.path.isfile(old) and not os.path.exists(new):
                os.renames(old, new)
        except BaseException:
            print(traceback.format_exc())

    def move_file(self, old_file, new_file, mode=True):
        """

        :param old_file:
        :param new_file:
        :param mode: 默认不删除原文件
        :return:
        """
        shutil.copy(old_file, new_file)
        if not mode:
            os.remove(old_file)


class FolderProcess():
    """

    """

    def __init__(self):
        pass

    def create_folder(self, path):
        """
        创建文件夹
        :param _path:
        :return:
        """
        os.makedirs(path, exist_ok=True)

    def merge_path(self, path_lis):
        """
        合并路径
        :param path_lis:
        :return:
        """
        if path_lis:
            return os.path.sep.join(path_lis)

    def split_path(self, path, spliter=None):
        """
        拆分路径
        """
        if not spliter:
            if not path.startswith("http://") or not path.startswith("https://"):
                return os.path.normpath(path).split(os.sep)
            else:
                return os.path.normpath(path).split("/")
        else:
            return path.split(spliter)

    def get_all_files(self, path, ext=None):
        """
        获取文件夹下所有文件绝对路径
        :param path:
        :param ext: 后缀列表[".txt",".json",...]
        :return:
        """
        try:
            if os.path.exists(path) and os.path.isabs(path):
                for path, dir_lis, file_lis in os.walk(path):
                    if len(file_lis) > 0:
                        for name in file_lis:
                            if ext:
                                if os.path.splitext(name)[-1] in ext:
                                    yield {
                                        "name": name,
                                        "file": os.path.join(path, name),
                                    }
                            else:
                                yield {
                                    "name": name,
                                    "file": os.path.join(path, name),
                                }
        except BaseException:
            print(traceback.format_exc())


class Solution():
    """
    Solution
    """

    def __init__(self, **kwargs):
        """
        初始化函数
        :param kwargs: 字典类型的参数字典，包含可选的关键字参数
        """

        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})
        self.folder = FolderProcess()
        self.file = FileProcess()

    def exit_handler(self):
        """
        程序退出自动执行
        :return:
        """
        print("程序退出")

    def muti_thread_function(self, *args):
        """
        处理数据函数
        :param args:
        :return:
        """
        file, name = args
        print("file", file)
        folder = self.folder.split_path(file)[-2]
        data = feature_calculate(file)
        new_path = os.path.join(self.save_path, folder)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        te_path = self.folder.merge_path([new_path, "result_{}.json".format(name)])

        try:
            result = json.loads(json.loads(data)["feature_result"]["value"])["result"]
            res = base64.b64decode(result)
            with io.open(te_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(json.loads(res), indent=4, ensure_ascii=False))
        except:
            print("te_path",te_path)

        return None

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        for arg in self.folder.get_all_files(self.in_path):
            file, name = arg["file"], arg["name"]
            self.muti_thread_function(file, name)


if __name__ == '__main__':
    in_path = R"D:\Desktop\33"
    save_path = R"D:\Desktop\44"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
