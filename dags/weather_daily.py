from datetime import timedelta

import pendulum
from airflow.sdk import dag, task


@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    catchup=False,
    tags=["weather"],
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
)
def weather_daily():
    @task
    def extract_weather(**context):
        from weather.extract import extract

        logical_date = context.get("logical_date") or pendulum.now("UTC")
        target_date = logical_date.in_timezone("Asia/Jakarta").date() - timedelta(days=1)
        extract(target_date, base_dir="/opt/airflow/data/raw/weather")

    extract_weather()


weather_daily()
