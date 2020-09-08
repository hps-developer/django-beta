from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from umoney.models import TopupReq, TopupResp, ConnectionReq, ConnectionResp
from umoney.serializers import TopupReqSerializer, TopupRespSerializer, ConnectionReqSerializer, ConnectionRespSerializer
from umoney.models import DepositBalanceInquiryReq, DepositBalanceInquiryResp
from umoney.serializers import DepositBalanceInquiryReqSerializer, DepositBalanceInquiryRespSerializer
from umoney.models import TransactionAggregationInquiryReq, TransactionAggregationInquiryResp
from umoney.serializers import TransactionAggregationInquiryReqSerializer, TransactionAggregationInquiryRespSerializer
import socket
import functools
from datetime import datetime
import pytz
from django.db.models import Max

master_key = '30313233343536373839414243444546'

PDA_processing_code = '486000'

stx_hex = '02'
message_length = '0219'
destination_info = '0000'
source_info = 'POS0'
version = '00'
message_data = ''
etx_hex = '03'

message_request_data = 'ID1234ID1234ID1222                                                                                                              '    
pos_id = 'ID1234ID1234ID1222'
merchant_information = '3010002014                              ' 
authentication_id = '197AFA642645A992'
  

OID_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'encrypted_wk': 231,
    'min_topup_amount': 241,
    'tcp_addr1': 305,
    'tcp_port1': 311,
    'tcp_addr2': 375,
    'tcp_port2': 381,
    'merchant_name': 531,
    'system_datetime': 545,
    'filler_space': 711,
    'etx': 712
}

PDA_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'encrypted_vsam': 231,
    'filler_space': 327,
    'etx': 328
}

OTU_first_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'card_number': 215,
    'vsam_tran_seq_number': 225,
    'card_balance': 235,
    'topup_amount': 245,
    'sign2': 253,
    'deposit_balance': 263,
    'filler_space': 327,
    'etx': 328
}


OTU_second_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'deposit_balance': 209,
    'filler_space': 327,
    'etx': 328
}

DBI_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'deposit_balance': 209,
    'filler_space': 327,
    'etx': 328
}
TAI_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'topup_count': 204,
    'topup_amount': 214,
    'topup_cancellation_count': 219,
    'topup_cancellation_amount': 229,
    'payment_count': 234,
    'payment_amount': 244,
    'payment_cancellation_count': 249,
    'payment_cancellation_amount': 259,
    'filler_space': 327,
    'etx': 328
}

class UmoneyReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = TopupReq.objects.all()
    serializer_class = TopupReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        message_type_id = '0200'
        primary_bit_map = '2200000008200010'
        processing_code = '183100'
        transaction_unique = create_transaction_unique()
        topup_req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 3, '', '', request.data)
        print(topup_req_data.encode("ascii"))
        data = send_socket_receive_data(topup_req_data)
        request.data['message_type_id'] = message_type_id
        request.data['primary_bit_map'] = primary_bit_map
        request.data['processing_code'] = processing_code
        request.data['transaction_unique'] = transaction_unique
        request.data['transmission_datetime'] = topup_req_data[41:51]
        request.data['terminal_id'] = merchant_information[0:10]
        request.data['request_data_len'] = '131'
        
        resp_data = data_to_array_by_type(OTU_first_response_len_arr, data)
        OTU_first_resp_data = {
            'comment': request.data['comment'], 
            'message_type_id': resp_data['message_type_id'], 
            'primary_bit_map': resp_data['primary_bit_map'], 
            'processing_code': resp_data['processing_code'],
            'response_code': resp_data['response_code'],
            'transmission_datetime': resp_data['transmission_datetime'],
            'transaction_unique': resp_data['transaction_uniq'],
            'terminal_id': merchant_information[0:10],
            'result_message_len': resp_data['result_message_len'],
            'result_message_data': resp_data['result_message_data'],
            'tran_type': request.data['tran_type'],
            'card_number': resp_data['card_number'],
            'vsam_tran_seq_num': resp_data['vsam_tran_seq_number'],
            'card_balance': resp_data['card_balance'],
            'topup_amount': resp_data['topup_amount'],
            'sign2': resp_data['sign2'],
            'deposit_balance': resp_data['deposit_balance'],
            'payment_method': request.data['payment_method'],
            'sign1': request.data['sign1']
        }
        serializer = TopupRespSerializer(data=OTU_first_resp_data)
        if serializer.is_valid():
            serializer.save()

        obj = self.create(request, *args, **kwargs)
        return Response({ 'request': obj.data, 'result': serializer.data })

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

class TopupRespList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = TopupResp.objects.all()
    serializer_class = TopupRespSerializer

    def get(self, request, *args, **kwargs):
        create_transaction_unique()
        return self.list(request, *args, **kwargs)

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
        transaction_unique = create_transaction_unique()
        req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 1)
        data = send_socket_receive_data(req_data)
        resp_data = data_to_array_by_type(OID_response_len_arr, data)

        encrypted_wk = resp_data['encrypted_wk']
        res = decrypt_seed128(transaction_unique + merchant_information[6:10], encrypted_wk, master_key)
        decrypted_wk = res.decode("ascii")
        request.data['message_type_id'] = message_type_id
        request.data['primary_bit_map'] = primary_bit_map
        request.data['processing_code'] = processing_code
        request.data['merchant_information_terminal_id'] = merchant_information
        request.data['terminal_id'] = merchant_information
        if request.data['pos_id'] == '':
            request.data['pos_id'] = pos_id
        request.data['transaction_unique'] = transaction_unique
        obj = self.create(request, *args, **kwargs)

        oid_resp_data = {
            'message_type_id': resp_data['message_type_id'],
            'primary_bit_map': resp_data['primary_bit_map'],
            'processing_code': resp_data['processing_code'],
            'response_code': resp_data['response_code'],
            'transmission_datetime': resp_data['transmission_datetime'],
            'transaction_unique': resp_data['transaction_uniq'],
            'merchant_id': resp_data['merchant_id'],
            'merchant_info_terminal_id': resp_data['merchant_info'][0:10],
            'result_message_len': resp_data['result_message_len'],
            'result_message_data': resp_data['result_message_data'],
            'response_data_len': resp_data['response_data_len'],
            'working_key': decrypted_wk,
            'minimum_topup_amount': resp_data['min_topup_amount'],
            'system_datetime': resp_data['system_datetime'],
            'pos_id': request.data['pos_id'], 
            'terminal_id': merchant_information, 
            'authentication_id': '', 
        }
        serializer = ConnectionRespSerializer(data=oid_resp_data)
        if serializer.is_valid():
            serializer.save()
        message_type_id = '0300'
        primary_bit_map = '2200000008200010'
        processing_code = '486000'
        transaction_unique = create_transaction_unique()
        req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 2, authentication_id, decrypted_wk)
        pda_req_data = {
            'message_type_id': message_type_id,
            'primary_bit_map': primary_bit_map,
            'processing_code': processing_code,
            'transmission_datetime': '',
            'transaction_unique': transaction_unique,
            'merchant_info_terminal_id': merchant_information[0:10],
            'pos_id': pos_id, 
            'terminal_id': merchant_information[0:10], 
            'authentication_id': authentication_id, 
            'vsam_id': ''
        }
        serializer = ConnectionReqSerializer(data=pda_req_data)
        if serializer.is_valid():
            serializer.save()

        data = send_socket_receive_data(req_data)
        PDA_resp_data = data_to_array_by_type(PDA_response_len_arr, data)

        pda_resp_data_model = {
            'message_type_id': PDA_resp_data['message_type_id'],
            'primary_bit_map': PDA_resp_data['primary_bit_map'],
            'processing_code': PDA_resp_data['processing_code'],
            'response_code': resp_data['response_code'],
            'transmission_datetime': PDA_resp_data['transmission_datetime'],
            'transaction_unique': PDA_resp_data['transaction_uniq'],
            'merchant_id': PDA_resp_data['merchant_id'],
            'merchant_info_terminal_id': PDA_resp_data['merchant_info'][0:10],
            'result_message_len': PDA_resp_data['result_message_len'],
            'result_message_data': PDA_resp_data['result_message_data'],
            'response_data_len': PDA_resp_data['response_data_len'],
            'working_key': decrypted_wk,
            'minimum_topup_amount': '',
            'system_datetime': '',
            'pos_id': pos_id, 
            'terminal_id': PDA_resp_data['merchant_info'][0:10], 
            'authentication_id': authentication_id, 
            'vsam_id': decrypt_seed128(PDA_resp_data['transaction_uniq'] + PDA_resp_data['merchant_info'][6:10], PDA_resp_data['encrypted_vsam'], decrypted_wk).decode("ascii")
        }
        serializer = ConnectionRespSerializer(data=pda_resp_data_model)
        if serializer.is_valid():
            print('hihi')
            serializer.save()
        return Response({})

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

class ConnectionRespList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = ConnectionResp.objects.all()
    serializer_class = ConnectionRespSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DepositBalanceInquiryReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = DepositBalanceInquiryReq.objects.all()
    serializer_class = DepositBalanceInquiryReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        message_type_id = '0100'
        primary_bit_map = '2200000008200010'
        processing_code = '191100'
        transaction_unique = create_transaction_unique()
        deposit_inquiry_req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 5, '', '', request.data)
        request.data['message_type_id'] = message_type_id
        request.data['primary_bit_map'] = primary_bit_map
        request.data['processing_code'] = processing_code
        request.data['transaction_unique'] = transaction_unique
        request.data['transmission_datetime'] = deposit_inquiry_req_data[41:51]
        request.data['terminal_id'] = merchant_information[0:10]
        request.data['request_data_len'] = '131'
        if request.data['pos_id'] == '':
            request.data['pos_id'] = pos_id
        obj = self.create(request, *args, **kwargs)
        if ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).count() <= 0: 
            return Response({ 'deposit_balance': '-1', 'message': 'no vsam_id found, please make connection to umoney','request': obj.data, 'result': {}}, status=status.HTTP_404_NOT_FOUND)
        print(deposit_inquiry_req_data.encode("ascii"))
        data = send_socket_receive_data(deposit_inquiry_req_data)
        print(data)
        resp_data = data_to_array_by_type(DBI_response_len_arr, data)
        DBI_resp_data = {
            'comment': request.data['comment'], 
            'message_type_id': resp_data['message_type_id'], 
            'primary_bit_map': resp_data['primary_bit_map'], 
            'processing_code': resp_data['processing_code'],
            'response_code': resp_data['response_code'],
            'transmission_datetime': resp_data['transmission_datetime'],
            'transaction_unique': resp_data['transaction_uniq'],
            'terminal_id': merchant_information[0:10],
            'result_message_len': resp_data['result_message_len'],
            'result_message_data': resp_data['result_message_data'],
            'pos_id': request.data['pos_id'],
            'deposit_balance': resp_data['deposit_balance'],
        }
        serializer = DepositBalanceInquiryRespSerializer(data=DBI_resp_data)
        if serializer.is_valid():
            serializer.save()
        
        return Response({ 'deposit_balance': DBI_resp_data['deposit_balance'], 'message': 'Success', 'request': obj.data, 'result': serializer.data })

class DepositBalanceInquiryReqDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = DepositBalanceInquiryReq.objects.all()
    serializer_class = DepositBalanceInquiryReqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class DepositBalanceInquiryRespList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = DepositBalanceInquiryResp.objects.all()
    serializer_class = DepositBalanceInquiryRespSerializer

    def get(self, request, *args, **kwargs):
        create_transaction_unique()
        return self.list(request, *args, **kwargs)


class TransactionAggregationInquiryReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = TransactionAggregationInquiryReq.objects.all()
    serializer_class = TransactionAggregationInquiryReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        message_type_id = '0260'
        primary_bit_map = '2200000008200010'
        processing_code = '182100'
        transaction_unique = create_transaction_unique()
        aggregation_inquiry_req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 6, '', '', request.data)
        request.data['message_type_id'] = message_type_id
        request.data['primary_bit_map'] = primary_bit_map
        request.data['processing_code'] = processing_code
        request.data['transaction_unique'] = transaction_unique
        request.data['transmission_datetime'] = aggregation_inquiry_req_data[41:51]
        request.data['terminal_id'] = merchant_information[0:10]
        request.data['request_data_len'] = '131'
        if request.data['pos_id'] == '':
            request.data['pos_id'] = pos_id
        if request.data['closing_date'] == '':
            request.data['closing_date'] = (datetime.now(pytz.timezone('Asia/Ulaanbaatar'))).strftime('%Y%m%d')
        obj = self.create(request, *args, **kwargs)
        if ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).count() <= 0: 
            return Response({ 'message': 'no vsam_id found, please make connection to umoney','request': obj.data, 'result': {}}, status=status.HTTP_404_NOT_FOUND)
        print(aggregation_inquiry_req_data.encode("ascii"))
        data = send_socket_receive_data(aggregation_inquiry_req_data)
        resp_data = data_to_array_by_type(TAI_response_len_arr, data)
        TAI_resp_data = {
            'comment': request.data['comment'], 
            'message_type_id': resp_data['message_type_id'], 
            'primary_bit_map': resp_data['primary_bit_map'], 
            'processing_code': resp_data['processing_code'],
            'response_code': resp_data['response_code'],
            'transmission_datetime': resp_data['transmission_datetime'],
            'transaction_unique': resp_data['transaction_uniq'],
            'terminal_id': merchant_information[0:10],
            'result_message_len': resp_data['result_message_len'],
            'result_message_data': resp_data['result_message_data'],
            'pos_id': request.data['pos_id'],
            'topup_count': resp_data['topup_count'],
            'topup_amount': resp_data['topup_amount'],
            'topup_cancellation_count': resp_data['topup_cancellation_count'],
            'topup_cancellation_amount': resp_data['topup_cancellation_amount'],
            'payment_count': resp_data['payment_count'],
            'payment_amount': resp_data['payment_amount'],
            'payment_cancellation_count': resp_data['payment_cancellation_count'],
            'payment_cancellation_amount': resp_data['payment_cancellation_amount'],
        }
        serializer = TransactionAggregationInquiryRespSerializer(data=TAI_resp_data)
        if serializer.is_valid():
            serializer.save()
        
        return Response({ 'message': 'Success', 'request': obj.data, 'result': serializer.data })

class TransactionAggregationInquiryReqDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = TransactionAggregationInquiryReq.objects.all()
    serializer_class = TransactionAggregationInquiryReqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TransactionAggregationInquiryRespList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = TransactionAggregationInquiryResp.objects.all()
    serializer_class = TransactionAggregationInquiryRespSerializer

    def get(self, request, *args, **kwargs):
        create_transaction_unique()
        return self.list(request, *args, **kwargs)

""" **************************** """
""" END OF REQUEST AND RESPONSES """
""" **************************** """

def data_to_array_by_type(response_len_data, data):
    resp_data = {}
    tmp = -1
    print("RESPONSE:\n")
    print(data)
    print("\n\n\n")
    for k,v in response_len_data.items():
        print(k + ": " + (data[tmp:v+1]).decode())
        resp_data[k] = (data[tmp:v+1]).decode()
        tmp = v+1
    return resp_data 

def decrypt_seed128(source_data, encrypted_str, mkey):
    compile_java('decryptSEED128.java')
    res = execute_java('decryptSEED128.java', source_data + encrypted_str + mkey, '')
    return res

def encrypt_seed128(source_data, decrypted_str, working_key):
    compile_java('encryptSEED128.java')
    res = execute_java('encryptSEED128.java', source_data + decrypted_str + working_key, '')
    return res

def encrypt_seed128_hex(source_data, decrypted_str, working_key):
    compile_java('encryptSEED128Hex.java')
    res = execute_java('encryptSEED128Hex.java', source_data + decrypted_str + working_key, '')
    return res

def send_socket_receive_data(req_data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = ('111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
    + '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
    + '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
    + '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
    + '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111').encode("ascii")
    try:
        s.connect(("202.126.92.39", 12021))
        s.send(bytes(req_data, encoding='ascii'))
        data = s.recv(4096)
        s.close()
    except socket.error as exc:
        print("Caught exception socket.error : %s" % exc)
        data = data[:133] + str(exc).encode("ascii") + data[197:]

    return data

def create_transaction_unique():
    current_date = (datetime.now(pytz.timezone('Asia/Ulaanbaatar'))).strftime('%y%m%d')
    result = current_date + '000000'
    result1 = '000000000000'
    result2 = '000000000000'
    result3 = '000000000000'
    result4 = '000000000000'
    if ConnectionReq.objects.all().count() + TopupReq.objects.all().count() + DepositBalanceInquiryReq.objects.all().count() + TransactionAggregationInquiryReq.objects.all().count() > 0:
        if ConnectionReq.objects.all().count() > 0:
            result1 = ConnectionReq.objects.aggregate(Max('transaction_unique'))['transaction_unique__max']
        if TopupReq.objects.all().count() > 0:
            result2 = TopupReq.objects.aggregate(Max('transaction_unique'))['transaction_unique__max']
        if DepositBalanceInquiryReq.objects.all().count() > 0:
            result3 = DepositBalanceInquiryReq.objects.aggregate(Max('transaction_unique'))['transaction_unique__max']
        if TransactionAggregationInquiryReq.objects.all().count() > 0:
            result4 = TransactionAggregationInquiryReq.objects.aggregate(Max('transaction_unique'))['transaction_unique__max']
        tmp = ''
        print(result1)
        print(result2)
        print(result3)
        print(result4)
        if result1 > tmp:
            tmp = result1
        if result2 > tmp: 
            tmp = result2
        if result3 > tmp: 
            tmp = result3
        if result4 > tmp: 
            tmp = result4
        result = tmp[0:6] + str(int(tmp[6:]) +1 ).zfill(6)
    print("********" + result + "********")
    return result

    
def prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, req_type, auth_id='', working_key='', card_data = {}):
    message_request_data = 'ID1234ID1234ID1222                                                                                                              '    
    if req_type == 1:
        message_request_data = 'ID1234ID1234ID1222                                                                                                              '
    elif req_type == 2:
        # print(encrypt_seed128(transaction_unique+merchant_information[6:10], auth_id).decode("ascii")+"\n\n\n")
        message_request_data = 'ID1234ID1234ID1222                                              ' + encrypt_seed128(transaction_unique+merchant_information[6:10], auth_id, working_key).decode("ascii") + "                                "
    elif req_type == 3:
        message_request_data = ''
        message_request_data = message_request_data + card_data['tran_type']
        message_request_data = message_request_data + card_data['card_number']
        message_request_data = message_request_data + card_data['card_algorithm_id']
        message_request_data = message_request_data + card_data['card_keyset_v']
        message_request_data = message_request_data + card_data['card_transaction_seq_number']
        message_request_data = message_request_data + card_data['card_random_number']
        message_request_data = message_request_data + card_data['card_balance']
        message_request_data = message_request_data + card_data['topup_amount']
        message_request_data = message_request_data + card_data['sign1']
        message_request_data = message_request_data + card_data['payment_method']
        message_request_data = message_request_data + '                                                   '
        print(message_request_data + "\n")
    elif req_type == 4:
        return
    elif req_type == 5:
        last_vsam_id = ''
        last_vsam_id_hex = ''
        if ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).count() > 0:
            last_vsam_id = toStr(ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).order_by('-created')[0].vsam_id)
            last_vsam_id_hex = ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).order_by('-created')[0].vsam_id
            working_key = ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).order_by('-created')[0].working_key
        print("----------" + last_vsam_id_hex + "----------")
        print("----------" + encrypt_seed128(transaction_unique+merchant_information[6:10], last_vsam_id, working_key).decode("ascii") + "-----")
        message_request_data = 'ID1234ID1234ID1222                                              ' + encrypt_seed128_hex(transaction_unique+merchant_information[6:10], last_vsam_id_hex, working_key).decode("ascii") + "                                "
    elif req_type == 6:
        last_vsam_id = ''
        if ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).count() > 0:
            last_vsam_id = toStr(ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).order_by('-created')[0].vsam_id)
            working_key = ConnectionResp.objects.all().filter(processing_code=PDA_processing_code).order_by('-created')[0].working_key
        message_request_data = 'ID1234ID1234ID1222                                              ' + encrypt_seed128(transaction_unique+merchant_information[6:10], last_vsam_id, working_key).decode("ascii") + (datetime.now(pytz.timezone('Asia/Ulaanbaatar'))).strftime('%Y%m%d') + "                        "
        print(message_request_data)
    transmission_date = (datetime.now(pytz.timezone('Asia/Ulaanbaatar'))).strftime('%m%d%H%M%S')
    print("\n\n\n\n\n" + transmission_date + "\n\n\n\n\n")
    message_request_data_length = '131'
    
    message_data = ''
    message_data = message_data + message_type_id
    message_data = message_data + primary_bit_map
    message_data = message_data + processing_code
    message_data = message_data + transmission_date
    message_data = message_data + transaction_unique
    message_data = message_data + merchant_information
    message_data = message_data + message_request_data_length
    message_data = message_data + message_request_data
    print(message_data + "\n")
    req_data = ''
    req_data = req_data + toStr(stx_hex)
    req_data = req_data + message_length
    req_data = req_data + destination_info
    req_data = req_data + source_info
    req_data = req_data + version
    req_data = req_data + message_data
    req_data = req_data + toStr(etx_hex)
    print(req_data + "\n")
    return req_data

""" 
java compiler
"""
import os.path,subprocess
from subprocess import STDOUT,PIPE

def compile_java(java_file):
    print(subprocess.check_call(['pwd']))
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, data, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class, data]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin)
    print(stdout)
    return stdout

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


