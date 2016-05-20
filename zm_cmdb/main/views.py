from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Host
import csv
from .zabbix import Zabbix

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
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition']  = 'attachment; filename="zm_hosts.csv"'
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
