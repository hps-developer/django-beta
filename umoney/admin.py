from django.contrib import admin

# Register your models here.

from .models import TopupReq
from .models import ConnectionReq

admin.site.register(TopupReq)
admin.site.register(ConnectionReq)

# class UmoneyReqList(generics.ListCreateAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer

# class UmoneyReqDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer