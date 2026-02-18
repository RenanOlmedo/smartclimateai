from flask import Flask, Response, request
from functools import wraps
import os

from download import get_climate_data
from dashboard_online import generate_dashboard
from cientifica_online import generate_cientifica

app = Flask(__name__)

# ======= AUTENTICAÇÃO =======

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

# ======= ROTAS =======

@app.route("/")
@requires_auth
def home():
    return """
    <h1>SmartClimateAI</h1>
    <a href="/dashboard"><button>📊 Painel Digital</button></a>
    <a href="/cientifica"><button>🔬 Painel Científico</button></a>
    """

@app.route("/dashboard")
@requires_auth
def dashboard():
    df = get_climate_data()
    return generate_dashboard(df)

@app.route("/cientifica")
@requires_auth
def cientifica():
    df = get_climate_data()
    return generate_cientifica(df)

if __name__ == "__main__":
    app.run(debug=True)

