# Generated by Django 2.2.12 on 2020-06-11 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200605_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='join_zoom_url',
            field=models.CharField(default='aoom link', max_length=1000),
        ),
        migrations.AddField(
            model_name='event',
            name='start_zoom_url',
            field=models.CharField(default='boom link', max_length=1000),
        ),
    ]