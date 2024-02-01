import os


def dir_pre_check(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'目录{dir_path}不存在，已自动创建')
