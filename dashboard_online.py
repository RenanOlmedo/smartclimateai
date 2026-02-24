import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def generate_dashboard(df):

    # Se ainda não existir cache
    if not os.path.exists("forecast_cache.json"):
        return """
        <h2>Ainda não existe previsão.</h2>
        <a href="/update_forecast"><button>🧠 Gerar Primeira Previsão</button></a>
        """

    with open("forecast_cache.json", "r") as f:
        data = json.load(f)

    last_temp = data["last_temp"]
    last_hum = data["last_hum"]
    last_pres = data["last_pres"]

    pred_temp = data["pred_temp"]
    pred_hum = data["pred_hum"]
    pred_pres = data["pred_pres"]

    delta_temp = pred_temp - last_temp
    delta_hum = pred_hum - last_hum
    delta_pres = pred_pres - last_pres

    arrow_temp = "↑" if delta_temp > 0 else "↓"
    arrow_hum = "↑" if delta_hum > 0 else "↓"
    arrow_pres = "↑" if delta_pres > 0 else "↓"

    chance_chuva = min(max((last_hum/100) * (abs(delta_pres)/10) * 100, 0), 100)
    chance_chuva = round(chance_chuva, 1)

    fig = make_subplots(
        rows=2, cols=4,
        specs=[[{'type':'indicator'}]*4,
               [{'type':'indicator'}]*4],
    )

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=last_temp,
        title={'text': "Temp Real (°C)"},
        gauge={'axis': {'range':[0,50]}}
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=last_hum,
        title={'text': "Umidade Real (%)"},
        gauge={'axis': {'range':[0,100]}}
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=last_pres,
        title={'text': "Pressão Real (hPa)"},
        gauge={'axis': {'range':[900,1050]}}
    ), row=1, col=3)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=chance_chuva,
        title={'text': "Chance Chuva (%)"},
        gauge={'axis': {'range':[0,100]}}
    ), row=1, col=4)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pred_temp,
        delta={'reference': last_temp},
        title={'text': f"Temp Prev {arrow_temp}"}
    ), row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pred_hum,
        delta={'reference': last_hum},
        title={'text': f"Umid Prev {arrow_hum}"}
    ), row=2, col=2)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pred_pres,
        delta={'reference': last_pres},
        title={'text': f"Pressão Prev {arrow_pres}"}
    ), row=2, col=3)

    fig.update_layout(
        paper_bgcolor="white",
        title={'text': "SmartClimateAI - Painel Digital",
               'x':0.5}
    )

    return fig.to_html(full_html=True)