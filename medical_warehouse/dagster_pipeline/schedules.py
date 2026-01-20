# dagster_pipeline/schedules.py

from dagster import ScheduleDefinition
from .jobs import telegram_analytics_job

daily_schedule = ScheduleDefinition(
    job=telegram_analytics_job,
    cron_schedule="0 2 * * *"  # daily at 2 AM
)
