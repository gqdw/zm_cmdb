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
