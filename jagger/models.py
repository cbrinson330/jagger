from django.db import models

class intrest(models.Model):
	name = models.CharField(max_length=200)
	minVal = models.IntegerField()
	maxVal = models.IntegerField()
	dateVals = models.CharField(max_length=800)
	owner = models.ForeignKey('auth.User', default=0)
