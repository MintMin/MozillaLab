# Generated by Django 2.2.12 on 2020-06-05 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='company',
        ),
        migrations.RemoveField(
            model_name='event',
            name='recruiter',
        ),
        migrations.RemoveField(
            model_name='event',
            name='typE',
        ),
        migrations.AddField(
            model_name='event',
            name='Event_type',
            field=models.CharField(choices=[('i', 'Infosession'), ('b', 'Interview Only')], default='i', help_text='Select a type for the event', max_length=1),
        ),
        migrations.AddField(
            model_name='event',
            name='absolute_url',
            field=models.CharField(blank=True, editable=False, max_length=400),
        ),
        migrations.AddField(
            model_name='event',
            name='main_recruiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='rsvp_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='rsvp_list',
            field=models.ManyToManyField(related_name='rsvp_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='space_open',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Recruiter',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
