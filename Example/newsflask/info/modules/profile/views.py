# encoding: utf-8
from flask import g, redirect, request

from info import constants
from info.utils.common import user_login_data
from info.utils.image_storage import storage
from info.utils.response_code import RET

__author__ = 'action'
from info.modules.profile import profile_blu
from flask import render_template
from flask import jsonify
from flask import current_app

@profile_blu.route('/pic_info', methods=['GET', 'POST'])
@user_login_data
def pic_info():
    user = g.user
    if request.method == "GET":
        return render_template('news/user_pic_info.html', data={"user": user.to_dict()})
    # TODO 如果是POST表示修改头像
    # 1. 取到上传的图片
    try:
        avatar = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 2.上传头像
    try:
        # 使用自己封装的storage方法进行土坯那上传
        key = storage(avatar)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传头像失败")
    # 3. 保存头像的地址
    # 不需要进行提交 因为SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    user.avatar_url = key
    return jsonify(errno=RET.OK, errmsg="OK", data={"avatar_url":constants.QINIU_DOMIN_PREFIX+key})


@profile_blu.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_info():
    # 不同的请求方式，做不同的事情
    if request.method == 'GET':
        data = {
            "user": g.user.to_dict()
        }
        return render_template('news/user_base_info.html', data=data)
    # 代表是修改用户的数据
    # 1. 取到传入的数据
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 2. 校验参数
    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if gender not in ("WOMAN", "MAN"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    user = g.user
    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender
    return jsonify(errno=RET.OK, errmsg="OK")


@profile_blu.route('/info')
@user_login_data
def user_info():
    # 需要判断用户是否登录,没有登录无法访问个人中心
    user = g.user
    if not user:
        # 代表没有登录,重定向到首页
        return redirect("/")
    data = {
        "user": user.to_dict()
    }

    return render_template('news/user.html', data=data)
