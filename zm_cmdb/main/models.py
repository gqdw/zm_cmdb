from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HostManager(models.Manager):
	def create_host(self, hostname, eth0, eth1):
		host = self.create(hostname=hostname, eth0=eth0, eth1=eth1)
		return host


class Host(models.Model):
	hostname = models.CharField(unique=True, max_length=30)
	# hostname = models.CharField(max_length=30, unique=True)
	eth0 = models.GenericIPAddressField(unique=True, blank=True, null=True)
	# eth0 = models.GenericIPAddressField(unique=True)
	eth1 = models.GenericIPAddressField(unique=True, blank=True, null=True)
	ismonitor = models.BooleanField(default=False)

	def __unicode__(self):
		return self.hostname
	objects = HostManager()

# 	@classmethod
# 	def create(cls, hostname, eth0, eth1):
# 		host = cls(hostname=hostname, eth0=eth0, eth1=eth1)
# 		return host
class PublicKeyManager(models.Manager):
	def create_key(self, key):
		k = self.create(key=key)
		return k

class PublicKey(models.Model):
	key = models.TextField(unique=True)
	key_shortname = models.TextField(unique=True, null=True)

	def __unicode__(self):
		return self.key
	objects = PublicKeyManager()
