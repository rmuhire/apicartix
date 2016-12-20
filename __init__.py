from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig

app = Flask(__name__, static_url_path='')
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
