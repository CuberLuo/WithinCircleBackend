from flask import Blueprint, request, jsonify

from app.status import StatusCode
from app.models.users import Users
from app.utils.passwordUtils import encrypt, checkPassword
from ..database import db
user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def handle_register():
    json_data = request.get_json()
    print(json_data)
    username = json_data['username']
    password = json_data['password']

    user_exist = Users.query.filter_by(username=username).first()
    if user_exist:
        res_data = {
            'code': StatusCode.ERROR,
            'data': None,
            'msg': '用户名已存在'
        }
        return res_data

    hashed_password = encrypt(password)
    new_user = Users(username=username, password=hashed_password)
    res_data = {}
    try:
        db.session.add(new_user)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'data': None,
            'msg': '注册成功'
        }
    except Exception:
        res_data = {
            'code': StatusCode.ERROR,
            'data': None,
            'msg': '注册失败'
        }
    finally:
        return jsonify(res_data)


@user_bp.route('/login', methods=['POST'])
def handle_login():
    json_data = request.get_json()
    print(json_data)
    username = json_data['username']
    password = json_data['password']

    user_exist = Users.query.filter_by(username=username).first()
    if not user_exist:
        res_data = {
            'code': StatusCode.ERROR,
            'data': None,
            'msg': '用户不存在'
        }
        return jsonify(res_data)
    else:
        if checkPassword(password, user_exist.password):
            res_data = {
                'code': StatusCode.OK,
                'data': None,
                'msg': '登录成功'
            }
            return jsonify(res_data)
        else:
            res_data = {
                'code': StatusCode.ERROR,
                'data': None,
                'msg': '密码错误'
            }
            return jsonify(res_data)
