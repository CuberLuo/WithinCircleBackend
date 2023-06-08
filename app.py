import os

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# 数据库密码
db_password = os.environ.get('DATABASE_PASSWORD')
config = {
    'host': 'localhost',
    'user': 'root',
    'password': db_password,
    'database': 'within-circle'
}
cnx = mysql.connector.connect(**config)


@app.route('/')
def hello_world():
    return 'hello'


@app.route('/register', methods=['POST'])
def handle_register():
    json_data = request.get_json()
    print(json_data)
    username = json_data['username']
    password = json_data['password']

    res_data = {
        'code': 10000,
        'data': None,
        'msg': '注册成功'
    }
    return jsonify(res_data)


@app.route('/login', methods=['POST'])
def handle_login():
    json_data = request.get_json()
    print(json_data)
    username = json_data['username']
    password = json_data['password']

    res_data = {
        'code': 10000,
        'data': None,
        'msg': '登录成功'
    }
    return jsonify(res_data)


if __name__ == '__main__':
    app.run()
