# Generated by Django 4.1.7 on 2024-03-02 20:13

import auths.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0017_alter_product_folder_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='folder_name',
            field=models.CharField(blank=True, default=auths.utils.generate_unique_id, max_length=10, null=True),
        ),
    ]
