import time

from flask import request
from ..utils.str_utils import combine_strings
from flask_socketio import emit

private_chat_history = {}
user_map = {}  # 用于存放用户socket_id (key)和user_id (value)的映射关系
user_set = {}


def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        socket_id = request.sid
        print(f'新增连接 socket id: {socket_id}')

    @socketio.on('login')
    def handle_login(data):
        socket_id = request.sid
        print(f'login socket id: {socket_id}')
        print(data)
        user_id = data['userId']
        user_map[socket_id] = str(user_id)  # 记录socket id对应的user id，下次就可以直接通过socket id获取用户的user id
        print(f'user_map {user_map}')
        return {"code": 10000, "status": "登录成功"}

    @socketio.on('logout')
    def handle_logout():
        socket_id = request.sid
        print(f"用户下线 socket id: {socket_id} user id: {user_map[socket_id]}")
        if socket_id in user_map:
            del user_map[socket_id]  # 下线后移除socket id和对应的user id
        print(f'user_map {user_map}')

    @socketio.on("privateChatHistory")
    def handle_private_chat_history(data):
        socket_id = request.sid
        print(f'private_chat_history socket id: {socket_id}')
        user_id = user_map[socket_id]
        chat_user_id = str(data['chatUserId'])
        chat_key = combine_strings(user_id, chat_user_id)
        # 聊天双方没有历史聊天记录则初始化聊天双方key对应的聊天记录列表
        if chat_key not in private_chat_history:
            private_chat_history[chat_key] = []
        emit("privateChatHistory", {
            "chatUserId": chat_user_id,
            "msgHistory": private_chat_history[chat_key]
        }, room=socket_id)

    @socketio.on("privateChat")
    def handle_private_chat(data):
        socket_id = request.sid
        print(f'private_chat socket id: {socket_id}')
        # 用于处理WebView发送图片断线重连的特殊情况
        if 'isImg' in data and data['isImg']:
            time.sleep(1)
        user_id = user_map[socket_id]
        chat_user_id = str(data['chatUserId'])
        chat_key = combine_strings(user_id, chat_user_id)
        print(f"发送消息 User ID: {user_id}, Chat User ID: {chat_user_id}")
        print(f"消息详情: {data}")
        private_chat_history[chat_key].append(data)
        chat_user_socket_id = get_socket_id_by_user_id(chat_user_id)  # 私聊的对方的socket id
        if chat_user_socket_id:
            emit("privateChat", data, room=chat_user_socket_id)
            return {"code": 10000, "status": "发送成功"}
        else:
            return {"code": 10001, "status": "该用户已下线"}

    @socketio.on('disconnect')
    def handle_disconnect():
        socket_id = request.sid
        if socket_id in user_map:
            del user_map[socket_id]  # Socket断连后移除socket id和对应的user id
        print(f"Socket断连 socket id: {socket_id}")


def get_socket_id_by_user_id(user_id):
    # 一个用户在多个平台上登录时会存在一个user_id对应多个socket_id的情况
    # 为简化处理此处仅获取第一个user_id对应的socket_id
    for key, value in user_map.items():
        if value == user_id:
            return key
    return None
