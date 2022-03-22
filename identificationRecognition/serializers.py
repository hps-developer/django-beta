from pyrsistent import field
from rest_framework import serializers
from .models import IdentificationRecognition
from .models import IdentificationList
from .models import IdentificationUrlOrName


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