# Generated by Django 3.1 on 2020-09-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umoney', '0013_auto_20200906_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionAggregationInquiryReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, default='', max_length=100)),
                ('message_type_id', models.CharField(blank=True, default='', max_length=4)),
                ('primary_bit_map', models.CharField(blank=True, default='', max_length=16)),
                ('processing_code', models.CharField(blank=True, default='', max_length=6)),
                ('transmission_datetime', models.CharField(blank=True, default='', max_length=10)),
                ('transaction_unique', models.CharField(blank=True, default='', max_length=12)),
                ('terminal_id', models.CharField(blank=True, default='', max_length=40)),
                ('request_data_len', models.CharField(blank=True, default='', max_length=3)),
                ('pos_id', models.CharField(blank=True, default='ID1234ID1234ID1222', max_length=64)),
                ('encrypted_vsam_id', models.CharField(blank=True, default='00000000', max_length=32)),
                ('closing_gate', models.CharField(blank=True, default='', max_length=8)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='TransactionAggregationInquiryResp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, default='', max_length=100)),
                ('message_type_id', models.CharField(blank=True, default='', max_length=4)),
                ('primary_bit_map', models.CharField(blank=True, default='', max_length=16)),
                ('response_code', models.CharField(blank=True, default='', max_length=2)),
                ('result_message_len', models.CharField(blank=True, default='', max_length=3)),
                ('result_message_data', models.CharField(blank=True, default='', max_length=64)),
                ('processing_code', models.CharField(blank=True, default='', max_length=6)),
                ('transmission_datetime', models.CharField(blank=True, default='', max_length=10)),
                ('transaction_unique', models.CharField(blank=True, default='', max_length=12)),
                ('terminal_id', models.CharField(blank=True, default='', max_length=40)),
                ('pos_id', models.CharField(blank=True, default='ID1234ID1234ID1222', max_length=64)),
                ('topup_count', models.CharField(blank=True, default='', max_length=5)),
                ('topup_amount', models.CharField(blank=True, default='', max_length=10)),
                ('topup_cancellation_count', models.CharField(blank=True, default='', max_length=5)),
                ('topup_cancellation_amount', models.CharField(blank=True, default='', max_length=10)),
                ('payment_count', models.CharField(blank=True, default='', max_length=5)),
                ('payment_amount', models.CharField(blank=True, default='', max_length=10)),
                ('payment_cancellation_count', models.CharField(blank=True, default='', max_length=5)),
                ('payment_cancellation_amount', models.CharField(blank=True, default='', max_length=10)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AlterField(
            model_name='depositbalanceinquiryreq',
            name='pos_id',
            field=models.CharField(blank=True, default='ID1234ID1234ID1222', max_length=64),
        ),
        migrations.AlterField(
            model_name='depositbalanceinquiryresp',
            name='pos_id',
            field=models.CharField(blank=True, default='ID1234ID1234ID1222', max_length=64),
        ),
    ]
