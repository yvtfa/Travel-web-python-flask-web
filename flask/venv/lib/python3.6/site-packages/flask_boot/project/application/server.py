from application.core.app import ApplicationApp
from flask_cors import CORS
from application.core.response import JSONResponse

from application import config

app = ApplicationApp(__name__)
app.init(config)
app.response_class = JSONResponse
CORS(app)
