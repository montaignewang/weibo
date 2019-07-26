from django.urls import path
from . import views


urlpatterns = [
    #path('index/',views.index),
    path('<str:username>/',views.userpage,name='userpage'),  #显示用户发过的微博页面
    path('',views.homepage,name='homepage'), #显示用户关注好友发布的微博
    path('ajax/add_zan',views.add_zan,name='homepage'),
    #path('comment/<int:weibo_id>/',views.comment,name='comment'),
]
