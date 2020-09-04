from django.contrib import admin

# Register your models here.

from .models import TopupReq
from .models import TopupResp
from .models import ConnectionReq
from .models import ConnectionResp

admin.site.register(TopupReq)
admin.site.register(TopupResp)
admin.site.register(ConnectionReq)
admin.site.register(ConnectionResp)

# class UmoneyReqList(generics.ListCreateAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer

# class UmoneyReqDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer