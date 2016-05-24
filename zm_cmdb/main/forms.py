# coding: utf-8
from django import forms

class ApplyForm(forms.Form):
	config = forms.CharField(label='配置', max_length=50, initial='2核4G')
	times = forms.IntegerField(label='台数', min_value=1, initial=1)
	info = forms.CharField(label='备注', max_length=100)
	sgroup = forms.CharField(label='安全组', initial='生产组', max_length=30)
	name = forms.CharField(label='申请人', max_length=30)
	