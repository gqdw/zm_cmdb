# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Host
import csv
from .zabbix import Zabbix
from datetime import datetime
from .forms import ApplyForm
from django.core.mail import send_mail

# Create your views here.

def import_data(request):
	with open('/Users/aca/Downloads/ecs_list0513.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			# print row[0]
			Host.objects.create_host(row[0], row[2], row[1])
	return HttpResponse('ok')

def reg(request):
	return render(request, 'reg.html')

def index(request):
	# return HttpResponse('Hello world!')
	return render(request, 'index.html')

def list_host(request):
	hosts = Host.objects.all()
	return render(request, 'list.html', {'hosts':hosts} )

def output_data(request):
	today = datetime.today()
	filename = datetime.strftime(today,'%y%m%d')
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition']  = 'attachment; filename="zm_hosts-%s.csv"' % (filename)
	writer = csv.writer(response)
	writer.writerow(['hostname', 'eth0', 'eth1'])
	for h in Host.objects.all():
		alist = []
		alist.append(h.hostname)
		alist.append(h.eth0)
		alist.append(h.eth1)
		writer.writerow(alist)
#	writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
	return response

def ismonitor(request):
	Z = Zabbix()
	Z.get_auth()
	Z.get_hostip()
	hosts = Host.objects.all()
	for h in hosts:
	#	print h.eth0
		if h.eth0 in Z.hosts:
			h.ismonitor = True
			h.save()
		else:
			h.ismonitor = False
#	print request.path
	return HttpResponseRedirect('/main/list/')
	# return HttpResponse('zabbix status is ok')

def apply(request):
	if request.method == 'POST':
		form = ApplyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			mtext = u'配置: %s \n台数:%d \n用途: %s \n安全组: %s\n需要连接的rds: %s\n申请人:%s ' % (cd['config'], 
				cd['times'], cd['info'], cd['sgroup'], cd['allowdb'], cd['name'])
			send_mail('apply resource', mtext, 'aca_jingru@qq.com',
			    ['monitor@zhai.me'], fail_silently=False)	
			return HttpResponse(u'<p>%s</p> <p>已发送</p>' % mtext)
	else:
		form = ApplyForm()
	return render(request, 'apply.html', {'form':form})


def login(request):
	return render(request, 'login.html')
