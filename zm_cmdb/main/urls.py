from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#    url(r'^import/', views.import_data, name='import_data'),
    url(r'^list/', views.list_host, name='list_host'),

]
