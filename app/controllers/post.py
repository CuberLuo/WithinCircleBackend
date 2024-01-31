import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from app.models.posts import Posts
from app.status import StatusCode
from config import WEB_BASE_URL
from ..database import db
from ..models.post_likes import PostLikes
from ..models.post_pics import PostPics
from ..models.users import Users
from ..utils import file_utils
from ..utils.file_utils import dev_file_upload

post_bp = Blueprint('post', __name__)


def process_posts(all_posts, user_id):
    posts_list = []
    for post in all_posts:
        user_like_post = False
        post_id = post.id
        post_like_exist = PostLikes.query.filter_by(user_id=user_id, post_id=post_id).first()
        if post_like_exist:  # 检查用户是否点赞该内容
            user_like_post = True
        poster_id = post.user_id  # 内容发布者id
        user_exist = Users.query.filter_by(id=poster_id).first()
        postpic_exist = PostPics.query.filter_by(post_id=post_id)
        postpic_list = []
        postpic_cnt = 0
        for postpic in postpic_exist:
            postpic_dict = {
                'id': postpic_cnt,
                'img_url': postpic.pic_link
            }
            postpic_list.append(postpic_dict)
            postpic_cnt += 1
        post_dict = {
            'id': post.id,
            'user_id': post.user_id,
            'username': user_exist.username,
            'user_avatar': user_exist.avatar_url,
            'post_content': post.post_msg,
            'visible_circle': post.visible_circle,
            'post_date': post.post_date.strftime("%Y-%m-%d %H:%M"),
            'post_images': postpic_list,
            'location': {
                'name': post.loc_name,
                'lat': post.lat,
                'lon': post.lon,
            },
            'like_num': post.like_num,
            'user_like': user_like_post,
            'is_my_post': poster_id == user_id
        }
        posts_list.append(post_dict)
    return posts_list


@post_bp.route('/fileUpload', methods=['POST'])
@jwt_required(optional=False)
def file_upload():
    try:
        pic = request.files['pic']
        filename = request.form.get('filename')
        pic.save(fr'/www/wwwroot/within-circle/images/{filename}')
        res_data = {
            'code': StatusCode.OK,
            'msg': '文件上传成功'
        }
        return jsonify(res_data)
    except Exception as e:
        print('file_upload', e)
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '文件上传失败'
        }
        return jsonify(res_data)


@post_bp.route('/uploadPost', methods=['POST'])
@jwt_required(optional=False)
def upload_post():
    user_id = get_jwt_identity()
    pic_list = request.files.getlist('pic_list')
    print(pic_list)
    message = request.form.get('message')
    location = request.form.get('location')
    visible_circle = request.form.get('visible_circle')
    loc_name, lon, lat = location.split(',')
    new_post = Posts(user_id, message, visible_circle, loc_name, lat, lon)
    post_id = new_post.id

    try:
        db.session.add(new_post)
        db.session.commit()
        for pic in pic_list:
            new_filename = file_utils.get_uuid_filename(pic.filename)
            if os.environ.get('FLASK_ENV') == 'development':
                dev_file_upload(pic, new_filename, request.headers.get('Authorization'))
            else:
                pic.save(fr'/www/wwwroot/within-circle/images/{new_filename}')  # r表示忽略所有的转义字符
            new_post_pics = PostPics(post_id, f'{WEB_BASE_URL}/images/{new_filename}')
            db.session.add(new_post_pics)
            db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '发布成功'
        }
        return jsonify(res_data)
    except Exception as e:
        print('upload_post', e)
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '发布失败'
        }
        return jsonify(res_data)


@post_bp.route('/getAllPosts', methods=['GET'])
@jwt_required(optional=False)
def get_all_posts():
    user_id = get_jwt_identity()
    all_posts = Posts.query.order_by(desc(Posts.post_date)).all()

    posts_list = process_posts(all_posts, user_id)

    res_data = {
        'code': StatusCode.OK,
        'data': posts_list,
        'msg': '成功'
    }
    return jsonify(res_data)


@post_bp.route('/getPageSizePosts', methods=['GET'])
@jwt_required(optional=False)
def get_page_size_posts():
    user_id = get_jwt_identity()
    page = int(request.args.get('page'))
    page_size = int(request.args.get('page_size'))
    all_posts = Posts.query.order_by(desc(Posts.post_date)).offset((page - 1) * page_size).limit(page_size).all()
    posts_list = process_posts(all_posts, user_id)
    res_data = {
        'code': StatusCode.OK,
        'data': posts_list,
        'msg': '成功'
    }
    return jsonify(res_data)


@post_bp.route('/likePost', methods=['POST'])
@jwt_required(optional=False)
def like_post():
    user_id = get_jwt_identity()
    post_id = request.get_json()['post_id']
    post_exist = Posts.query.filter_by(id=post_id).first()
    post_like_exist = PostLikes.query.filter_by(user_id=user_id, post_id=post_id).first()
    if post_like_exist:
        post_exist.like_num -= 1
        db.session.delete(post_like_exist)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '取消点赞成功'
        }
        return jsonify(res_data)
    else:
        new_post_like = PostLikes(post_id, user_id)
        post_exist.like_num += 1
        db.session.add(new_post_like)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '点赞成功'
        }
        return jsonify(res_data)


@post_bp.route('/getMyPosts', methods=['GET'])
@jwt_required(optional=False)
def get_my_posts():
    user_id = get_jwt_identity()
    all_posts = Posts.query.filter_by(user_id=user_id).order_by(desc(Posts.post_date)).all()
    posts_list = process_posts(all_posts, user_id)
    res_data = {
        'code': StatusCode.OK,
        'data': posts_list,
        'msg': '成功'
    }
    return jsonify(res_data)


@post_bp.route('/deletePost', methods=['POST'])
@jwt_required(optional=False)
def delete_post():
    user_id = get_jwt_identity()
    post_id = request.get_json()['post_id']
    post_exist = Posts.query.filter_by(id=post_id).first()
    if user_id == post_exist.user_id:
        db.session.delete(post_exist)
        db.session.commit()
        res_data = {
            'code': StatusCode.OK,
            'msg': '删除成功'
        }
        return jsonify(res_data)
    else:
        res_data = {
            'code': StatusCode.ERROR,
            'msg': '删除失败'
        }
        return jsonify(res_data)


@post_bp.route('/getMyLikePosts', methods=['GET'])
@jwt_required(optional=False)
def get_my_like_posts():
    user_id = get_jwt_identity()
    all_post_likes = PostLikes.query.filter_by(user_id=user_id).order_by(desc(PostLikes.like_date)).all()
    all_posts = []
    for post_like in all_post_likes:
        post_id = post_like.post_id
        post = Posts.query.filter_by(id=post_id).first()
        all_posts.append(post)
    posts_list = process_posts(all_posts, user_id)
    res_data = {
        'code': StatusCode.OK,
        'data': posts_list,
        'msg': '成功'
    }
    return jsonify(res_data)
