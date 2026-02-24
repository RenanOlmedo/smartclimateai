import pandas as pd
from prophet import Prophet
import json
import os
from download import get_climate_data

def forecast_column(df, column_name, periods=1):
    train = df[["ds", column_name]].copy()
    train = train.rename(columns={column_name: "y"})
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(train)
    future = model.make_future_dataframe(periods=periods, freq='30min')
    forecast = model.predict(future)
    return forecast["yhat"].iloc[-1]

def update_forecast_file():

    df = get_climate_data()

    df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)
    df = df.rename(columns={"created_at": "ds"})

    last_temp = df["temp_dht"].iloc[-1]
    last_hum = df["humidity"].iloc[-1]
    last_pres = df["pressure"].iloc[-1]

    pred_temp = forecast_column(df, "temp_dht")
    pred_hum = forecast_column(df, "humidity")
    pred_pres = forecast_column(df, "pressure")

    data = {
        "last_temp": float(last_temp),
        "last_hum": float(last_hum),
        "last_pres": float(last_pres),
        "pred_temp": float(pred_temp),
        "pred_hum": float(pred_hum),
        "pred_pres": float(pred_pres)
    }

    with open("forecast_cache.json", "w") as f:
        json.dump(data, f)

    print("Forecast atualizado com sucesso!")