from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('f_app.config')

db = SQLAlchemy(app)
from .models import user

import f_app.views