from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('topup/', views.UmoneyReqList.as_view()),
    path('topup/<int:pk>/', views.UmoneyReqDetail.as_view()),
    path('topupresp/', views.TopupRespList.as_view()),
    path('connection/', views.ConnectionReqList.as_view()),
    path('connection/<int:pk>/', views.ConnectionReqDetail.as_view()),
    path('connectionresp/', views.ConnectionRespList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)