# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: get_result.py
@time: 2024/4/1 18:22 
@desc: 

"""
from sdk.temp.temp_supports import IsSolution, DM
from doc_test.demo.python_demo.vil import *



class Solution(IsSolution):
    """
    Solution
    """

    def __init__(self, **kwargs):
        """
        初始化函数
        :param kwargs: 字典类型的参数字典，包含可选的关键字参数
        """
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})


    def exit_handler(self):
        """
        程序退出自动执行
        :return:
        """
        print("程序退出")

    @DM.add_project()
    def muti_thread_function(self, *args):
        """
        处理数据函数
        :param args:
        :return:
        """
        file, name = args
        data = feature_calculate(file)
        te_path = self.folder.merge_path([self.save_path, "result_{}.json".format(name)])
        with open(te_path, "w",encoding="utf-8") as f:
            f.write(self.json.dumps(data))

        return None

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.folder.create_folder(self.save_path)
        for file, name in self.get_file(self.in_path, status=True):
            self.muti_thread_function(file, name)
        DM.close_pool()


if __name__ == '__main__':
    in_path = R"D:\Desktop\33"
    save_path = R"D:\Desktop\44"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
