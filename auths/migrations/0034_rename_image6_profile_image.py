# Generated by Django 4.1.7 on 2024-03-22 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0033_profile_image6'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image6',
            new_name='image',
        ),
    ]
