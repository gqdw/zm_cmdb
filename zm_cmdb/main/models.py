from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Host(models.Model):
	hostname = models.CharField(max_length=30, unique=True)
	eth0 = models.GenericIPAddressField(unique=True)
	eth1 = models.GenericIPAddressField(blank=True, null=True )

