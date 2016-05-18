from django.shortcuts import render
from django.http import HttpResponse
from .models import Host
import csv

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
