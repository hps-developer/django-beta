from django.urls import include, path, re_path
from .views import IdentificationRecognitionView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'identificationRecognition', IdentificationRecognitionView, 'IdentificationRecognition')

urlpatterns = [
    path('api/', include(router.urls)),
]
