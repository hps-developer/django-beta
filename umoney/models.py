from django.db import models

# Create your models here.
class UmoneyReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    card_number = models.CharField(max_length=16, blank=True, default='')
    card_algorithm_id = models.CharField(max_length=2, blank=True, default='')
    card_keyset_v = models.CharField(max_length=2, blank=True, default='')
    card_transaction_seq_number = models.CharField(max_length=10, blank=True, default='')
    card_random_number = models.CharField(max_length=16, blank=True, default='')
    card_balance = models.CharField(max_length=10, blank=True, default='')
    topup_amount = models.CharField(max_length=10, blank=True, default='')
    sign1 = models.CharField(max_length=8, blank=True, default='')
    comment = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created']