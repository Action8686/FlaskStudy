# encoding: utf-8
import logging

from flask import current_app

__author__ = 'action'

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info import create_app, db

app = create_app('development')

manager = Manager(app)
# 将app与db关联
Migrate(app, db)
# 将迁移命令添加到manager中
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    logging.log(logging.DEBUG, "This is a debug log.")
    logging.log(logging.INFO, "This is a info log.")
    logging.log(logging.WARNING, "This is a warning log.")
    logging.log(logging.ERROR, "This is a error log.")
    logging.log(logging.CRITICAL, "This is a critical log.")
    # 在flask中不用logging需要用
    current_app.logger.error("错误日志")
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
