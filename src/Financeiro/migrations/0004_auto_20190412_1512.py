# Generated by Django 2.1.7 on 2019-04-12 18:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Financeiro', '0003_entrada_cliente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entrada',
            old_name='classificacao',
            new_name='classificacao_servico',
        ),
        migrations.RenameField(
            model_name='entrada',
            old_name='origem',
            new_name='forma_pagamento',
        ),
        migrations.AddField(
            model_name='entrada',
            name='data_vencimento',
            field=models.DateField(default=datetime.datetime(2019, 4, 12, 18, 12, 16, 265722, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entrada',
            name='observacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='percentual_desconto',
            field=models.DecimalField(decimal_places=2, default=(0.00), max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entrada',
            name='produto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='quantidade_produto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='receita_fixa',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
