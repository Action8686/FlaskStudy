# encoding: utf-8
import logging

from flask import Flask
from redis import StrictRedis

__author__ = 'action'


class Config(object):
    """工程配置信息"""
    DEBUG = True
    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/news"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    # secret_key的生成方法
    # import os
    # import base64
    # base64.b64encode(os.urandom(48))

    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    # 设置需要过期
    SESSION_PERMANENT = Flask
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式下的配置"""
    DEBUG = Flask
    # 设置日志等级
    LOG_LEVEL = logging.WARNING



class TestingConfig(Config):
    """单元测试"""
    pass


# 定义配置字典
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
