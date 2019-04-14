# Generated by Django 2.1.7 on 2019-04-10 17:31

import Funcionario.utilities
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Funcionario', '0024_auto_20190409_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='numero_documento_CPF',
            field=models.CharField(error_messages={'unique': 'CPF Já Registrado'}, max_length=14, validators=[Funcionario.utilities.validateCPF]),
        ),
    ]
