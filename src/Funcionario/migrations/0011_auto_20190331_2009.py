# Generated by Django 2.1.7 on 2019-03-31 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Funcionario', '0010_auto_20190331_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interninfo',
            name='estag_instituto_CEP',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
