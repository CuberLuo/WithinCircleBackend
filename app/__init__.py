import os.path

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from .controllers.post import post_bp
from .controllers.userinfo import userinfo_bp
from .database import db
from .controllers.user import user_bp
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from .status import StatusCode


def create_app():
    app = Flask(__name__)
    # 导入配置文件
    app.config.from_object(Config)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(userinfo_bp)
    app.register_blueprint(post_bp)
    # 数据库初始化
    db.init_app(app)
    # JWT 初始化
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    @jwt.invalid_token_loader
    def unauthorized_callback(callback):
        return jsonify({
            'code': StatusCode.UNAUTHORIZED,
            'msg': '无效token'
        })

    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'code': StatusCode.UNAUTHORIZED,
            'msg': 'token过期'
        })

    log_dir = './log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"目录'{log_dir}'不存在，已创建成功")

    # 配置日志
    handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app
