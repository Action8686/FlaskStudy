# encoding: utf-8
from info.modules.news import news_blu

__author__ = 'action'
from flask import render_template


@news_blu.route('/<int:news_id>')
def news_detail(news_id):
    """
    新闻详情
    :return:
    """
    return render_template('news/detail.html')


