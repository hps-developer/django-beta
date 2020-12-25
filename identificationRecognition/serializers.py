from rest_framework import serializers
from .models import IdentificationRecognition


class IdentificationRecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationRecognition
        fields = ['template', 'idImage']