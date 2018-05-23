# -*- coding: utf-8 -*-
"""Processing Controller view default route."""
from http import HTTPStatus

from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound


BP = Blueprint('home', __name__)


@BP.route('/', methods=['GET'])
def get():
    """Processing Controller Interface Home page"""
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(HTTPStatus.NOT_FOUND)
