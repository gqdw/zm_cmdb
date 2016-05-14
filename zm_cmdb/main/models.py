from __future__ import unicode_literals

from django.db import models

# Create your models here.
class HostManager(models.Manager):
	def create_host(self, hostname, eth0, eth1):
		host = self.create(hostname=hostname, eth0=eth0, eth1=eth1)
		return host



class Host(models.Model):
	hostname = models.CharField(max_length=30, unique=True)
	eth0 = models.GenericIPAddressField(unique=True)
	eth1 = models.GenericIPAddressField(blank=True, null=True )
	
	objects = HostManager()

#	@classmethod
#	def create(cls, hostname, eth0, eth1):
#		host = cls(hostname=hostname, eth0=eth0, eth1=eth1)
#		return host


