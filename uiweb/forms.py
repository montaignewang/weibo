from django import forms
from .models import Weibo,Comment

class WeiboForm(forms.Form):
    text = forms.CharField(label='', max_length=128,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "发布新微博...",'autofocus': ''}))
    pic = forms.ImageField(required=False)
    forward_weibo_id = forms.IntegerField(widget=forms.HiddenInput,required=False)

class CommentForm(forms.Form):
    text = forms.CharField(label='', max_length=128,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "发布精彩评论...",'autofocus': ''}))
    weibo_id = forms.IntegerField(widget=forms.HiddenInput)
