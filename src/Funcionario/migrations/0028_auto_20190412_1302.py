# Generated by Django 2.1.7 on 2019-04-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Funcionario', '0027_auto_20190410_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='data_ultima_ativacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
