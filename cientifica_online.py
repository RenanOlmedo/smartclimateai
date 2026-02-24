import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_cientifica(df):

    T = df["temp_dht"].astype(float)
    RH = df["humidity"].astype(float)
    P = df["pressure"].astype(float)

    temp = T.iloc[-1]
    hum = RH.iloc[-1]
    pres = P.iloc[-1]

    dew = temp - (100 - hum) / 5

    if len(P) > 6:
        delta_p = pres - P.iloc[-6]
    else:
        delta_p = 0

    CI = (temp - dew) * (hum / 100)
    PI = min(100, abs(delta_p) / 3 * 100)

    IAI = (
        0.35 * CI +
        0.35 * PI +
        0.2 * hum +
        0.1 * (100 - (temp - dew) * 5)
    )

    IAI = max(0, min(100, IAI))

    if IAI < 20:
        status = "Atmosfera Estável ☀️"
    elif IAI < 40:
        status = "Atenção"
    elif IAI < 60:
        status = "Instável"
    elif IAI < 80:
        status = "Tempestade ⛈️"
    else:
        status = "Tempestade Severa 🌩️"

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "indicator"}, {"type": "domain"}]],
        column_widths=[0.5, 0.5]
    )

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=IAI,
        title={'text': "Índice de Instabilidade", 'font': {'size': 40}},
        gauge={
            'axis': {'range':[0,100]},
            'steps': [
                {'range':[0,20], 'color':'#2ecc71'},
                {'range':[20,40], 'color':'#f1c40f'},
                {'range':[40,60], 'color':'#e67e22'},
                {'range':[60,80], 'color':'#e74c3c'},
                {'range':[80,100], 'color':'#8e44ad'}
            ],
            'bar': {'color':'darkred'}
        }
    ), row=1, col=1)

    info = (
        f"<b>Temperatura:</b> {temp:.2f} °C<br><br>"
        f"<b>Umidade:</b> {hum:.1f} %<br><br>"
        f"<b>Pressão:</b> {pres:.2f} hPa<br><br>"
        f"<b>Ponto de Orvalho:</b> {dew:.2f} °C<br><br>"
        f"<b>Tendência Pressão:</b> {delta_p:.2f} hPa / 30 min<br><br>"
        f"<b>Estado:</b> {status}"
    )

    fig.add_annotation(
        x=0.95, y=0.5,
        text=info,
        showarrow=False,
        align='left',
        font={'size':30}
    )

    fig.update_layout(
        title="",
        paper_bgcolor="white",
        font={'family':'Arial'},
        margin={'t':80}
    )

    return fig.to_html(full_html=False)
