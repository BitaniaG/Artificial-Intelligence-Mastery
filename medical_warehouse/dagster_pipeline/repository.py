# dagster_pipeline/repository.py

from dagster import Definitions
from .jobs import telegram_analytics_job
from .schedules import daily_schedule

defs = Definitions(
    jobs=[telegram_analytics_job],
    schedules=[daily_schedule]
)
