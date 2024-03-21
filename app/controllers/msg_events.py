from flask import request
from ..utils.str_utils import combine_strings
from flask_socketio import emit

private_chat_history = {}
user_map = {}  # 用于存放用户id和socket id的映射关系
user_set = {}


def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        socket_id = request.sid
        username = request.args.get('username')
        user_id = request.args.get('userId')
        print(f'新增连接 socket id: {socket_id} username: {username} user_id: {user_id}')

    @socketio.on("privateChatHistory")
    def handle_private_chat_history(data):
        socket_id = request.sid
        print(f'private_chat_history socket id: {socket_id}')
        username = request.args.get('username')
        user_id = request.args.get('userId')
        print(f'用户{username}获取聊天记录')
        chat_user_id = data['chatUserId']
        chat_key = combine_strings(user_id, chat_user_id)

        user_map[user_id] = socket_id
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
        username = request.args.get('username')
        user_id = request.args.get('userId')
        chat_user_id = data['chatUserId']
        chat_key = combine_strings(user_id, chat_user_id)
        print(f"{username}发送消息 User ID: {user_id}, Chat User ID: {chat_user_id}")
        print(f"data: {data}")
        private_chat_history[chat_key].append(data)
        if chat_user_id in user_map:
            chat_user_socket_id = user_map[chat_user_id]  # 私聊的对方的socket id
            emit("privateChat", data, room=chat_user_socket_id)
            return {"code": 1000, "status": "发送成功"}
        else:
            return {"code": 1001, "status": "该用户已下线"}

    @socketio.on('disconnect')
    def handle_disconnect():
        socket_id = request.sid
        username = request.args.get('username')
        user_id = request.args.get('userId')
        if user_id in user_map:
            del user_map[user_id]  # 下线后移除user id和对应的socket id
        print(f"用户断连 socket id: {socket_id} username: {username} user_id: {user_id}")
