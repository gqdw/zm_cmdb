from django.contrib import admin
from .models import Host
# Register your models here.


class HostAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'eth0', 'eth1')
	search_fields = ('hostname', 'eth0', 'eth1')
# list_filter = ('hostname',)
# 	fields = ('hostname', 'eth0', 'eth1')

admin.site.register(Host, HostAdmin)
