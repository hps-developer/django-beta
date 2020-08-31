from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('topup/', views.UmoneyReqList.as_view()),
    path('topup/<int:pk>/', views.UmoneyReqDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)