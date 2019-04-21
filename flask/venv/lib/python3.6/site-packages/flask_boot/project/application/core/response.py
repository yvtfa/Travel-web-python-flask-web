# coding=utf8

from werkzeug.wrappers import Response
from flask import jsonify


class JSONResponse(Response):
    _header_dict = {'Content-Type': 'application/json'}

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)
