# -*- coding: utf-8 -*-
"""Scheduling Block Instance List Web UI."""
from http import HTTPStatus

import requests
from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound


BP = Blueprint('scheduling-blocks', __name__)


def _get_scheduling_block_instance_list():
    """Return list of scheduling block instances"""
    req = requests.get('http://localhost:5000/api/v1/scheduling-blocks')
    return req.json()['scheduling_blocks']


@BP.route('/scheduling-blocks', methods=['GET'])
def _get():
    """View list of Scheduling Block Instances."""
    blocks = _get_scheduling_block_instance_list()
    try:
        return render_template('scheduling_block_list.html', blocks=blocks)
    except TemplateNotFound:
        abort(HTTPStatus.NOT_FOUND)


@BP.route('/scheduling-blocks/new', methods=['GET'])
def _new():
    """View list of Scheduling Block Instances."""
    blocks = _get_scheduling_block_instance_list()
    num_blocks = len(blocks)
    try:
        return render_template('scheduling_block_new.html', blocks=blocks,
                               num_blocks=num_blocks)
    except TemplateNotFound:
        abort(HTTPStatus.NOT_FOUND)


@BP.route('/test', methods=['GET'])
def _test():
    """Test."""
    try:
        return render_template('test.html')
    except TemplateNotFound:
        abort(HTTPStatus.NOT_FOUND)


# @BP.route('/scheduling-blocks', methods=['POST'])
# def _post():
#     global NEW_SCHEDULING_BLOCK
#     # print('-------')
#     # print('REQUEST=')
#     # print('args:', request.args)
#     # print('form:', request.form)
#     # print('data:', request.data)
#     # print('vals:', request.values)
#     # print('files:', request.files)
#     # print('-------')
#     print(request.form)
#     NEW_SCHEDULING_BLOCK = True
#     return 'hello', HTTPStatus.OK
    # text = ''
    # blocks = _get_scheduling_block_instance_list()
    # try:
    #     return render_template('scheduling_block_accepted.html',
    #                            blocks=blocks, text=text,
    #                            form_data=request.form)
    # except TemplateNotFound:
    #     abort(HTTPStatus.NOT_FOUND)
