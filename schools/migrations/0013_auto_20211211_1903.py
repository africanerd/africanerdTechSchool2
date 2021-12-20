# Generated by Django 3.2.9 on 2021-12-12 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0012_school_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='school',
            options={'ordering': ['-school_pub_date']},
        ),
        migrations.AddField(
            model_name='schooltype',
            name='schooltype_color',
            field=models.CharField(blank=True, default='Enter Text', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='schooltype',
            name='schooltype_desc',
            field=models.CharField(blank=True, default='Enter Text', max_length=200, null=True),
        ),
    ]
