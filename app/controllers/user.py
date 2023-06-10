from flask import Blueprint, request, jsonify

from app.status import StatusCode
from app.models.users import Users
from app.utils.passwordUtils import encrypt, checkPassword
from ..database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
            'code': StatusCode.USER_EXIST,
            'msg': '用户名已存在'
        }
        return res_data

    hashed_password = encrypt(password)
    new_user = Users(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '注册成功'
        }
        return jsonify(res_data)
    except Exception:
        res_data = {
            'code': StatusCode.REGISTER_FAIL,
            'msg': '注册失败'
        }
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
            'code': StatusCode.USER_NOT_EXIST,
            'msg': '用户不存在'
        }
        return jsonify(res_data)
    else:
        if checkPassword(password, user_exist.password):
            # 生成包含用户信息的 JWT 并添加到返回数据中
            access_token = create_access_token(identity=user_exist.id)
            res_data = {
                'code': StatusCode.OK,
                'data': {'access_token': access_token},
                'msg': '登录成功'
            }
            return jsonify(res_data)
        else:
            res_data = {
                'code': StatusCode.PASSWORD_ERROR,
                'msg': '密码错误'
            }
            return jsonify(res_data)


@user_bp.route('/hello', methods=['GET'])
@jwt_required(optional=False)
def handle_hello():
    userId = get_jwt_identity()
    res_data = {
        'code': StatusCode.OK,
        'msg': f'鸡你太美 {userId}'
    }
    return jsonify(res_data)
