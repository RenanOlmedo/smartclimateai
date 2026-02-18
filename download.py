import requests
import pandas as pd

CHANNEL_ID = "2420345"
READ_API_KEY = "MTKXHOTLMKL75UV4"

def get_climate_data(results=200):

    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

    params = {
        "api_key": READ_API_KEY,
        "results": results
    }

    response = requests.get(url, params=params)
    data = response.json()

    feeds = data["feeds"]
    df = pd.DataFrame(feeds)

    df["created_at"] = pd.to_datetime(df["created_at"])

    # MAPA CORRETO DOS CAMPOS
    df["humidity"] = pd.to_numeric(df["field1"], errors="coerce")
    df["temp_dht"] = pd.to_numeric(df["field2"], errors="coerce")
    df["pressure"] = pd.to_numeric(df["field4"], errors="coerce")

    df = df[["created_at", "temp_dht", "humidity", "pressure"]]

    df = df.dropna()

    return df
