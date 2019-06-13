# Generated by Django 2.1.7 on 2019-06-11 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Funcionario', '0051_auto_20190606_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressinfo',
            name='basicinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='address_info', serialize=False, to='Funcionario.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='contractualinfo',
            name='basicinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='contractual_info', serialize=False, to='Funcionario.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='documentattachments',
            name='basicinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='docscans', serialize=False, to='Funcionario.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='documentsinfo',
            name='basicinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='documents_info', serialize=False, to='Funcionario.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='foreignerinfo',
            name='basicinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='foreigner_info', serialize=False, to='Funcionario.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='handicappedinfo',
            name='basicinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='handicapped_info', serialize=False, to='Funcionario.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='handicappedinfo',
            name='deficiencia_obs',
            field=models.TextField(blank=True, null=True),
        ),
    ]
