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
    path('depositinquiry/', views.DepositBalanceInquiryReqList.as_view()),
    path('depositinquiry/<int:pk>/', views.DepositBalanceInquiryReqDetail.as_view()),
    path('depositinquiryresp/', views.DepositBalanceInquiryRespList.as_view()),
    path('transactionaggregation/', views.TransactionAggregationInquiryReqList.as_view()),
    path('transactionaggregation/<int:pk>/', views.TransactionAggregationInquiryReqDetail.as_view()),
    path('transactionaggregationresp/', views.TransactionAggregationInquiryRespList.as_view()),
    path('topupcheck/', views.TopupCheckReqList.as_view()),
    path('topupcheck/<int:pk>/', views.TopupCheckReqDetail.as_view()),
    path('topupcheckresp/', views.TopupCheckRespList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)