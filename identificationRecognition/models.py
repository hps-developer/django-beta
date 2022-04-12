from django.db import models
from jsonfield import JSONField

# Create your models here.

class IdentificationRecognition(models.Model):
    template = models.CharField(max_length=250)
    idImage = models.CharField(max_length=250)
    # idExist = models.BooleanField(blank=False)

class IdentificationList(models.Model):
    idList = JSONField()

class IdentificationUrlOrName(models.Model):
    urlOrName = models.CharField(max_length=250)

class GetIdentificationData(models.Model):
    urlOrName = models.CharField(max_length=250)

