# Generated by Django 3.2 on 2021-10-11 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentgateway', '0002_transactiondetails_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiondetails',
            name='trans',
            field=models.IntegerField(default=1),
        ),
    ]
