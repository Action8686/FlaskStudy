# encoding: utf-8
__author__ = 'action'


# 公用的自定义工具类
# 实现模板过滤器
# 自定义过滤器实现排行列表标签class
# 需要在 info __index__ 中添加
def do_index_class(index):
    """
    返回指定索引对应的类名
    :param index:
    :return:
    """
    if index == 0:
        return "first"
    elif index == 1:
        return "second"
    elif index == 2:
        return "third"
    return ""
