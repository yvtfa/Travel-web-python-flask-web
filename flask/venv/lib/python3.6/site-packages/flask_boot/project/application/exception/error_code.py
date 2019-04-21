# coding=utf8

from __future__ import unicode_literals


DEV_METHOD_VALID = 40
DEV_CLASS_EXTENDS_ERR = 30
DEV_EXCEPTION_UNDEFINED_ERROR = 10
DATABASE_UNKNOWN_ERROR = 200
INVALID_ARGS = 1361


CODE_MSG = {
    DEV_CLASS_EXTENDS_ERR: '抽象类<{class_name}> 必须先继承才能使用。',
    DEV_METHOD_VALID: '函数写法不符合要求。{msg}',
    DEV_EXCEPTION_UNDEFINED_ERROR: '异常码未定义',
    DATABASE_UNKNOWN_ERROR: '数据库未知错误',
    INVALID_ARGS: '请求参数不合法',
}
