# Generated by Django 5.0.3 on 2024-04-01 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0069_alter_historicalorder_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalorder',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
    ]
