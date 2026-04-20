from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.workflow import run_workflow

scheduler = BackgroundScheduler(timezone="Asia/Bangkok")

cron_trigger = CronTrigger(hour='0,6,12,18', minute=0)

scheduler.add_job(
    run_workflow,
    trigger=cron_trigger,
    name="6-hour-summary-job"
)