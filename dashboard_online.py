import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def generate_dashboard(df):

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

    # 3 COLUNAS CENTRALIZADAS
    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{'type':'indicator'}]*3,
               [{'type':'indicator'}]*3],
        vertical_spacing=0.25,
    )

    # ======================
    # MEDIDORES REAIS (MAIORES)
    # ======================

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=last_temp,
        title={'text': "🌡 Temp Real (°C)", 'font': {'size': 32}},
        gauge={'axis': {'range':[0,50]}},
        number={'font': {'size': 50}}
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=last_hum,
        title={'text': "💧 Umidade Real (%)", 'font': {'size': 32}},
        gauge={'axis': {'range':[0,100]}},
        number={'font': {'size': 50}}
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=last_pres,
        title={'text': "🧭 Pressão Real (hPa)", 'font': {'size': 32}},
        gauge={'axis': {'range':[900,1050]}},
        number={'font': {'size': 50}}
    ), row=1, col=3)

    # ======================
    # PREVISÕES
    # ======================

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pred_temp,
        delta={'reference': last_temp},
        title={'text': f"Temp Prev {arrow_temp}", 'font': {'size': 40}},
        number={'font': {'size': 50}}
    ), row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pred_hum,
        delta={'reference': last_hum},
        title={'text': f"Umid Prev {arrow_hum}", 'font': {'size': 40}},
        number={'font': {'size': 50}}
    ), row=2, col=2)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pred_pres,
        delta={'reference': last_pres},
        title={'text': f"Pressão Prev {arrow_pres}", 'font': {'size': 40}},
        number={'font': {'size': 50}}
    ), row=2, col=3)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            'text': "",
            'x': 0.5,
            'font': {'size': 28}
        },
        height=700,
        margin=dict(t=80)
    )

    return fig.to_html(full_html=False)