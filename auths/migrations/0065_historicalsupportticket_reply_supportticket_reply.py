# Generated by Django 5.0.3 on 2024-04-01 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0064_historicalsupportattachment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsupportticket',
            name='reply',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='supportticket',
            name='reply',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
