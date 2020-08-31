from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import generics
from umoney.models import UmoneyReq
from umoney.serializers import UmoneyReqSerializer
import socket
import functools

# @api_view(['GET', 'POST'])
# def umoney_req_list(request, format=None):
#     """
#     List all code UmoneyReq, or create a new UmoneyReq.
#     """
#     if request.method == 'GET':
#         snippets = UmoneyReq.objects.all()
#         serializer = UmoneyReqSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UmoneyReqSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def umoney_req_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code UmoneyReq.
#     """
#     try:
#         snippet = UmoneyReq.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UmoneyReqSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UmoneyReqSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class UmoneyReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = UmoneyReq.objects.all()
    serializer_class = UmoneyReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.create(request, *args, **kwargs)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('POS0')
        print(toHex('POS0'))
        hex_str = toHex('POS0')
        hex_int = int(hex_str, 16)
        new_int = hex_int + 0x200
        print(new_int)
        s.connect(("www.python.org", 80))
        totalsent = 0
        # while totalsent < 1000:
        #     sent = self.sock.send(msg[totalsent:])
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     totalsent = totalsent + sent
        return obj

class UmoneyReqDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = UmoneyReq.objects.all()
    serializer_class = UmoneyReqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# class UmoneyReqList(generics.ListCreateAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer

# class UmoneyReqDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UmoneyReq.objects.all()
#     serializer_class = UmoneyReqSerializer

#convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return functools.reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < 1000:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                # self.sock.close()
                raise RuntimeError("socket connection broken")
                
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 3000:
            chunk = self.sock.recv(min(3000 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        # self.sock.close()
        return b''.join(chunks)


