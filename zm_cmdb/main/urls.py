from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#    url(r'^import/', views.import_data, name='import_data'),
    url(r'^list/', views.list_host, name='list_host'),
	url(r'^out/', views.output_data, name='output_data'),
	url(r'^zabbix', views.ismonitor, name='ismonitor'),
	url(r'^apply', views.apply, name='apply'),

]
