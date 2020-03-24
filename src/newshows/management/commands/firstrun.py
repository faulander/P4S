import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from newshows.models import Setting
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from loguru import logger

class Command(BaseCommand):
    help = 'Setup of cronjobs for P4S'
    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.MINUTES)
        task, created = PeriodicTask.objects.get_or_create(
            name='Check for Active Sonarr',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.checkForActiveSonarr",
            }
        )
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the list of TV Shows from TV Maze',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.HelperUpdateTVMaze",
            }
        )

        schedule, created = IntervalSchedule.objects.get_or_create(every=5,period=IntervalSchedule.MINUTES)
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the latest Sonarr Downloads',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.getSonarrDownloads",
            }
        )
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the latest Sonarr Profiles',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.helperGetSonarrProfiles",
            }
        )
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the latest Sonarr Downloads',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.HelperUpdateSonarr",
            }
        )

        schedule, created = IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.DAYS)
        task, created = PeriodicTask.objects.get_or_create(
            name='Update local TV Maze Database',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.HelperUpdateShows",
            }
        )
 