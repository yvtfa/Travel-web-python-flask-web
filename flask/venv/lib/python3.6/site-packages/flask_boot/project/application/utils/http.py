#!/usr/bin/env python2
# coding=utf8

from __future__ import absolute_import, division, print_function

import logging
from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow.fields import Field

from application.exception.util import raise_user_exc
from application.exception.error_code import INVALID_ARGS

logger = logging.getLogger(__name__)


class ArgsParser(FlaskParser):
    def all_args_spec(self, req=None, *args, **kwargs):
        req = req or request
        locations = kwargs.get('locations', []) or self.locations
        spec = {}
        for location in locations:
            if location == 'json':
                json_dict = req.get_json(silent=True)
                if json_dict:
                    [spec.__setitem__(k, Field()) for k in json_dict.keys()]
            elif location == 'querystring':
                [spec.__setitem__(k, Field()) for k in req.args.keys()]
            elif location == 'form':
                [spec.__setitem__(k, Field()) for k in req.form.keys()]
            elif location == 'headers':
                [spec.__setitem__(k, Field()) for k in req.headers.keys()]
            elif location == 'cookies':
                [spec.__setitem__(k, Field()) for k in req.cookies.keys()]
            elif location == 'files':
                [spec.__setitem__(k, Field()) for k in req.files.keys()]
            else:
                pass
        return spec

    def parse_all(self, req=None, *args, **kwargs):
        args_spec = self.all_args_spec(req, *args, **kwargs)
        return self.parse(args_spec, req, *args, **kwargs)


args_parser = ArgsParser()


@args_parser.error_handler
def handle_error(error):
    logger.error('invalid args!ERROR MESSAGE:{}'.format(error))
    raise_user_exc(INVALID_ARGS)


