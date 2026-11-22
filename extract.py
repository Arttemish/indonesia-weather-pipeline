import os
import requests
import pandas as pd

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": -6.2,
    "longitude": 106.85,  # Jakarta
    "hourly": "temperature_2m,precipitation,relative_humidity_2m",
    "past_days": 1,
    "forecast_days": 1,
    "timezone": "Asia/Jakarta",
}

response = requests.get(URL, params=PARAMS, timeout=30)
response.raise_for_status()

df = pd.DataFrame(response.json()["hourly"])

os.makedirs("data", exist_ok=True)
df.to_parquet("data/jakarta_weather.parquet", index=False)

print(df.head(10))
print(f"\nTotal baris: {len(df)}")