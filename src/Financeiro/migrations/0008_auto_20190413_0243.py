# Generated by Django 2.1.7 on 2019-04-13 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Financeiro', '0007_auto_20190413_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='forma_pagamento',
            field=models.CharField(choices=[('Débito', 'Débito'), ('Crédito', 'Crédito'), ('Boleto', 'Boleto'), ('Dinheiro', 'Dinheiro')], max_length=100),
        ),
    ]
