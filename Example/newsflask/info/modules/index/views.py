# encoding: utf-8
from flask import render_template
from flask import current_app
from info import redis_store

__author__ = 'action'

from . import index_blu

@index_blu.route('/')
def index():
    # 设置redis_store name haha
    # redis_store.set("name", "haha")
    # return 'index'
    return render_template('news/index.html')

# 在打开网页的时候,浏览器会默认请求跟根路径favicon.ico 作为网站标签的小图标
# send_static_file是flask取查找指定静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')