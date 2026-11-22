import os
from datetime import date, timedelta

import pandas as pd
import requests

URL = "https://api.open-meteo.com/v1/forecast"

CITIES = [
    {"city": "Jakarta", "latitude": -6.21, "longitude": 106.85},
    {"city": "Surabaya", "latitude": -7.25, "longitude": 112.75},
    {"city": "Bandung", "latitude": -6.92, "longitude": 107.61},
    {"city": "Medan", "latitude": 3.59, "longitude": 98.67},
    {"city": "Semarang", "latitude": -6.97, "longitude": 110.42},
    {"city": "Palembang", "latitude": -2.98, "longitude": 104.76},
    {"city": "Makassar", "latitude": -5.15, "longitude": 119.43},
    {"city": "Denpasar", "latitude": -8.65, "longitude": 115.22},
    {"city": "Balikpapan", "latitude": -1.27, "longitude": 116.83},
    {"city": "Jayapura", "latitude": -2.53, "longitude": 140.72},
]


def fetch_city(city: dict, target_date: date) -> pd.DataFrame:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": "temperature_2m,precipitation,relative_humidity_2m",
        "start_date": target_date.isoformat(),
        "end_date": target_date.isoformat(),
        "timezone": "Asia/Jakarta",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    df = pd.DataFrame(response.json()["hourly"])
    df["city"] = city["city"]
    return df


def extract(target_date: date, base_dir: str = "data/raw/weather") -> str:
    frames = [fetch_city(city, target_date) for city in CITIES]
    df = pd.concat(frames, ignore_index=True)

    out_dir = f"{base_dir}/date={target_date.isoformat()}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/weather.parquet"
    df.to_parquet(out_path, index=False)

    print(f"{len(df)} baris tersimpan di {out_path}")
    return out_path


if __name__ == "__main__":
    extract(date.today() - timedelta(days=1))
