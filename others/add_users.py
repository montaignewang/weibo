#创建新用户
import sys
sys.path.append('../')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","weibo.settings")
import django
django.setup()

from login.models import User
from login.views import hash_code
from uiweb.models import UserProfile

def add_user(username, password, email, sex):
    same_name_user = User.objects.filter(name=username)
    if same_name_user:
        message = '用户名已存在'
        return None
    same_email_user = User.objects.filter(email=email)
    if same_email_user:
        message = '该邮箱已经被注册了！'
        return None

    new_user = User()
    new_user.name = username
    new_user.password = hash_code(password)
    new_user.email = email
    new_user.sex = sex
    new_user.has_confirmed = True  #直接跳过邮件确认
    new_user.save()

    new_userprofile = UserProfile()
    new_userprofile.user = new_user
    new_userprofile.save()
    new_userprofile.follow_list.add(new_userprofile)
    new_userprofile.save()

    return

def add_users(start_num, end_num):
    # start_num及end_num需是两个整数
    for i in range(int(start_num), int(end_num)+1):
        username = 'user' + str(i)
        password = 'user' + str(i) + 'pwd'
        email = 'user'+ str(i) +'@qq.com'
        if int(i) % 2 == 0:
            sex = '女'
        else:
            sex = '男'
        add_user(username,password,email,sex)

def main():
    add_users(1,10)

if __name__ == '__main__':
    main()