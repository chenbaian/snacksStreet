from celery.task import task
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.template import loader
from .utils import create_random_str

@task
def send_confirm_email(user, host):
    # 拼接验证连接
    random_str = create_random_str()

    url = "http://{host}/axf/confirm/{random_str}".format(
        host=host,
        random_str=random_str
    )
    # 发送邮件
    temp = loader.get_template("user/user_confirm.html")
    # 渲染模板
    html = temp.render({"url": url})
    # 拼接邮件的发送内容
    title = "您正在注册axf···"
    msg = ""
    email_from = settings.DEFAULT_FROM_EMAIL
    receives = [user.email]
    send_mail(
        title,
        msg,
        email_from,
        receives,
        fail_silently=False,
        html_message=html
    )
    # 设置缓存
    cache.set(random_str, user.id, settings.CACHE_AGE)
    return True