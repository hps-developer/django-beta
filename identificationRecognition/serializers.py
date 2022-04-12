from pyrsistent import field
from rest_framework import serializers
from .models import IdentificationRecognition
from .models import IdentificationList
from .models import IdentificationUrlOrName
from .models import GetIdentificationData


class IdentificationRecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationRecognition
        fields = ['template', 'idImage']

class IdentificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationList
        fields = ['idList']

class IdentificationUrlOrNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationUrlOrName
        fields = ['urlOrName']

class Get_IdentificationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetIdentificationData
        fields = ['urlOrName']
        