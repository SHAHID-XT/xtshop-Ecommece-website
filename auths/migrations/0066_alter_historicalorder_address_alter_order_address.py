# Generated by Django 5.0.3 on 2024-04-01 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0065_historicalsupportticket_reply_supportticket_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='address',
            field=models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auths.address'),
        ),
    ]