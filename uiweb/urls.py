from django.urls import path
from . import views


urlpatterns = [
    #path('index/',views.index),
    path('<str:username>/',views.userpage,name='userpage'),  #显示用户发过的微博页面
    path('',views.homepage,name='homepage'), #显示用户关注好友发布的微博
    path('ajax/add_zan',views.add_zan,name='add_zan'),  #处理点赞事件，ajax提交
    path('ajax/add_follow',views.add_follow, name='add_follow')  #处理加关注事件，ajax方式
    #path('comment/<int:weibo_id>/',views.comment,name='comment'),
]
