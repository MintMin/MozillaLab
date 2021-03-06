# Generated by Django 2.2.12 on 2020-06-16 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('career_fair', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary_Booth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='career_fair',
            name='date',
        ),
        migrations.RemoveField(
            model_name='career_fair',
            name='time',
        ),
        migrations.AddField(
            model_name='career_booth',
            name='booth_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='career_booth',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='career_booth',
            name='join_zoom_url',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='career_booth',
            name='start_zoom_url',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='career_fair',
            name='firstdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='career_fair',
            name='lastdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='career_booth',
            name='interview_duration',
            field=models.IntegerField(choices=[(4, 'Four minutes'), (5, 'Five minutes'), (6, 'Six minutes'), (7, 'Seven minutes'), (8, 'Eight minutes'), (9, 'Nine minutes'), (10, 'Ten minutes')], default=4, help_text='How long do you want every interaction to be? (per student)'),
        ),
        migrations.AlterField(
            model_name='career_booth',
            name='rest_duration',
            field=models.IntegerField(choices=[(1, 'One minutes'), (2, 'Two minutes'), (3, 'Three minutes'), (4, 'Four minutes')], default=2, help_text='How long do you need to rest between interactions?'),
        ),
        migrations.CreateModel(
            name='KeyVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=240)),
                ('container', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='career_fair.Dictionary_Booth')),
                ('value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dictionary_booth',
            name='career_booth',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='career_fair.Career_Booth'),
        ),
    ]
