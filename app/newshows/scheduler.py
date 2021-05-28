from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution, DjangoJob
import pendulum

from .tasks import (
    helperGetSonarrProfiles,
    HelperUpdateShows,
    HelperUpdateSonarr,
    HelperUpdateTVMaze,
    checkForActiveSonarr,
    getSonarrDownloads,
)


def start():
    run1 = pendulum.now()
    run1 = run1.add(minutes=30)
    run1 = run1.to_datetime_string()
    run2 = pendulum.now()
    run2 = run2.add(minutes=60)
    run2 = run2.to_datetime_string()
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.remove_all_jobs()

    scheduler.add_job(
        helperGetSonarrProfiles,
        "interval",
        minutes=5,
        name="getSonarrProfiles",
        jobstore="default",
        id="getSonarrProfiles",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        HelperUpdateSonarr,
        "interval",
        minutes=5,
        name="updateSonarr",
        jobstore="default",
        id="updateSonarr",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        checkForActiveSonarr,
        "interval",
        minutes=1,
        name="checkForActiveSonarr",
        jobstore="default",
        id="checkForActiveSonarr",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        getSonarrDownloads,
        "interval",
        minutes=3,
        name="getSonarrDownloads",
        jobstore="default",
        id="getSonarrDownloads",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        HelperUpdateTVMaze,
        "interval",
        hours=8,
        name="updateTVMaze",
        jobstore="default",
        id="updateTVMaze",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        HelperUpdateShows,
        "interval",
        hours=24,
        name="updateShows",
        jobstore="default",
        id="updateShows",
        replace_existing=True,
        max_instances=1,
    )
    # Run once on application startup with delay
    scheduler.add_job(
        HelperUpdateTVMaze,
        "date",
        run_date=run1,
        name="updateTVMazeOnceAtStartup",
        jobstore="default",
        id="updateTVMazeOnceAtStartup",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        HelperUpdateShows,
        "date",
        run_date=run2,
        name="updateShowsOnceAtStartup",
        jobstore="default",
        id="updateShowsOnceAtStartup",
        replace_existing=True,
        max_instances=1,
    )
    # register_events(scheduler)
    scheduler.start()
