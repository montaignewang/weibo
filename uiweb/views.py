from django.shortcuts import render,redirect
from .models import Weibo, Topic, Category, Comment, Tags, UserProfile

# Create your views here.

def homepage(request,username):  #个人主页，显示发过的微博

    user =UserProfile.objects.get(user__name=username)  #用户名
    if not user:
        return redirect('/login/login.html')
    weibos = Weibo.objects.filter(user=user).order_by('-date')
    context = {'weibos': weibos, 'user': user}
    return render(request,'uiweb/homepage.html',context)


def index(request):
    return render(request, 'uiweb/index.html')
