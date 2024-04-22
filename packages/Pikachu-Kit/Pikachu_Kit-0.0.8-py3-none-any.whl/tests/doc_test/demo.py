# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: demo.py
@time: 2024/3/6 16:10
@desc: docx提取图片

"""

# python-docx
from docx import Document
# pymupdf
import fitz
import re
from sdk.utils.util_class import PathParser
from sdk.temp.temp_supports import IsSolution, DM
from sdk.utils.util_encrypt import EncryptProcess

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
        self.encrypt = EncryptProcess()

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
        img_out_file_lis, file_split = args
        with open(self.folder.merge_path([self.save_path, f"{file_split.name}.{file_split.tail}.md"]), "w", encoding="utf-8") as f:
            for _file in img_out_file_lis:
                _file_split = PathParser(_file)
                img_folder = "/".join(self.folder.split_path(_file)[-2:])
                f.write(f"![{_file_split.name}](./{img_folder})\n")

    @DM.add_project()
    def parse_imgs_from_docx(self, file, file_split):
        """
        从doc文档中解析，保存图片，并返回图片本地保存路径
        :param file:
        :return:
        """
        print("提交", file)
        img_out_file_lis = []
        doc = Document(file)
        dict_rel = doc.part.rels
        for index, (r_id, rel) in enumerate(dict_rel.items()):
            if not (  # 如果文件不是在media或者embeddings中的，直接跳过
                    str(rel.target_ref).startswith('media')
                    or str(rel.target_ref).startswith('embeddings')
            ):
                continue

            # 如果文件不是我们想要的后缀，也直接跳过
            _file_split = PathParser(str(rel.target_ref))
            if _file_split.tail.lower() not in ['png', "jpeg", 'jpg', 'bin']:
                continue
            file_name = _file_split.name.lower() + "." + _file_split.tail
            _save_path = self.make_out_path(self.save_path, [f"{file_split.name}.{file_split.tail}"])
            img_save_file = self.folder.merge_path([_save_path, file_name])

            self.save_imgs(img_save_file, rel.target_part.blob)

            img_out_file_lis.append(img_save_file)

        self.muti_thread_function(img_out_file_lis, file_split)
        print("结束", file)

    @DM.add_project()
    def parse_imgs_from_pdf(self, file, file_split):
        """

        :param file:
        :param file_split:
        :return:
        """
        # print(" file, file_split", file, file_split)
        img_out_file_lis = []
        checkXO = r"/Type(?= */XObject)"
        checkIM = r"/Subtype(?= */Image)"
        # 打开pdf
        doc = fitz.open(file)
        # 图片计数
        imgcount = 0
        # 获取对象数量长度
        lenXREF = doc.xref_length()

        for i in range(1, lenXREF):
            # 定义对象字符串
            text = doc.xref_object(i)
            isXObject = re.search(checkXO, text)
            # 使用正则表达式查看是否是图片
            isImage = re.search(checkIM, text)
            # 如果不是对象也不是图片，则continue
            if not isXObject or not isImage:
                continue
            imgcount += 1
            # 根据索引生成图像
            pix = fitz.Pixmap(doc, i)
            # 根据pdf的路径生成图片的名称
            # new_name = f"{file_split.name}_{i}.png"
            new_name = f"{i}.png"
            # 如果pix.n<5,可以直接存为PNG
            _save_path = self.make_out_path(self.save_path, [f"{file_split.name}.{file_split.tail}"])
            _save_file = self.folder.merge_path([_save_path, new_name])
            if pix.n < 5:
                pix.writePNG(_save_file)
            # 否则先转换CMYK
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(_save_file)
                pix0 = None
            # 释放资源
            pix = None
            img_out_file_lis.append(_save_file)
        # self.muti_thread_function(img_out_file_lis, file_split)

    def save_imgs(self, file, date):
        """
        保存图片
        :param file:
        :param date:
        :return:
        """
        with open(file, "wb") as f:
            f.write(date)


    def resave_images(self, file, new_file):
        """

        :param file:
        :param new_file:
        :return:
        """
        self.file.move_file(file, new_file)

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        save_path_temp = R"D:\Desktop\temp"
        self.folder.create_folder(self.save_path)
        self.folder.create_folder(save_path_temp)

        self.name_set = set()
        map = {}
        for file, name in self.get_file(self.in_path, status=True):
            folder = self.folder.split_path(file)[-2]
            old_file = file
            name = self.encrypt.make_uuid(1)
            file_split = PathParser(file)
            _temp_path = self.make_out_path(save_path_temp, [folder])
            file = self.folder.merge_path([_temp_path,f"{name}.{file_split.tail}"])
            self.resave_images(old_file,file)
            map[old_file] = file

            print(file, name)  # 打印文件名和名称
            file_split = PathParser(file)
            if file_split.tail == "docx":
                self.parse_imgs_from_docx(file, file_split)
            elif file_split.tail == "pdf":
                self.parse_imgs_from_pdf(file, file_split)

        DM.close_pool()
        with open("map.json","w",encoding="utf-8")as fp:
            fp.write(self.json.dumps(map))


if __name__ == '__main__':
    in_path = R"D:\Desktop\1"
    save_path = R"D:\Desktop\33"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
