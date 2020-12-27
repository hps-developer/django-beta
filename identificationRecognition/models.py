from django.db import models

# Create your models here.

class IdentificationRecognition(models.Model):
    template = models.CharField(max_length=250)
    idImage = models.CharField(max_length=250)
    # idExist = models.BooleanField(blank=False)


    