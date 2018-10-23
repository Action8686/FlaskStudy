# encoding: utf-8
import functools

from flask import g, current_app, session

from info.models import User

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


"""
# 主要是在detail中用到了这个方法,在index中也用到了这个方法
    # 取到用户的id
    user_id = session.get('user_id')
    user = None  # 当查询不到用户的时候,user为None, 不返回数据
    if user_id:
        # 尝试查询用户的模型
        try:
            user = User().query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

"""

def user_login_data(f):
    @functools.wraps(f)# 使用functools.wraps 去装饰内层函数,可以保持当前装饰器去装饰的函数的__name__的值不变, 可以看text.py详解
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id", None)
        user = None
        if user_id:
            # 尝试查询用户的模型
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        # 把查询出来的数据赋值给g变量
        g.user = user
        return f(*args, **kwargs)
    return wrapper