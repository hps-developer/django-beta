from django.contrib import admin

# Register your models here.

from .models import UmoneyReq

admin.site.register(UmoneyReq)

# class UmoneyReqList(generics.ListCreateAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer

# class UmoneyReqDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer