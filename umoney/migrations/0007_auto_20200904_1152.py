# Generated by Django 3.1 on 2020-09-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umoney', '0006_auto_20200904_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='topupreq',
            name='message_type_id',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='payment_method',
            field=models.CharField(blank=True, default='', max_length=1),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='primary_bit_map',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='processing_code',
            field=models.CharField(blank=True, default='', max_length=6),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='request_data_len',
            field=models.CharField(blank=True, default='', max_length=3),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='terminal_id',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='tran_type',
            field=models.CharField(blank=True, default='', max_length=2),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='transaction_unique',
            field=models.CharField(blank=True, default='', max_length=12),
        ),
        migrations.AddField(
            model_name='topupreq',
            name='transmission_datetime',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
