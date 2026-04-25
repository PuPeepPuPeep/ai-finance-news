from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.workflow import run_main_workflow, run_6h_summary
from datetime import datetime, timedelta

scheduler = BackgroundScheduler(timezone="Asia/Bangkok")

scheduler.add_job(
    run_main_workflow,
    trigger='interval',
    minutes=30,
    name="Main Workflow Job",
    next_run_time=datetime.now() + timedelta(seconds=30)
)

scheduler.add_job(
    run_6h_summary,
    trigger='cron',
    hour='0,6,12,18',
    minute=5,
    name="6h Summary Job",
    next_run_time=datetime.now() + timedelta(minutes=10)
)