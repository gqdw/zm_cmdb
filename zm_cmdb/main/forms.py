# coding: utf-8
from django import forms


class ApplyForm(forms.Form):
	config = forms.CharField(label='配置', max_length=50, initial='2核4G')
	times = forms.IntegerField(label='台数', min_value=1, initial=1)
	info = forms.CharField(label='用途', max_length=100)
	sgroup = forms.CharField(label='安全组', initial='生产组', max_length=30)
	allowdb = forms.CharField(label='需要连接的rds', initial='xx.mysql.rds.aliyuncs.com', max_length=100)
	name = forms.CharField(label='申请人', max_length=30)


class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput())
	
class KeysForm(forms.Form):
	hostname = forms.CharField(max_length=30)
