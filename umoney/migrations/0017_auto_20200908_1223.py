# Generated by Django 3.1 on 2020-09-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umoney', '0016_auto_20200908_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='topupcheckreq',
            name='sign2',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_algorithm_id',
            field=models.CharField(blank=True, default='', max_length=2),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_keyset_v',
            field=models.CharField(blank=True, default='', max_length=2),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_number',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_post_balance',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_pre_balance',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_random_number',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='card_transaction_seq_number',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='sign2',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='topup_amount',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='topupcheckresp',
            name='tran_type',
            field=models.CharField(blank=True, default='', max_length=2),
        ),
    ]
