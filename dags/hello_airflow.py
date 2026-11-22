from datetime import datetime
from airflow.sdk import dag, task


@dag(
    schedule="@daily",
    start_date=datetime(2026, 11, 1),
    catchup=False,
    tags=["latihan"],
)
def hello_airflow():
    @task
    def say_hello():
        print("Halo dari Airflow!")

    say_hello()


hello_airflow()
