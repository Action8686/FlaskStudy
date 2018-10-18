# encoding: utf-8
__author__ = 'action'

from flask import Blueprint

index_blu = Blueprint("index", __name__)

from . import views
