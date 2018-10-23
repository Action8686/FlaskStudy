# encoding: utf-8
from flask import render_template, session, request, jsonify
from flask import current_app
from info import redis_store
from info.models import User, News, Category
from info.utils.response_code import RET

__author__ = 'action'

from . import index_blu


@index_blu.route('/news_list')
def news_list():
    """
    获取首页新闻数据
    :return:
    """
    # 1.获取参数
    # 新闻的分类id
    cid = request.args.get('cid', '1')
    page = request.args.get('page', '1')
    per_page = request.args.get('per_page', '10')

    # 2. 校验参数
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    filters = []
    if cid != 1: # 查询的不是最新的数据, 1是最新数据
        # 需要添加条件
        filters.append(News.category_id==cid)
    # print('filters:%s'%filters)

    # 3. 查询数据
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    # 取到当前页的数据
    news_model_list = paginate.items # 模型对象列表
    total_page =  paginate.pages # 取到总的页数
    current_page = paginate.page # 当前页
    # 将模型对象列表转成字典列表
    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())

    # 查询分类数据,通过末班的形式渲染出来
    categories = Category.query.all()
    category_li = []
    for category in categories:
        category_li.append(category.to_dict())

    data = {
        "total_page":total_page,
        "current_page": current_page,
        "news_dict_li": news_dict_li,
        "category_li": category_li
    }
    return jsonify(errno=RET.OK, errmsg='OK', data=data)


@index_blu.route('/')
def index():
    # 设置redis_store name haha
    # redis_store.set("name", "haha")
    # return 'index'
    # return render_template('news/index.html')
    """
    显示首页
    1.如果用户已经登录,将当前登录用户的数据传到模板中,供模板显示
    :return:
    """
    # 显示用户是否登录的逻辑
    # 取到用户的id
    user_id = session.get('user_id')
    user = None  # 当查询不到用户的时候,user为None, 不返回数据
    if user_id:
        # 尝试查询用户的模型
        try:
            user = User().query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 右侧的新闻排行的逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(6)
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
    return render_template('news/index.html', data=data)


# 在打开网页的时候,浏览器会默认请求跟根路径favicon.ico 作为网站标签的小图标
# send_static_file是flask取查找指定静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
