from flask import Flask
from flask_login import LoginManager
from .routes import routing
from .models import login_manager_func
import os
import secrets
from app.config import connect_redis
import threading
from app.send_to_redis import sent_to_redis
from .models import PsqlQuery, User, ServiceQuerys
from app.utils.general import parse_stocks

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    redis_cli = connect_redis()
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    app.config["FILE_PATH"] = f"{os.getcwd()}/app/templates/uploads"
    print(app.config["FILE_PATH"])

    login_manager_thread = threading.Thread(target=login_manager_func, args=(login_manager,))
    login_manager_thread.start()

    redis_thread = threading.Thread(target=sent_to_redis, args=(redis_cli, ServiceQuerys, parse_stocks))
    redis_thread.start()

    routing(app, redis_cli, PsqlQuery, User, ServiceQuerys, parse_stocks)
    return app