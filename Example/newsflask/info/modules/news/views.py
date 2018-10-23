# encoding: utf-8
from info import constants
from info.models import User, News
from info.modules.news import news_blu
from info.utils.common import user_login_data

__author__ = 'action'
from flask import render_template, session, current_app, g


@news_blu.route('/<int:news_id>')
@user_login_data
def news_detail(news_id):
    """
    新闻详情
    :return:
    """
    # 显示用户是否登录的逻辑
    # 取到用户的id
    # user_id = session.get('user_id')
    # user = None  # 当查询不到用户的时候,user为None, 不返回数据
    # if user_id:
    #     # 尝试查询用户的模型
    #     try:
    #         user = User().query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)
    user = g.user
    # 右侧的新闻排行的逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    # 定义一个空的字典列表,里面装的就是字典
    news_dict_li = []
    # 遍历对象列表,将对象的字典添加到字典的列表中
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li
    }
    return render_template('news/detail.html', data=data)


