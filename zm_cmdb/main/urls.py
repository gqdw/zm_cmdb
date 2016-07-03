from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#    url(r'^import/', views.import_data, name='import_data'),
    url(r'^list/', views.list_host, name='list_host'),
	url(r'^out/', views.output_data, name='output_data'),
	url(r'^zabbix', views.ismonitor, name='ismonitor'),
	url(r'^apply', views.apply, name='apply'),
	url(r'^login', views.mylogin, name='mylogin'),
	url(r'^logout', views.mylogout, name='mylogout'),
	url(r'^getkeys', views.getkeys, name='getkeys'),
	url(r'^keylist', views.keylist, name='keylist'),
	# url(r'^gethosteth1', views.keylist),
	url(r'^gethosteth1', views.gethosteth1, name='gethosteth1'),
	url(r'^gethosteth0', views.gethosteth0, name='gethosteth0'),

]
