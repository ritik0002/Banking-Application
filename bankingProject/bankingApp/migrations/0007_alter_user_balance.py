# Generated by Django 4.1.5 on 2023-02-27 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankingApp', '0006_user_balance_alter_transaction_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]