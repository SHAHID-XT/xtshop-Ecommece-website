# Generated by Django 5.0.3 on 2024-04-01 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0074_address_city_address_country_address_landmark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='address', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='category',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicaladdress',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalcart',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalprofile',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalrating',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalseller',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalsupportattachment',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='historicalsupportticket',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='passwordresettoken',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='supportattachment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auths.customuser'),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auths.customuser'),
        ),
    ]
