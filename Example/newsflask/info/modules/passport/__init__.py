# encoding: utf-8
__author__ = 'action'

# 登录注册的相关业务逻辑都放在当前的模块中
from flask import Blueprint

passpot_blu = Blueprint('passport', __name__, url_prefix="/passport")

from . import views