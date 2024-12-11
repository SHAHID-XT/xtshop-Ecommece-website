# Generated by Django 5.0.3 on 2024-04-01 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0068_alter_historicalorder_order_promotion_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='address',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.address'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='order_promotion_discount',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='auths.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_promotion_discount',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]