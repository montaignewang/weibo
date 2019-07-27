from django.shortcuts import render,redirect
from .models import Weibo, Topic, Category, Comment, Tags, UserProfile, Zan
from . import models
from .forms import WeiboForm,CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
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

    if request.method == 'POST' and 'add_weibo' in request.POST:
        weibo_form = WeiboForm(request.POST or None, request.FILES or None)

        if weibo_form.is_valid():
            new_weibo = models.Weibo()
            new_weibo.user = user
            new_weibo.wb_type = 0
            new_weibo.text = weibo_form.cleaned_data.get('text')
            new_weibo.pic = weibo_form.cleaned_data.get('pic')
            new_weibo.perm = 0
            new_weibo.pictures_link_id=''
            new_weibo.video_link_id=''
            new_weibo.save()
            return redirect('/u/')
    elif request.method  == 'POST' and 'add_comment' in request.POST:
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            weibo_id = comment_form.cleaned_data.get('weibo_id')
            weibo_to_comment = Weibo.objects.get(id=weibo_id)
            new_comment = Comment()
            new_comment.to_weibo = weibo_to_comment
            new_comment.user = user
            new_comment.comment = comment_form.cleaned_data.get('text')
            new_comment.save()
            return redirect('/u/')
    elif request.method == 'POST' and 'add_forward' in request.POST:
        weibo_form = WeiboForm(request.POST or None, request.FILES or None)
        if weibo_form.is_valid():
            forward_weibo_id = weibo_form.cleaned_data.get('forward_weibo_id')
            forward_weibo = Weibo.objects.get(id=forward_weibo_id)

            new_weibo = models.Weibo()
            new_weibo.user = user
            new_weibo.wb_type = 0
            new_weibo.text = weibo_form.cleaned_data.get('text')
            new_weibo.pic = weibo_form.cleaned_data.get('pic')
            new_weibo.forward_or_collect_from = forward_weibo
            new_weibo.perm = 0
            new_weibo.pictures_link_id=''
            new_weibo.video_link_id=''
            new_weibo.save()
            return redirect('/u/')

    else:
        weibo_form = WeiboForm()
        comment_form = CommentForm()

    f_usernames = []
    for u in user.follow_list.all():  #获取用户关注者的姓名列表
        f_usernames.append(u.user.name)

    f_weibos = Weibo.objects.filter(user__user__name__in=f_usernames).order_by('-date')  #获取关注者的微博列表
    #评论数和点赞数

    context={'f_weibos':f_weibos,'user':user,'weibo_form':weibo_form,'comment_form': comment_form,}

    return render(request,'uiweb/homepage.html',context=context)

#点赞事件处理，ajax
@csrf_exempt
def add_zan(request):
    if not request.session.get('is_login',None):  #如果未登陆则转到登陆界面
        return redirect('/login/')
    username = request.session['user_name']
    user = UserProfile.objects.get(user__name=username)  #获取已登陆的用户名

    if request.method == 'POST':
        weibo_id = request.POST.get('weibo_id')
        zan_to_weibo = Weibo.objects.get(id=weibo_id)
        if zan_to_weibo.zan_set.filter(user=user):  #如果已点过赞
            zan_to_weibo.zan_set.filter(user=user).delete()  #点过赞的则取消
        else:   #没点过赞，则记录点赞事件
            new_zan = Zan()
            new_zan.user = user  # 点赞的是已登陆的用户
            new_zan.to_weibo = zan_to_weibo
            new_zan.save()
        zan_num = Zan.objects.filter(to_weibo=zan_to_weibo).count()
        return_json = {'zan_num': zan_num}
        return HttpResponse(json.dumps(return_json), content_type='application/json')

@csrf_exempt
def add_follow(request):
    if not request.session.get('is_login',None):  #如果未登陆则转到登陆界面
        return redirect('/login/')
    username = request.session['user_name']
    user = UserProfile.objects.get(user__name=username)  #获取已登陆的用户名

    if request.method == 'POST':
        weibo_id = request.POST.get('weibo_id')  # 处理的微博id
        follow_to_weibo = Weibo.objects.get(id=weibo_id)
        weibo_user = follow_to_weibo.user

        if weibo_user in user.follow_list.all():
            user.follow_list.remove(weibo_user)  #如果已关注则取消关注
            text = '+关注'
            user.save()
        else:
            user.follow_list.add(weibo_user)
            text = '已关注'
            user.save()
        return_json = {'text': text}
        return HttpResponse(json.dumps(return_json), content_type='application/json')



'''
def comment(request, weibo_id):
    if not request.session.get('is_login',None):  #如果未登陆则转到登陆界面
        return redirect('/login/')
    username = request.session['user_name']
    user = UserProfile.objects.get(user__name=username)  # 获取已登陆的用户名
    if not Weibo.objects.get(id=weibo_id):  #如果该id的微博不存在
        return redirect('/u/')
    weibo_to_comment = Weibo.objects.get(id=weibo_id)


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = Comment()
            new_comment.user = user
            new_comment.text = comment_form.cleaned_data.get('text')
            new_comment.to_weibo = weibo_to_comment
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'comment_form': comment_form,'weibo': weibo_to_comment,}
    return render(request,'uiweb/homepage.html',context=context)
'''