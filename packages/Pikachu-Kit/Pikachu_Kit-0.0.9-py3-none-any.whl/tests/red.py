# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: red.py
@time: 2024/2/5 16:18 
@desc: 

"""
from sdk.utils.util_cmd import RunCmd
from sdk.temp.temp_supports import IsSolution
from sdk.utils.util_class import PathParser



class Solution(IsSolution):
    """

    """

    def __init__(self):
        super(Solution, self).__init__()

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.name = kwargs["name"]

        self.folder.create_folder(self.save_path)
        num = 0
        for file, name in self.get_file(self.in_path, status=True):
            file_split = PathParser(file)
            num += 1
            new_file = self.folder.merge_path([save_path, f"{str(num).zfill(3)}.{file_split.tail}"])
            self.file.move_file(file, new_file)
            # self.success_lis.append([new_file])
        # merge_file = self.folder.merge_path([self.save_path, "merge.txt"])
        # self.save_result(merge_file, data=self.success_lis)

        cmd = f"ffmpeg -framerate 2 -i {save_path}/%3d.png -c:v libx264 -pix_fmt yuv420p {self.name}.mp4"
        for _ in RunCmd().run(cmd):
            print(_)



if __name__ == '__main__':
    name = 0
    in_path = fR"D:\BaiduNetdiskDownload\st_test\{name}"
    save_path = fR"D:\Desktop\2\0\{name}"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path,name=name)
