from flask import Flask, Response, request
from functools import wraps
import os

from download import get_climate_data
from dashboard_online import generate_dashboard
from cientifica_online import generate_cientifica
from forecast_engine import update_forecast_file
from flask import render_template

app = Flask(__name__)

# ================= AUTH =================

def check_auth(username, password):
    return username == os.environ.get("APP_USER") and password == os.environ.get("APP_PASS")

def authenticate():
    return Response(
        "Acesso restrito.\nLogin necessário.",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ================= ROTAS =================

@app.route("/")
@requires_auth
def home():
    return render_template("home.html")


@app.route("/dashboard")
@requires_auth
def dashboard():
    df = get_climate_data()
    graph = generate_dashboard(df)
    return render_template("dashboard.html", graph=graph)


@app.route("/cientifica")
@requires_auth
def cientifica():
    df = get_climate_data()
    graph = generate_cientifica(df)
    return render_template("cientifica.html",graph=graph)
    


@app.route("/update_forecast")
@requires_auth
def update_forecast():
    update_forecast_file()
    return "<h2>Previsão atualizada com sucesso!</h2><a href='/'>Voltar</a>"

