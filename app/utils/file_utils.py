import os
import uuid

import oss2


def get_uuid_filename(filename):
    file_id = str(uuid.uuid4()).replace("-", "")
    suffix = os.path.splitext(filename)[1]  # 获取文件的后缀名
    new_file_name = f'{file_id}{suffix}'
    return new_file_name


def image_upload_oss(file, filename):
    file_size = os.fstat(file.stream.fileno()).st_size
    print(f'file_size:{file_size / 1024}KB')
    # 上传的文件大小不得超过10MB
    if file_size / (1024 * 1024) > 10:
        return 500, ''

    endpoint = 'https://oss-cn-hangzhou.aliyuncs.com'

    auth = oss2.Auth(
        os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    bucket_name = 'withincircle'
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    dir_name = 'images'
    key = f'{dir_name}/{filename}'

    # 上传
    result = bucket.put_object(key, file)
    # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
    print('request_id: {0}'.format(result.request_id))
    # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
    print('ETag: {0}'.format(result.etag))
    file_url = f'https://{bucket_name}.oss-cn-hangzhou.aliyuncs.com/{key}'

    return result.status, file_url
