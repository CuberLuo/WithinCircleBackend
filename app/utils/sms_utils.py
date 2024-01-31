import os
import random

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models


def create_client(
        access_key_id: str,
        access_key_secret: str,
):
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    config.endpoint = f'dysmsapi.aliyuncs.com'
    return Dysmsapi20170525Client(config)


def send_sms_code(phone: str, sms_code: str):
    print(f"手机号:{phone}")

    sms_param = {"code": sms_code}
    client = create_client(os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
                           os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
        sign_name='方圆几里',
        template_code='SMS_463775932',
        phone_numbers=phone,
        template_param=str(sms_param)
    )
    runtime = util_models.RuntimeOptions()
    response = client.send_sms_with_options(send_sms_request, runtime)
    return response.body.code


def generate_code():
    # 生成5位数的随机整数
    random_number = random.randint(10000, 99999)
    print(f"生成验证码:{random_number}")
    return random_number
