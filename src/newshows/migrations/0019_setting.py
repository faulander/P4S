# Generated by Django 3.0.1 on 2020-01-07 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newshows', '0018_profile_profile_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField()),
                ('sonarr_url', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('sonarr_apikey', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('sonarr_autoadd', models.BooleanField(default=False)),
                ('sonarr_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='newshows.Profile')),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
        ),
    ]