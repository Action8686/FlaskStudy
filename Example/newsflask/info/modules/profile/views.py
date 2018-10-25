# encoding: utf-8
from flask import g, redirect

from info.utils.common import user_login_data

__author__ = 'action'
from info.modules.profile import profile_blu
from flask import render_template


@profile_blu.route('/info')
@user_login_data
def user_info():
    # 需要判断用户是否登录,没有登录无法访问个人中心
    user = g.user
    if not user:
        # 代表没有登录,重定向到首页
        return redirect("/")
    data = {
        "user":user.to_dict()
    }

    return render_template('news/user.html', data=data)