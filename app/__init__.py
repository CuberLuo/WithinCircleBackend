from flask import Flask
from .database import db
from .controllers.user import user_bp
import logging
from logging.handlers import RotatingFileHandler
from config import Config


def create_app():
    app = Flask(__name__)
    # 导入配置文件
    app.config.from_object(Config)
    # 注册蓝图
    app.register_blueprint(user_bp)
    # 数据库初始化
    db.init_app(app)
    # 配置日志
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app
