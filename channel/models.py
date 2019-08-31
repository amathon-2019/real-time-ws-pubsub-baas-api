from django.db import models

class Channels_Ids(models.Model):
	lists = models.CharField(max_length=100)

class Channels(models.Model):
	name = models.CharField(max_length=50, null=True)
	Client_count = models.IntegerField()
	RPM = models.IntegerField()

class Servers(models.Model):
	Count = models.IntegerField()
	state = models.CharField(max_length=10)




