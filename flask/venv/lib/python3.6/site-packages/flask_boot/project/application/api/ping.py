# coding=utf8

from __future__ import absolute_import, division, print_function

from flask import Blueprint

ping_bp = Blueprint('ping', __name__)


@ping_bp.route('/ping', methods=['GET', 'POST'])
def ping():
    return 'pong'
