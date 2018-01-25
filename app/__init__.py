from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

"""
Logger Settings
"""
file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
	
from app import routes, models