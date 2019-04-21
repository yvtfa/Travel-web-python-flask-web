import sys

from flask import Flask
from application.api import api_init
from application.core.signal import signal

reload(sys)
sys.setdefaultencoding('utf-8')


class ApplicationApp(Flask):

    def init(self, settings):
        self.config.update(**settings.FLASK)
        api_init(self)
        signal(self)
