#!/usr/bin/env python2
# coding=utf8

from __future__ import absolute_import, division, unicode_literals

HTTP_SYS_ERROR_CODE = 500
HTTP_AUTH_ERROR_CODE = 403
HTTP_BAD_REQUEST = 400


class BreezeExc(Exception):

    def __init__(self, error_code, type, http_code, msg):
        super(BreezeExc, self).__init__(msg)
        self.error_code = error_code
        self.type = type
        self.http_code = http_code
        self.msg = msg

    def __str__(self):
        return u'{}: [{}] {} http[{}]'.format(
            self.type, self.error_code, self.msg, self.http_code)


class UserExc(BreezeExc):

    def __init__(self, error_code, msg, http_code=HTTP_BAD_REQUEST):
        super(UserExc, self).__init__(
            type='user_exc', error_code=error_code, http_code=http_code, msg=msg)


class SysExc(BreezeExc):

    def __init__(self, error_code, msg, http_code=HTTP_SYS_ERROR_CODE):
        super(SysExc, self).__init__(
            type='sys_exc', error_code=error_code, http_code=http_code, msg=msg)


class DevExc(SysExc):

    def __init__(self, error_code, msg, http_code=HTTP_SYS_ERROR_CODE):
        super(SysExc, self).__init__(
            type='dev_exc', error_code=error_code, http_code=http_code, msg=msg)


