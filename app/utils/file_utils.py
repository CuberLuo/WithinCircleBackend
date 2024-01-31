import os
import uuid

import requests

from config import API_BASE_URL


def get_uuid_filename(filename):
    file_id = str(uuid.uuid4()).replace("-", "")
    suffix = os.path.splitext(filename)[1]  # 获取文件的后缀名
    new_file_name = f'{file_id}{suffix}'
    return new_file_name


def dev_file_upload(file, filename, Authorization):
    local_file_path = fr'D:\ProgramData\within-circle-file\{filename}'
    file.save(local_file_path)
    headers = {
        'Authorization': Authorization
    }
    response = requests.post(f'{API_BASE_URL}/file-upload', headers=headers, data={
        'filename': filename
    }, files={
        'pic': open(local_file_path, 'rb')
    })
    print(response.json())
