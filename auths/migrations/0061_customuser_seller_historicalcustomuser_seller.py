# Generated by Django 5.0.3 on 2024-03-31 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0060_alter_historicalsupportticket_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcustomuser',
            name='seller',
            field=models.BooleanField(default=False),
        ),
    ]