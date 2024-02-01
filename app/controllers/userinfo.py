import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.status import StatusCode
from config import WEB_BASE_URL
from ..database import db
from ..models.phones import Phones
from ..models.user_follows import UserFollows
from ..models.users import Users
from ..utils import file_utils
from ..utils.file_utils import dev_file_upload

userinfo_bp = Blueprint('userinfo', __name__)


@userinfo_bp.route('/user-info', methods=['GET'])
@jwt_required(optional=False)
def get_user_info():
    user_id = get_jwt_identity()
    user_exist = Users.query.filter_by(id=user_id).first()
    if user_exist:
        phone_exist = Phones.query.filter_by(user_id=user_id).first()
        hidden_phone_num = ''
        if phone_exist:
            phone_num = phone_exist.phone
            hidden_phone_num = phone_num[:3] + '****' + phone_num[7:]
        username = user_exist.username
        register_date = user_exist.register_date
        avatar_url = user_exist.avatar_url
        res_data = {
            'code': StatusCode.OK,
            'data': {
                'username': username,
                'register_date': register_date,
                'avatar_url': avatar_url,
                'phone_num': hidden_phone_num
            },
            'msg': '获取用户信息成功'
        }
        return jsonify(res_data)
    else:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '用户不存在'
        }
        return jsonify(res_data)


@userinfo_bp.route('/avatar', methods=['PUT'])
@jwt_required(optional=False)
def upload_user_avatar():
    user_id = get_jwt_identity()
    pic = request.files['pic']
    new_filename = file_utils.get_uuid_filename(pic.filename)
    if os.environ.get('FLASK_ENV') == 'development':
        dev_file_upload(pic, new_filename, request.headers.get('Authorization'))
    else:
        pic.save(fr'/www/wwwroot/within-circle/images/{new_filename}')  # r表示忽略所有的转义字符
    user_exist = Users.query.filter_by(id=user_id).first()
    user_exist.avatar_url = f'{WEB_BASE_URL}/images/{new_filename}'
    db.session.commit()
    res_data = {
        'code': StatusCode.OK,
        'msg': '修改成功'
    }
    return jsonify(res_data)


@userinfo_bp.route('/poster_user_info/<poster_id>', methods=['GET'])
@jwt_required(optional=False)
def get_poster_user_info(poster_id):
    user_id = get_jwt_identity()
    user_exist = Users.query.filter_by(id=poster_id).first()
    if user_exist:
        poster_username = user_exist.username  # 变量的作用域将延伸到包含该变量的函数
        avatar_url = user_exist.avatar_url
    else:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '用户不存在'
        }
        return jsonify(res_data)
    user_follows_exist = UserFollows.query.filter_by(base_user_id=user_id, follow_user_id=poster_id).first()
    if user_follows_exist:
        is_followed = True
    else:
        is_followed = False
    res_data = {
        'code': StatusCode.OK,
        'data': {
            'follow': is_followed,
            'avatar_url': avatar_url,
            'username': poster_username
        },
        'msg': '获取发布者信息成功'
    }
    return jsonify(res_data)
