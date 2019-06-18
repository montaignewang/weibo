from django.db import models
from login.models import User

# Create your models here.

class Weibo(models.Model):  #所有微博
    wb_type_choices = (
        (0,'new'),
        (1,'forward'),
        (2,'collect'),
    )
    wb_type = models.IntegerField(choices=wb_type_choices,default=0)
    #forward_or_collect_from = models.ForeignKey('self', related_name='forward_or_collects', blank=True, null=True)
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    pic = models.ImageField(upload_to='wb_pic/%Y%m%d',null=True, blank=True)
    pictures_link_id = models.CharField(max_length=128,blank=True,null=True)
    video_link_id = models.CharField(max_length=128,blank=True,null=True)
    perm_choice = (
        (0,'public'),
        (1,'private'),
        (2,'friends')
    )
    perm = models.IntegerField(choices=perm_choice,default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Topic(models.Model):  #话题
    name = models.CharField(max_length=140)
    date = models.DateTimeField()
    def __str__(self):
        return self.name

class Category(models.Model):  #微博分类
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Comment(models.Model): #评论
    to_weibo = models.ForeignKey(Weibo,on_delete=models.CASCADE)
    #p_comment = models.ForeignKey('self',related_name='child_comments')
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    comment_type_choices = ((0,'comment'),(1,'thumb_up'))
    comment_type = models.IntegerField(choices=comment_type_choices,default=0)
    comment = models.CharField(max_length=140)
    date = models.DateTimeField(auto_created=True)
    def __str__(self):
        return self.comment

class Tags(models.Model):  #标签
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class UserProfile(models.Model):  #用户信息
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    brief = models.CharField(max_length=140,blank=True,null=True)
    age = models.PositiveSmallIntegerField(blank=True,null=True)
    tags = models.ManyToManyField(Tags)
    head_img = models.ImageField(upload_to="head_img/%Y%m%d/",blank=True)
    follow_list = models.ManyToManyField('self', blank=True, related_name="my_followers", symmetrical=False)
    def __str__(self):
        return self.user.name

