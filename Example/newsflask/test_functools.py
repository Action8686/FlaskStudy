# encoding: utf-8
__author__ = 'action'
import functools

def user_login_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


@user_login_data
def num1():
    print('aaa')


@user_login_data
def num2():
    print('bbb')


if __name__ == '__main__':
    print(num1.__name__)  # 打印下函数的名字 为num1
    print(num2.__name__)  # 打印下函数的名字 为num2

# 当使用装饰器的时候打印的名字是相同的都是wrapper,这样在同一个模块中就会报错
# 为了处理名字相同的问题,导入functools, 就会避免这种错误
