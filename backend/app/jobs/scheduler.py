from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.workflow import run_main_workflow, run_6h_summary

scheduler = BackgroundScheduler(timezone="Asia/Bangkok")

# cron_trigger = CronTrigger(hour='0,6,12,18', minute=0)

scheduler.add_job(
    run_main_workflow,
    trigger='interval',
    minutes=30,
    name="Main Workflow Job"
)

scheduler.add_job(
    run_6h_summary,
    trigger='cron',
    hour='0,6,12,18',
    minute=5
)