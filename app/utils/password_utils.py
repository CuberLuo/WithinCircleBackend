import bcrypt


def encrypt(password):
    # 指定生成盐值时使用的算法迭代次数为14,加密强度高
    salt = bcrypt.gensalt(rounds=14)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(input_password, hashed_password):
    if bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    else:
        return False
