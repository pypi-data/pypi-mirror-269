# # !/usr/bin/python3
# # -*- coding:utf-8 -*-
# """
# @author: JHC000abc@gmail.com
# @file: dd3.py
# @time: 2024/2/2 17:47
# @desc:
#
# """
# import asyncio
#
# class Test(object):
#     def __init__(self,file,mode="w",encoding="utf-8"):
#         self.file = file
#         self.mode = mode
#         self.encoding = encoding
#
#
#     async def __aenter__(self):
#         self.file = open(self.file, mode=self.mode,encoding=self.encoding)
#         return self.file
#
#     async def __aexit__(self, *args):
#         self.file.close()
#
# async def write_date(file,data):
#     async with Test(file,"a")as f:
#         for i in data:
#             f.write(f"{i}\n")
#
#
# async def main():
#     file = R"1.txt"
#     data = [i for i in range(1000000)]
#     await write_date(file,data)
#     await write_date(file,data)
#
#
#
# def func():
#     return 111
#
# if __name__ == '__main__':
#     # asyncio.run(main())
#     dic = {
#         func():1,
#         7:3,
#         True:343,
#
#     }
#
#     print(dic)
#
#
# # 对象即容器，是数据和功能的集合体
#
# class Game(object):
#     isinstance = {}
#     count = 0
#     # __sex = None
#     def __new__(cls, *args, **kwargs):
#         """
#
#         :param args:
#         :param kwargs:
#         """
#         if cls not in cls.isinstance:
#             cls.isinstance[cls] = object.__new__(cls)
#         return cls.isinstance[cls]
#
#     def __init__(self, name, age):
#         super(Game, self).__init__()
#         self.name = name
#         self.age = age
#         Game.count += 1
#     def __str__(self):
#         return f"{self.name},{self.age}"
#     @property
#     def sex(self):
#         # if self.__dict__.get("_Game__set") is None:
#         #     self.__sex = False
#         return self.__sex
#     @sex.setter
#     def sex(self,sex):
#         if not isinstance(sex,bool):
#             print(f"sex must bool not {type(sex)}")
#             return
#         self.__sex = sex
#     @sex.deleter
#     def sex(self):
#         del self.__sex
#
#
#
# g = Game("zhansan",12)
# print(g.count)
# # g.__test = 111
# g2 = Game("zhansan",12)
# print(g.count)
# g3 = Game("zhansan",12)
# print(g.count)
# g.__dict__["test"] = 111
# print(g.__dict__)
#
# # print(g.sex)
# g.sex = True
# print(g.sex)
# del g.sex
# # print(g.sex)
#
#
# class PropertyTest(object):
#     """
#
#     """
#
#     def __init__(self,count):
#         """
#
#         """
#         self.__count = count
#     @property
#     def count(self):
#         return self.__count
#
#     @count.setter
#     def count(self,count):
#         if isinstance(count,int):
#             self.__count = count
#         else:
#             print(f"count must be int ,not {type(count)}")
#             return
#
#     @count.deleter
#     def count(self):
#         del self.__count
#
#
# pt = PropertyTest(19)
# print(pt.count)
# pt.count = 12
# print(pt.count)
# del pt.count
# # print(pt.count)
# print(PropertyTest.mro())
#
#
# # class TestMixIn():
#
#
# from abc import ABCMeta,abstractmethod
#
# class Parent(metaclass=ABCMeta):
#     @abstractmethod
#     def run(self):
#         print("parent run")
#
#
# class Child1(Parent):
#     """
#
#     """
#     def __init__(self):
#         super(Child1, self).__init__()
#
#     def run(self):
#         print("child1 run")
#
# # c1 = Child1()
# # c1.run()
#
# import datetime
# print(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))


"""
# r_9707

"""
import json
from sdk.utils.util_file import FileProcess
from sdk.utils.util_folder import FolderProcess


class Test(object):
    """

    """
    def __init__(self):
        self.file = FileProcess()
        self.folder = FolderProcess()
        self.map = {}
    def get_main_map(self):
        return {
    "角色侧信息": {
        "角色类别": {},
        "角色姓名": {},
        "搜索词条": {},
        "基本信息": {},
        "修改后信息": {},
        "语言学特征": {
            "经典台词语录（如有）": {},
            "地域特征（如有）": {},
            "文体特征（如有）": {},
            "常用表达（如有）": {},
            "其他（如有）": {}
        },
        "开场语": {},
        "角色搜索词条": {}
    },
    "角色侧补充信息": {
        "身份背景": {
            "团队": {},
            "身份": {},
            "以前的学校": {},
            "现在的学校": {},
            "曾住地": {},
            "现住地": {},
            "高中学校": {},
            "家庭情况": {},
            "性别": {},
            "小学学校": {},
            "现居住地": {},
            "家庭构成": {},
            "工作单位": {},
            "前工作单位": {},
            "学历背景": {},
            "家庭条件": {},
            "常住地": {},
            "职业": {},
            "工作地点": {},
            "真实身份": {},
            "年龄": {},
            "位分": {},
            "出身": {},
            "工作地": {},
            "职位": {},
            "现在地": {},
            "原住地": {},
            "出生方式": {},
            "曾经的职业": {},
            "毕业院校": {},
            "工作": {},
            "家庭成员": {},
            "家庭背景": {},
            "毕业学校": {},
            "前身份": {},
            "归属物": {},
            "所属物": {},
            "现工作职业": {},
            "现居地": {},
            "学历": {},
            "居住地": {},
            "出生地": {}
        },
        "别名称呼": {
            "称呼": {},
            "别名": {},
            "封号": {},
            "爸爸": {},
            "闺蜜": {},
            "朋友": {},
            "曾用名": {},
            "自称": {},
            "绰号": {},
            "外号": {},
            "本名": {}
        },
        "社会关系": {
            "队友": {},
            "朋友": {},
            "偶像": {},
            "妈妈": {},
            "闺蜜": {},
            "男友": {},
            "老师": {},
            "死对头": {},
            "同学": {},
            "宠物": {},
            "弟弟": {},
            "继母": {},
            "兄长": {},
            "女朋友": {},
            "女朋友的大哥": {},
            "女朋友的父亲": {},
            "丈夫": {},
            "敌人": {},
            "姐姐": {},
            "妻子": {},
            "表哥": {},
            "四妹": {},
            "三妹": {},
            "妹夫": {},
            "二弟": {},
            "父亲": {},
            "同僚": {},
            "阿婆": {},
            "同事": {},
            "哥哥": {},
            "男神": {},
            "爸爸": {},
            "表兄": {},
            "好友": {},
            "启蒙教练": {},
            "教练": {},
            "搭档": {},
            "谋士": {},
            "对手": {},
            "旧识": {},
            "军师": {},
            "兄弟": {},
            "夫人": {},
            "弟弟（无血缘）": {},
            "属下": {},
            "导师": {},
            "前辈": {},
            "母亲": {},
            "二姐（无血缘）": {},
            "二姐夫（无血缘）": {},
            "外甥（无血缘）": {},
            "男朋友": {},
            "假男友": {},
            "高中暗恋对象": {},
            "阿姨": {},
            "战友": {},
            "师父": {},
            "丫鬟": {},
            "妹妹": {},
            "岳父": {},
            "上级": {},
            "情敌": {},
            "儿子": {},
            "祖母": {},
            "邻居": {},
            "爱慕对象": {},
            "合作伙伴": {},
            "知己": {},
            "父王": {},
            "未婚夫": {},
            "姐夫": {},
            "倾慕者": {},
            "婆婆": {},
            "宿敌": {},
            "挚友": {},
            "仆人": {},
            "心腹": {},
            "老婆": {},
            "女儿": {},
            "仲父": {},
            "天祖父": {},
            "曾祖父": {},
            "高祖母": {},
            "臣子": {},
            "弟子": {},
            "同门": {},
            "师弟": {},
            "师祖": {},
            "师兄": {},
            "政敌": {},
            "下属": {},
            "小叔子": {},
            "姑姑": {},
            "哥哥（无血缘）": {},
            "爱人": {},
            "马夫": {},
            "生死兄弟": {},
            "前夫": {},
            "堂妹": {},
            "路人": {},
            "助理": {},
            "嘉宾": {},
            "同行": {},
            "同盟": {},
            "婢女": {},
            "青梅竹马": {},
            "外公": {},
            "父亲的结义弟兄": {},
            "警卫员": {},
            "恩人": {},
            "义子": {},
            "养子": {},
            "相亲对象": {},
            "公公": {},
            "主教练": {},
            "伯母": {},
            "伯伯": {},
            "大伯哥": {},
            "大嫂": {},
            "师姐": {},
            "大嫂子": {},
            "三嫂": {},
            "爱慕者": {},
            "追求者": {},
            "姘头": {},
            "侍女": {},
            "情人": {},
            "兄长（无血缘）": {},
            "学生": {},
            "二姐": {},
            "侄子": {},
            "暗恋对象": {},
            "生意伙伴": {},
            "前任": {},
            "普通朋友": {},
            "姐妹": {},
            "准妹夫": {},
            "继女": {},
            "小姑子": {},
            "老公": {},
            "前男友": {},
            "外甥": {},
            "前未婚夫": {},
            "五姐姐": {},
            "二姐姐": {},
            "亲生母亲": {},
            "三哥哥": {},
            "大哥哥": {},
            "世交": {},
            "四姐姐": {},
            "大姐姐": {},
            "嫡母": {},
            "祖父": {},
            "女神": {},
            "前队友": {},
            "下级": {},
            "养父": {},
            "二姨娘": {},
            "长辈": {},
            "未婚妻": {},
            "仇人": {},
            "上司": {},
            "大哥": {},
            "二哥": {},
            "伙伴": {},
            "养母": {},
            "同伴": {},
            "经纪人": {},
            "母亲的好友": {},
            "四哥": {},
            "会长": {},
            "房东": {},
            "侍从": {},
            "表弟": {},
            "远亲": {},
            "前女友": {},
            "竞争对手": {},
            "爱慕者兼合作伙伴": {},
            "收购公司的总经理": {},
            "前教练": {},
            "师傅": {},
            "妖仆": {},
            "部下": {},
            "叔叔": {},
            "利益伙伴": {},
            "徒弟": {},
            "受害者": {},
            "报案人": {},
            "舅舅": {},
            "冤家": {},
            "故友": {},
            "师侄": {},
            "师叔": {},
            "闺蜜的哥哥": {},
            "初恋": {}
        },
        "经历成就": {
            "经历": {},
            "成就": {},
            "主要经历": {},
            "主要成就": {},
            "经验": {}
        },
        "其他信息": {
            "性格": {},
            "观点": {},
            "爱好": {},
            "武器": {},
            "技能": {},
            "性格特点": {},
            "兴趣爱好": {},
            "特征": {},
            "未来规划": {},
            "特长": {},
            "作品": {},
            "特点": {},
            "感情状况": {},
            "个人特点": {},
            "日常生活": {},
            "武魂": {},
            "承诺": {},
            "决心": {},
            "弱点": {},
            "外貌": {},
            "理想": {},
            "个人特征": {},
            "缺点": {},
            "婚礼举办地": {},
            "偶像": {},
            "个人志向": {},
            "文化程度": {},
            "愿景": {},
            "身体状况": {},
            "文学主张": {},
            "功法": {},
            "长相": {},
            "钢琴级别": {},
            "拥有能力": {},
            "称号": {},
            "经历": {},
            "梦想": {},
            "生活习惯": {},
            "目前体重": {},
            "粉丝数量": {},
            "主持风格": {},
            "信念": {},
            "理论": {},
            "外貌特征": {}
        }
    },
    "用户侧信息": {
        "用户姓名": {},
        "用户搜索词条": {},
        "基本信息": {},
        "对话主题": {},
        "角色和用户间的社会关系": {},
        "角色对用户的态度": {},
        "用户对角色的态度": {}
    },
    "对话设定": {
        "对话主题": {},
        "角色和用户间的社会关系": {},
        "角色对用户的态度": {},
        "用户对角色的态度": {}
    },
    "对话": {}
}

    def recode_key(self,data):
        """

        :param data:
        :return:
        """
        try:
            for k, v in data["角色侧补充信息"]["身份背景"]["团队"].items():
                self.map.update({k: {}})
        except:
            pass

            # if isinstance(v,dict):

    def update_nested_dict(self,d, u):
        for k, v in u.items():
            # print(k,v)
            if v != "":
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    self.update_nested_dict(d[k], v)
                else:
                    d[k] = v

    def process(self):
        """

        :return:
        """

        for arg in self.folder.get_all_files(R"D:\Desktop\2"):
            file,name = arg["file"],arg["name"]
            main_map = self.get_main_map()
            if file.endswith(".json"):
                data = self.file.read_json_file(file)
                self.update_nested_dict(main_map,data)
                print(main_map)
                with open(fR"D:\Desktop\3\{name}","w",encoding="utf-8")as fp:
                    fp.write(json.dumps(main_map,indent=4,ensure_ascii=False))
                # break



if __name__ == '__main__':
    t = Test()
    t.process()