from django.contrib import admin
from .models import Host, PublicKey, aliHost
# Register your models here.


class HostAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'eth0', 'eth1', 'cpu', 'mem', 'disknum')
	search_fields = ('hostname', 'eth0', 'eth1')
# list_filter = ('hostname',)
# 	fields = ('hostname', 'eth0', 'eth1')

admin.site.register(Host, HostAdmin)
admin.site.register(PublicKey)
admin.site.register(aliHost)
