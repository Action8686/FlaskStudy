# encoding: utf-8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from redis import StrictRedis

from config import config

__author__ = 'action'

# 初始化数据库,
# 在flask很多扩展里边都可以先初始化扩展对象,然后再去调用init_app方法初始化
db = SQLAlchemy()


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
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启当前项目的csrf保护,只做服务器验证功能
    CSRFProtect(app)
    # 设置session保存指定位置
    Session(app)

    return app