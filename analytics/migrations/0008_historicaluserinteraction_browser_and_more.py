# Generated by Django 4.1.7 on 2024-03-29 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_historicaluserloginlog_historicaluserinteraction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluserinteraction',
            name='browser',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userinteraction',
            name='browser',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]