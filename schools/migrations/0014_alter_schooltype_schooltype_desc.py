# Generated by Django 3.2.9 on 2021-12-12 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0013_auto_20211211_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schooltype',
            name='schooltype_desc',
            field=models.TextField(blank=True, default='Enter Text', max_length=200, null=True),
        ),
    ]