# dagster_pipeline/ops.py

from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(
        ["python", "src/scraper.py"],
        check=True
    )

@op
def load_raw_to_postgres():
    subprocess.run(
        ["python", "src/load_to_postgres.py"],
        check=True
    )

@op
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run", "--profiles-dir", "medical_warehouse"],
        check=True
    )
    subprocess.run(
        ["dbt", "test", "--profiles-dir", "medical_warehouse"],
        check=True
    )

@op
def run_yolo_enrichment():
    subprocess.run(
        ["python", "src/vision/yolo_inference.py"],
        check=True
    )
