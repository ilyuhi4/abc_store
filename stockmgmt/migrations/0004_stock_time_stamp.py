# Generated by Django 3.2.7 on 2021-09-09 17:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0003_alter_stock_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
