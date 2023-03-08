# Generated by Django 4.1.5 on 2023-02-06 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bankingApp', '0003_rename_condition_transactions_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='account',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bankingApp.account'),
        ),
    ]
