# Generated by Django 4.1.5 on 2023-03-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankingApp', '0017_alter_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.BinaryField(default=b''),
        ),
    ]
