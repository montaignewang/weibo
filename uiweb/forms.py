from django import forms

class WeiboForm(forms.Form):
    text = forms.CharField(label='发布微博', max_length=128)