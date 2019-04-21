# coding=utf8

from application.api.ping import ping_bp
from application.exception.util import raise_user_exc
from application.exception.error_code import INVALID_ARGS

__all__ = [
    ping_bp,
]


def api_init(app):
    for blue_print in __all__:
        app.register_blueprint(blue_print)

    @app.errorhandler(TypeError)
    def invalid_params(error):
        raise_user_exc(INVALID_ARGS)
