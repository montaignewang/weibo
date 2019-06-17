from django.shortcuts import render,redirect
from .models import Weibo, Topic, Category, Comment, Tags, UserProfile
from . import models
from .forms import WeiboForm
import datetime

# Create your views here.

def userpage(request,username):  #个人主页，显示发过的微博

    user =UserProfile.objects.get(user__name=username)  #用户名
    if not user:
        return redirect('/login/login.html')
    weibos = Weibo.objects.filter(user=user).order_by('-date')
    context = {'weibos': weibos, 'user': user}
    return render(request,'uiweb/userpage.html',context)


def homepage(request):
    if not request.session.get('is_login',None):  #如果未登陆则转到登陆界面
        return redirect('/login/')
    username = request.session['user_name']
    user = UserProfile.objects.get(user__name=username)  #获取已登陆的用户名

    if request.method == 'POST':
        weibo_form = WeiboForm(request.POST)

        if weibo_form.is_valid():
            new_weibo = models.Weibo()
            new_weibo.user = user
            new_weibo.wb_type = 0
            new_weibo.text = weibo_form.cleaned_data.get('text')
            new_weibo.perm = 0
            new_weibo.pictures_link_id=''
            new_weibo.video_link_id=''
            new_weibo.date = datetime.datetime.now()
            new_weibo.save()
            return redirect('/u/')
    else:
        weibo_form = WeiboForm()

    f_usernames = []
    for u in user.follow_list.all():  #获取用户关注者的姓名列表
        f_usernames.append(u.user.name)

    f_weibos = Weibo.objects.filter(user__user__name__in=f_usernames).order_by('-date')  #获取关注者的微博列表
    context={'f_weibos':f_weibos,'user':user,'weibo_form':weibo_form}

    return render(request,'uiweb/homepage.html',context=context)

