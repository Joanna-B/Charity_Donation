# Generated by Django 3.1.1 on 2020-10-08 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0007_auto_20201008_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
