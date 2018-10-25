# encoding: utf-8
__author__ = 'action'

# 个人中信相关业务

from flask import Blueprint

profile_blu = Blueprint('profile', __name__, url_prefix="/user")

from . import views

