import os

from flask import Flask, request, jsonify

from models import Users
from utils.passwordUtils import encrypt, checkPassword
from status import StatusCode
from database import db

app = Flask(__name__)

# 数据库密码
db_password = os.environ.get('DATABASE_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + db_password + '@1.15.134.164/within-circle'
db.init_app(app)


@app.route('/')
def hello_world():
    return 'hello'


@app.route('/register', methods=['POST'])
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


@app.route('/login', methods=['POST'])
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


if __name__ == '__main__':
    app.run(port=54321)
