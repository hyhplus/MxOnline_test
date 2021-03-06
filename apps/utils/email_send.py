# coding: utf-8
__author__ = 'Evan'

from random import Random
from django.template import loader

# 导入Django自带的邮件模块
from django.core.mail import send_mail, EmailMessage

from users.models import EmailVerifyRecord

# 导入setting中发送邮件的配置
from MxOnline.settings import EMAIL_FROM


def random_str(random_length=8):
    """
    生成随机字符串
    """
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    """
    默认send_type='register'，其他方式重载即可更换send_type='xxxx'
    发送激活邮箱： 注册，忘记密码，修改邮箱等逻辑
    发送之前先保存到数据库，其中修改邮箱时验证码设置为4位
    特别注意：这里的数据保存在数据库，特别是验证码
    """
    email_record = EmailVerifyRecord()

    # 生成随机的code放入链接
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容
    # email_title = 'MxOnline激活邮件'
    # email_body = ''

    if send_type == 'register':
        email_title = 'MxOnline 注册激活链接'
        # email_body = "欢迎注册MxOnline慕课小站:  " \
        #              "请点击下面的链接激活你的账号: " \
        #              "http://127.0.0.1:8000/active/{0}".format(code)

        email_body = loader.render_to_string(
            "users/email_register.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = 'html'
        send_status = msg.send()

        if send_status:
            pass

    elif send_type == 'forget':
        email_title = 'MxOnline 找回密码'
        email_body = loader.render_to_string(
                        'users/email_forget.html', {'active_code': code}
                     )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = 'html'
        send_status = msg.send()
        if send_status:
            pass

    elif send_type == 'update_email':
        # 上面写了code并保存了，这里只需引用code即可，不能再写code=rand_str(4)了，
        # 否则无法验证有效的验证码, 因为code被重新random了，
        # 而且这个code不是数据库这条记录的code了。

        email_title = "mx慕课小站 修改邮箱验证码"
        email_body = loader.render_to_string(
            "user_center/email_update.html",  # 需要渲染的html模板
            {
                "active_code": code, # 参数
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        if send_status:
            pass