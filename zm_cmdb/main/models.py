from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HostManager(models.Manager):
	def create_host(self, hostname, eth0, eth1, cpu=0, mem=0, disknum=0):
		host = self.create(hostname=hostname, eth0=eth0, eth1=eth1, cpu=cpu, mem=mem, disknum=disknum)
		return host


class Host(models.Model):
	hostname = models.CharField(unique=True, max_length=30)
	# hostname = models.CharField(max_length=30, unique=True)
	eth0 = models.GenericIPAddressField(unique=True, blank=True, null=True)
	# eth0 = models.GenericIPAddressField(unique=True)
	eth1 = models.GenericIPAddressField(unique=True, blank=True, null=True)
	ismonitor = models.BooleanField(default=False)
	cpu = models.IntegerField(blank=True, null=True)
	mem = models.IntegerField(blank=True, null=True)
	disknum = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.hostname
	objects = HostManager()


class aliHostManager(models.Manager):
	def create_host(self, InstanceName, PublicIpAddress, InnerIpAddress, IoOptimized, Cpu, Memory, DeviceAvailable, ZoneId):
		host = self.create(InstanceName=InstanceName, PublicIpAddress=PublicIpAddress, InnerIpAddress=InnerIpAddress, IoOptimized=IoOptimized, Cpu=Cpu, Memory=Memory, DeviceAvailable=DeviceAvailable, ZoneId=ZoneId)
		return host


class aliHost(models.Model):
	InstanceName = models.CharField(unique=True, max_length=50)
	PublicIpAddress = models.GenericIPAddressField(unique=True, max_length=50, null=True)
	InnerIpAddress = models.GenericIPAddressField(unique=True, max_length=50)
	IoOptimized = models.BooleanField()
	Cpu = models.IntegerField()
	Memory = models.IntegerField()
	DeviceAvailable = models.BooleanField()
	ZoneId = models.CharField(max_length=30)

	def __unicode__(self):
		return self.InstanceName
	objects = aliHostManager()


class PublicKeyManager(models.Manager):
	def create_key(self, key, key_shortname):
		k = self.create(key=key, key_shortname=key_shortname)
		return k


class PublicKey(models.Model):
	key = models.TextField(unique=True)
	key_shortname = models.TextField(unique=True, null=True)
	key_info = models.CharField(max_length=50, null=True)

	def __unicode__(self):
		return self.key_shortname
	objects = PublicKeyManager()
