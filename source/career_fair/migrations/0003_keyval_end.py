# Generated by Django 2.2.12 on 2020-06-16 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career_fair', '0002_auto_20200616_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyval',
            name='end',
            field=models.CharField(blank=True, max_length=240),
        ),
    ]
