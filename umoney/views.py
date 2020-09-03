from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import generics
from umoney.models import TopupReq, ConnectionReq
from umoney.serializers import TopupReqSerializer, ConnectionReqSerializer
import socket
import functools

stx_hex = '02'
message_length = '0219'
destination_info = '0000'
source_info = 'POS0'
version = '00'
message_data = ''
etx_hex = '03'

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

    queryset = TopupReq.objects.all()
    serializer_class = TopupReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.create(request, *args, **kwargs)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.python.org", 80))
        print('POS0')
        print(toHex('POS0'))
        print(toStr('504F5330'))
        # compile_java('encryptSEED128.java')
        # execute_java('encryptSEED128.java', '')
        # compile_java('decryptSEED128.java')
        # execute_java('decryptSEED128.java', '')
        # hex_str = toHex('POS0')
        # hex_int = int(hex_str, 16)
        # new_int = hex_int + 0x200
        # print(new_int)
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

    queryset = TopupReq.objects.all()
    serializer_class = TopupReqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ConnectionReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = ConnectionReq.objects.all()
    serializer_class = ConnectionReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        message_type_id = '0300'
        primary_bit_map = '2200000008200010'
        processing_code = '481100'
        transmission_date = '0902100912'
        transaction_unique = '000000000001'
        merchant_information = '3010002014                              ' 
        message_request_data_length = '131'
        message_request_data = 'ID1234ID1234ID1222                                                                                                              '
        message_data = ''
        message_data = message_data + message_type_id
        message_data = message_data + primary_bit_map
        message_data = message_data + processing_code
        message_data = message_data + transmission_date
        message_data = message_data + transaction_unique
        message_data = message_data + merchant_information
        message_data = message_data + message_request_data_length
        message_data = message_data + message_request_data
        print(message_data)
        req_data = ''
        req_data = req_data + toStr(stx_hex)
        req_data = req_data + message_length
        req_data = req_data + destination_info
        req_data = req_data + source_info
        req_data = req_data + version
        req_data = req_data + message_data
        req_data = req_data + toStr(etx_hex)
        print(req_data)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("202.126.92.39", 12021))
        s.send(bytes(req_data, encoding='ascii'))
        data = ''
        data = s.recv(4096)
        print(data)
        s.close()
        obj = self.create(request, *args, **kwargs)
        return obj

class ConnectionReqDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = ConnectionReq.objects.all()
    serializer_class = ConnectionReqSerializer

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

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
import urllib
import random


# 16바이트에 모자라면 '\x00'을 뒤에 붙침.
def pad_to_sixteen_bytes(txt):
    if len(txt) < 16:
        txt += '\x00'*(16 - len(txt))
    return txt

def strip_padding(txt):
    idx = txt.find('\x00')
    # no padding in the first place
    if idx == -1:
        return txt
    return txt[:idx]

# use this for encrypting parameters. actually used in API
def encrypt_param(key, txt):
    txt = pad_to_sixteen_bytes(txt)
    cipher_text = encrypt(key, txt)

    encoded = [unichr(sign_byte(each)).encode('utf-8') for each in cipher_text]
    return urllib.quote_plus(''.join(encoded))


# use this for decrypting. actually used in APIs
def decrypt_param(key, cipher_text):
    cipher_text = list(urllib.unquote_plus(cipher_text).decode('utf-8'))
    cipher_text = ''.join(map(chr, map(unsign_byte, cipher_text)))
    return strip_padding(decrypt(key, cipher_text))

# for testing purposes
def generate_text():
    return ''.join([random.choice('0123456789abcdefghjklmnopqrstuxyzABCDEFGHIJKLMNOPQRSTUXYZ') for i in range(16)])

# for testing purposes
def test():
    key = '0123465789abcdef'
    for _ in range(5):
        txt = generate_text()
        print(txt, encrypt_param(key, txt))

# python cryptography documentation.
# seed 128 encryption
def encrypt(key, txt):
    mode = modes.ECB()
    cipher = base.Cipher(
        algorithms.SEED(key),
        mode,
        backend
    )
    encryptor = cipher.encryptor()
    ct = encryptor.update(txt)
    ct += encryptor.finalize()
    return ct

# seed 128 decryption
def decrypt(key, txt):
    mode = modes.ECB()
    cipher = base.Cipher(
        algorithms.SEED(key),
        mode,
        backend
    )
    decryptor = cipher.decryptor()
    ct = decryptor.update(txt)
    ct += decryptor.finalize()
    return ct

# java byte = signed
# python byte = unsigned
# means 0x80 ~ 0xFF needs to be converted.
# see http://stackoverflow.com/questions/4958658/char-into-byte-java
# 65280을 더하는 이유는 ..자바에서 byte를 chr로 강제 캐스팅시 byte가 int형태로 sign_extension되고 그 뒤,
# chr는 2바이트니 결과값의 최하위 바이트 2개를 사용.

def sign_byte(me):
    if ord(me) > 127:
        # java casting rule. from chr to int.
        # 65280 == '\xFF00'
        return 65280 + ord(me)
    else:
        return ord(me)

def unsign_byte(me):
    if ord(me) >= 65280:
        return ord(me) - 65280
    else:
        return ord(me)

""" 
java compiler
"""
import os.path,subprocess
from subprocess import STDOUT,PIPE

def compile_java(java_file):
    print(subprocess.check_call(['pwd']));
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin)
    print (stdout )

"""
End java compiler
"""


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
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''

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


