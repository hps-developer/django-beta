from django.db import models

# Create your models here.

class ConnectionReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    merchant_info_terminal_id = models.CharField(max_length=10, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='')
    terminal_id = models.CharField(max_length=64, blank=True, default='')
    authentication_id = models.CharField(max_length=64, blank=True, default='')
    vsam_id = models.CharField(max_length=64, blank=True, default='')

class ConnectionResp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    response_code = models.CharField(max_length=2, blank=True, default='')
    merchant_id = models.CharField(max_length=15, blank=True, default='')
    merchant_info_terminal_id = models.CharField(max_length=10, blank=True, default='')
    result_message_len = models.CharField(max_length=3, blank=True, default='')
    result_message_data = models.CharField(max_length=64, blank=True, default='')
    response_data_len = models.CharField(max_length=3, blank=True, default='')
    working_key = models.CharField(max_length=32, blank=True, default='')
    minimum_topup_amount = models.CharField(max_length=10, blank=True, default='')
    system_datetime = models.CharField(max_length=14, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='')
    terminal_id = models.CharField(max_length=64, blank=True, default='')
    authentication_id = models.CharField(max_length=64, blank=True, default='')
    vsam_id = models.CharField(max_length=64, blank=True, default='')

class TopupReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, default='')
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    terminal_id = models.CharField(max_length=40, blank=True, default='')
    request_data_len = models.CharField(max_length=3, blank=True, default='')
    tran_type = models.CharField(max_length=2, blank=True, default='')
    card_number = models.CharField(max_length=16, blank=True, default='')
    card_algorithm_id = models.CharField(max_length=2, blank=True, default='')
    card_keyset_v = models.CharField(max_length=2, blank=True, default='')
    card_transaction_seq_number = models.CharField(max_length=10, blank=True, default='')
    card_random_number = models.CharField(max_length=16, blank=True, default='')
    card_balance = models.CharField(max_length=10, blank=True, default='')
    topup_amount = models.CharField(max_length=10, blank=True, default='')
    sign1 = models.CharField(max_length=8, blank=True, default='')
    payment_method = models.CharField(max_length=1, blank=True, default='')

    class Meta:
        ordering = ['created']

class TopupResp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, default='')
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    response_code = models.CharField(max_length=2, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    terminal_id = models.CharField(max_length=40, blank=True, default='')
    result_message_len = models.CharField(max_length=3, blank=True, default='')
    result_message_data = models.CharField(max_length=64, blank=True, default='')
    tran_type = models.CharField(max_length=2, blank=True, default='')
    card_number = models.CharField(max_length=16, blank=True, default='')
    vsam_tran_seq_num = models.CharField(max_length=10, blank=True, default='')
    card_balance = models.CharField(max_length=10, blank=True, default='')
    topup_amount = models.CharField(max_length=10, blank=True, default='')
    sign2 = models.CharField(max_length=8, blank=True, default='')
    deposit_balance = models.CharField(max_length=10, blank=True, default='')
    payment_method = models.CharField(max_length=1, blank=True, default='')
    sign1 = models.CharField(max_length=8, blank=True, default='')

    class Meta:
        ordering = ['created']

class DepositBalanceInquiryReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, default='')
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    terminal_id = models.CharField(max_length=40, blank=True, default='')
    request_data_len = models.CharField(max_length=3, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='ID1234ID1234ID1222')
    encrypted_vsam_id = models.CharField(max_length=32, blank=True, default='')

    class Meta:
        ordering = ['created']

class DepositBalanceInquiryResp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, default='')
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    response_code = models.CharField(max_length=2, blank=True, default='')
    result_message_len = models.CharField(max_length=3, blank=True, default='')
    result_message_data = models.CharField(max_length=64, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    terminal_id = models.CharField(max_length=40, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='ID1234ID1234ID1222')
    deposit_balance = models.CharField(max_length=32, blank=True, default='')

    class Meta:
        ordering = ['created']


class TransactionAggregationInquiryReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, default='')
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    terminal_id = models.CharField(max_length=40, blank=True, default='')
    request_data_len = models.CharField(max_length=3, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='ID1234ID1234ID1222')
    encrypted_vsam_id = models.CharField(max_length=32, blank=True, default='00000000')
    closing_gate = models.CharField(max_length=8, blank=True, default='')

    class Meta:
        ordering = ['created']

class TransactionAggregationInquiryResp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, default='')
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    response_code = models.CharField(max_length=2, blank=True, default='')
    result_message_len = models.CharField(max_length=3, blank=True, default='')
    result_message_data = models.CharField(max_length=64, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    terminal_id = models.CharField(max_length=40, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='ID1234ID1234ID1222')
    topup_count = models.CharField(max_length=5, blank=True, default='')
    topup_amount = models.CharField(max_length=10, blank=True, default='')
    topup_cancellation_count = models.CharField(max_length=5, blank=True, default='')
    topup_cancellation_amount = models.CharField(max_length=10, blank=True, default='')
    payment_count = models.CharField(max_length=5, blank=True, default='')
    payment_amount = models.CharField(max_length=10, blank=True, default='')
    payment_cancellation_count = models.CharField(max_length=5, blank=True, default='')
    payment_cancellation_amount = models.CharField(max_length=10, blank=True, default='')

    class Meta:
        ordering = ['created']