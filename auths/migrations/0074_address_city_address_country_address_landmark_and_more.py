# Generated by Django 5.0.3 on 2024-04-01 10:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0073_remove_address_user_remove_historicaladdress_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(default='India', editable=False, max_length=30),
        ),
        migrations.AddField(
            model_name='address',
            name='landmark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='line1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='line2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='mobile_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='pincode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='city',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='country',
            field=models.CharField(default='India', editable=False, max_length=30),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='landmark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='line1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='line2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='mobile_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='pincode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='state',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='historicaladdress',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='address',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicaladdress',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
