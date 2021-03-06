# encoding: utf-8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf
from redis import StrictRedis

from config import config

__author__ = 'action'

# 初始化数据库,

db = SQLAlchemy()

# 在py3.6以上的版本中支持这种写法
# 这样在views中导入redis_sore就可以有智能提示了
redis_store = None  # type:StrictRedis
# redis_store:StrictRedis = None

def setup_log(config_name):
    # 设置日志的记录等级
    # config[config_name].LOG_LEVEL获取到config中配置字典中的是开发模式,还是生产模式,中的LOG_LEVEL等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 配置日志,当创建app的时候就获取到日志的配置信息
    # 传入配置名字,以便能获取到指定配置的对应的日志等级信息
    setup_log(config_name)
    # 创建Flask对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 通过app初始化, 可以查看SQLAlchemy源码
    db.init_app(app)
    # 初始化 redis存储对象
    # 设置redis_store为全局变量,局部变量不能被别的模块引用,变为全局变量可以为别的模块引用
    global redis_store  # 需要设置decode_responses=True 不然在输入验证码的时候,输入的是str 获取出来是byte
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT, decode_responses=True)
    # 开启当前项目的csrf保护,只做服务器验证功能
    # 帮我们做了:从cookie中取出随机值,从表单中随机取出,然后进行校验,并且响应校验结果
    # 我们需要做:
    # 1.在返回响应的时候,往cookie中添加一个csrf_cookie
    # 2. 并且在表单中添加一个隐藏的csrf_token这个随机值就可以了
    # 而我们现在登录或者注册不是使用的表单,而是使用的ajax请求,所以我们需要在ajax 请求的时候带上 csrf_token 这个随机值就可以了
    CSRFProtect(app)
    # 设置session保存指定位置
    Session(app)

    # 在flask很多扩展里边都可以先初始化扩展对象,然后再去调用init_app方法初始化
    # 在创建app时候调用,不然会报错,不能导入db错误
    from info.utils.common import do_index_class

    # 添加自定义过滤器
    app.add_template_filter(do_index_class, "index_class")

    # 请求钩子函数
    @app.after_request
    def after_request(response):
        # 调用函数生成 csrf_token
        csrf_token = generate_csrf()
        # 通过 cookie 将值传给前端
        response.set_cookie("csrf_token", csrf_token)
        return response

    # 注册蓝图
    # 在这里导入模块,这样会避免出现导入不成功的现象
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passpot_blu
    app.register_blueprint(passpot_blu)

    from info.modules.news import news_blu
    app.register_blueprint(news_blu)

    from info.modules.profile import profile_blu
    app.register_blueprint(profile_blu)

    return app
