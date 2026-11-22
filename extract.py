import os
import requests
import pandas as pd

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


def fetch_city(city: dict) -> pd.DataFrame:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": "temperature_2m,precipitation,relative_humidity_2m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Asia/Jakarta",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    df = pd.DataFrame(response.json()["hourly"])
    df["city"] = city["city"]
    return df


def main():
    frames = []
    for city in CITIES:
        print(f"Mengambil data {city['city']}...")
        frames.append(fetch_city(city))

    df = pd.concat(frames, ignore_index=True)

    os.makedirs("data", exist_ok=True)
    df.to_parquet("data/weather.parquet", index=False)

    print(df.head())
    print(f"\nTotal baris: {len(df)}")
    print(df["city"].value_counts())


if __name__ == "__main__":
    main()