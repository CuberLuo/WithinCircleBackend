import os
import uuid

import requests

from app.utils.os_utils import dir_pre_check
from config import API_BASE_URL


def get_uuid_filename(filename):
    file_id = str(uuid.uuid4()).replace("-", "")
    suffix = os.path.splitext(filename)[1]  # 获取文件的后缀名
    new_file_name = f'{file_id}{suffix}'
    return new_file_name


def dev_file_upload(file, filename, authorization):
    local_dir_path = r'C:\ProgramData\within-circle-file'
    dir_pre_check(local_dir_path)
    local_file_path = fr'{local_dir_path}\{filename}'
    file.save(local_file_path)
    headers = {
        'Authorization': authorization
    }
    response = requests.post(f'{API_BASE_URL}/file-upload', headers=headers, data={
        'filename': filename
    }, files={
        'pic': open(local_file_path, 'rb')
    })
    print(response.json())
