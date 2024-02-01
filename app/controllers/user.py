import os
from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from sqlalchemy import desc

from app.models.users import Users
from app.status import StatusCode
from app.utils.password_utils import encrypt, check_password
from app.utils.sms_utils import send_sms_code, generate_code
from ..database import db
from ..models.phones import Phones
from ..models.user_follows import UserFollows
from ..utils import time_utils

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    username = request.get_json()['username']
    password = request.get_json()['password']
    # TODO:用户名和密码长度需要进行验证
    user_exist = Users.query.filter_by(username=username).first()
    if user_exist:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '用户名已存在'
        }
        return res_data

    hashed_password = encrypt(password)
    new_user = Users(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)
        res_data = {
            'code': StatusCode.OK,
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'msg': '注册成功'
        }
        return jsonify(res_data)
    except Exception as e:
        print(e)
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '注册失败'
        }
        return jsonify(res_data)


@user_bp.route('/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']

    user_exist = Users.query.filter_by(username=username).first()
    if not user_exist:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '用户不存在'
        }
        return jsonify(res_data)
    else:
        if check_password(password, user_exist.password):
            # 生成包含用户信息的 JWT 并添加到返回数据中
            access_token = create_access_token(identity=user_exist.id)
            refresh_token = create_refresh_token(identity=user_exist.id)
            res_data = {
                'code': StatusCode.OK,
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                'msg': '登录成功'
            }
            return jsonify(res_data)
        else:
            res_data = {
                'code': StatusCode.ERROR,
                'msg': '密码错误'
            }
            return jsonify(res_data)


@user_bp.route('/token-refresh', methods=['GET'])
@jwt_required(refresh=True)
def token_refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    res_data = {
        'code': StatusCode.OK,
        'data': {
            'access_token': access_token,
            'refresh_token': refresh_token,
        },
        'msg': '刷新成功'
    }
    return jsonify(res_data)


@user_bp.route('/hello', methods=['GET'])
@jwt_required(optional=False)  # optional=False 意味着 JWT 是必需的
def hello():
    user_id = get_jwt_identity()
    res_data = {
        'code': StatusCode.OK,
        'msg': f'你好! {user_id}'
    }
    return jsonify(res_data)


@user_bp.route('/msg', methods=['GET'])
def msg():
    print('/msg')
    res_data = {
        'code': StatusCode.OK,
        'msg': f"{os.environ.get('FLASK_ENV')}"
    }
    return jsonify(res_data)


@user_bp.route('/sms', methods=['GET'])
def sms():
    phone_num = request.args.get('phone')
    sms_flag = request.args.get('sms_flag')
    phone_exist = Phones.query.filter_by(phone=phone_num).first()
    if not phone_exist:
        if sms_flag == 'login':
            res_data = {
                'code': StatusCode.ERROR,
                'msg': f'该手机号尚未注册'
            }
            return jsonify(res_data)
    else:
        if sms_flag != 'login' and phone_exist.user_id != '':
            res_data = {
                'code': StatusCode.ERROR,
                'msg': f'该手机号已被其他账号绑定'
            }
            return jsonify(res_data)
    sms_code = generate_code()

    res_code = send_sms_code(phone_num, sms_code)
    if res_code == "OK":
        if not phone_exist and sms_flag != 'login':
            new_phone = Phones(phone=phone_num)
            db.session.add(new_phone)
            db.session.commit()
            phone_exist = new_phone
        phone_exist.code = sms_code  # 更新数据库中的code
        active_minutes = 5  # 验证码有效时长
        phone_exist.expire_time = time_utils.get_current_date_time() + timedelta(minutes=active_minutes)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': f'短信验证码发送成功'
        }
        return jsonify(res_data)
    else:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': f'短信验证码发送失败'
        }
        return jsonify(res_data)


@user_bp.route('/sms-check', methods=['GET'])
@jwt_required(optional=True)
def sms_check():
    phone_num = request.args.get('phone')
    sms_code = request.args.get('sms')
    sms_flag = request.args.get('sms_flag')
    phone_exist = Phones.query.filter_by(phone=phone_num).first()
    if not phone_exist:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': f'验证码信息不存在'
        }
        return jsonify(res_data)
    elif phone_exist.user_id == '':
        if sms_flag == 'login':
            res_data = {
                'code': StatusCode.ERROR,
                'msg': f'该手机号尚未注册'
            }
            return jsonify(res_data)

    if time_utils.get_current_date_time() > phone_exist.expire_time:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '验证码已失效'
        }
        return jsonify(res_data)

    if phone_exist.code == sms_code:
        if sms_flag == 'login':
            access_token = create_access_token(identity=phone_exist.user_id)
            refresh_token = create_refresh_token(identity=phone_exist.user_id)
            res_data = {
                'code': StatusCode.OK,
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                'msg': '登录成功'
            }
            return jsonify(res_data)
        else:
            user_id = get_jwt_identity()
            phone_exist.user_id = user_id
            db.session.commit()
            res_data = {
                'code': StatusCode.OK,
                'data': {
                    'phone_num': phone_num[:3] + '****' + phone_num[7:]
                },
                'msg': '绑定成功'
            }
            return jsonify(res_data)
    else:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '验证码错误'
        }
        return jsonify(res_data)


@user_bp.route('/pwd', methods=['PUT'])
@jwt_required(optional=False)
def pwd_change():
    original_pwd = request.get_json()['original_pwd']
    new_pwd = request.get_json()['new_pwd']
    user_id = get_jwt_identity()
    user_exist = Users.query.filter_by(id=user_id).first()
    if check_password(original_pwd, user_exist.password):
        user_exist.password = encrypt(new_pwd)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '密码修改成功'
        }
        return jsonify(res_data)
    else:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '原密码错误'
        }
        return jsonify(res_data)


@user_bp.route('/follow-user', methods=['POST'])
@jwt_required(optional=False)
def follow_user():
    user_id = get_jwt_identity()  # int类型的user_id
    other_user_id = int(request.get_json()['user_id'])  # str类型的user_id转为int类型

    if user_id == other_user_id:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '不能关注自己哦'
        }
        return jsonify(res_data)
    user_follows_exist = UserFollows.query.filter_by(base_user_id=user_id, follow_user_id=other_user_id).first()
    if user_follows_exist:
        db.session.delete(user_follows_exist)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '取消关注成功'
        }
        return jsonify(res_data)
    else:
        new_user_follows = UserFollows(base_user_id=user_id, follow_user_id=other_user_id)
        db.session.add(new_user_follows)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '关注成功'
        }
        return jsonify(res_data)


@user_bp.route('/my-follows', methods=['GET'])
@jwt_required(optional=False)
def get_my_follows():
    user_id = get_jwt_identity()
    all_user_follows = UserFollows.query.filter_by(base_user_id=user_id).order_by(desc(UserFollows.follow_date)).all()
    follower_list = []
    for user_follows in all_user_follows:
        follow_user_id = user_follows.follow_user_id
        user_exist = Users.query.filter_by(id=follow_user_id).first()
        user_dict = {
            'id': user_exist.id,
            'username': user_exist.username,
            'avatar_url': user_exist.avatar_url,
            'follow': True
        }
        follower_list.append(user_dict)
    res_data = {
        'code': StatusCode.OK,
        'data': follower_list,
        'msg': '成功'
    }
    return jsonify(res_data)


@user_bp.route('/my-fans', methods=['GET'])
@jwt_required(optional=False)
def get_my_fans():
    user_id = get_jwt_identity()
    all_user_follows = UserFollows.query.filter_by(follow_user_id=user_id).order_by(desc(UserFollows.follow_date)).all()
    fans_list = []
    for user_follows in all_user_follows:
        fans_id = user_follows.base_user_id
        user_exist = Users.query.filter_by(id=fans_id).first()
        user_follows_exist = UserFollows.query.filter_by(base_user_id=user_id, follow_user_id=fans_id).first()
        user_dict = {
            'id': user_exist.id,
            'username': user_exist.username,
            'avatar_url': user_exist.avatar_url,
            'follow': True if user_follows_exist else False
        }
        fans_list.append(user_dict)
    res_data = {
        'code': StatusCode.OK,
        'data': fans_list,
        'msg': '成功'
    }
    return jsonify(res_data)
