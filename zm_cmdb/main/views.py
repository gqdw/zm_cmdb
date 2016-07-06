# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Host, PublicKey
import csv
from .zabbix import Zabbix
from datetime import datetime
from .forms import ApplyForm, LoginForm, KeysForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from mytools import get_keys, get_cpu_info, get_mem_info, get_disk_info

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


@login_required(login_url='/main/login/')
def list_host(request):
	hosts = Host.objects.all()
	return render(request, 'list.html', {'hosts': hosts})


@login_required(login_url='/main/login/')
def output_data(request):
	today = datetime.today()
	filename = datetime.strftime(today, '%y%m%d')
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="zm_hosts-%s.csv"' % (filename)
	writer = csv.writer(response)
	writer.writerow(['hostname', 'eth0', 'eth1'])
	for h in Host.objects.all():
		alist = []
		alist.append(h.hostname)
		alist.append(h.eth0)
		alist.append(h.eth1)
		writer.writerow(alist)
# 	writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
	return response


@login_required(login_url='/main/login/')
def output_data_txt(request):
	today = datetime.today()
	filename = datetime.strftime(today, '%y%m%d')
	hosts = Host.objects.all()
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename="eth1-%s.txt"' % (filename)
	for h in hosts:
		if h.eth1:
			response.write(h.eth1 + '\n')
	return response


def ismonitor(request):
	Z = Zabbix()
	Z.get_auth()
	Z.get_hostip()
	hosts = Host.objects.all()
	for h in hosts:
		if h.eth0 in Z.hosts:
			h.ismonitor = True
			h.save()
		else:
			h.ismonitor = False
# 	print request.path
	return HttpResponseRedirect('/main/list/')
# 	 return HttpResponse('zabbix status is ok')


@login_required(login_url='/main/login/')
def apply(request):
	if request.method == 'POST':
		form = ApplyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			mtext = u'配置: %s \n台数:%d \n用途: %s \n安全组: %s\n需要连接的rds: %s\n申请人:%s ' % (
				cd['config'], cd['times'], cd['info'], cd['sgroup'], cd['allowdb'], cd['name'])
			send_mail(
				'apply resource', mtext, 'aca_jingru@qq.com', ['monitor@zhai.me'], fail_silently=False)
			return HttpResponse(u'<p>%s</p> <p>已发送</p>' % mtext)
	else:
		form = ApplyForm()
	return render(request, 'apply.html', {'form': form})


def mylogin(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
# 			print cd['username'], cd['password']
			user = authenticate(username=cd['username'], password=cd['password'])
			if user is not None:
				if user.is_active:
					print "user is valid, active and authenticated"
					login(request, user)
# 					return HttpResponse('<h3>登录成功</h3>')
					return HttpResponseRedirect('/main')
				else:
					print "The password is valid, but the account has been disabled!"
			else:
				return HttpResponse('<h3>登录失败</h3>')
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})


def mylogout(request):
	logout(request)
	return HttpResponseRedirect('/main')


def getkeys(request):
	if request.method == 'POST':
		form = KeysForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			hostname = cd['hostname']
			keys = get_keys(hostname)
			# return render(request, 'listkeys.html', {'keys':keys})
			if keys == '':
				return render(request, 'getkeys.html', {'form': form, 'keys': keys, 'nokeys': 1})
			else:
				for k in keys:
					# p1 = PublicKey(key=k)
					# if p1 in PublicKey.objects.all():
					try:
						pk = PublicKey.objects.get(key=k)
					except Exception as e:
						pk = None
					if pk is not None:
						print 'key exists'
					else:
						print 'add key'
						PublicKey.objects.create_key(key=k, key_shortname=k.split()[-1])

				return render(request, 'getkeys.html', {'form': form, 'keys': keys})
	else:
		form = KeysForm()
	return render(request, 'getkeys.html', {'form': form})


def updatekey():
	for k in PublicKey.objects.all():
		if k.key != '':
			k.key_shortname = k.key.split()[-1]
			k.save()


def update_info():
	"""
	update cup,mem,disk info
	"""
	for h in Host.objects.all():
		try:
			cpu = get_cpu_info(h.eth1)
			mem = get_mem_info(h.eth1)
			disk = get_disk_info(h.eth1)
			h.cpu = cpu
			h.mem = mem
			h.disknum = disk
			h.save()
		except Exception as e:
			print e
# 	return HttpResponse('ok')


def keylist(request):
	keys = PublicKey.objects.all()
	return render(request, 'keylist.html', {'keys': keys})


@login_required(login_url='/main/login/')
def gethosteth1(request):
	"""
	return hosts eth1 list
	"""
	hosts = Host.objects.all()
# 	return render(request, 'gethosteth1.html', {'hosts': hosts})
	return render(request, 'api/gethosteth1.html', {'hosts': hosts})


@login_required(login_url='/main/login/')
def gethosteth0(request):
	"""
	return hosts eth1 list
	"""
	hosts = Host.objects.all()
# 	return render(request, 'gethosteth1.html', {'hosts': hosts})
	return render(request, 'api/gethosteth0.html', {'hosts': hosts})
