🔗 Aplicação Online:
https://smartclimate-online.onrender.com


# 🌍 SmartClimateAI — Online Edition

Sistema de Inteligência Atmosférica com IA rodando 100% online.

O SmartClimateAI transforma dados reais coletados por sensores físicos em análises meteorológicas avançadas, previsões com Machine Learning e um índice proprietário de instabilidade atmosférica.

🔗 Acesse online:
https://smartclimate-online.onrender.com

---

## 🚀 Arquitetura do Projeto

ESP8266 + Sensores  
⬇  
ThingSpeak (Cloud IoT)  
⬇  
Servidor Flask (Render)  
⬇  
Modelos de IA (Prophet + Índice Atmosférico Próprio)  
⬇  
Dashboards Interativos (Plotly)

---

## 📡 Coleta de Dados

Os dados são enviados por uma estação IoT baseada em:

- ESP8266
- Sensor de temperatura (DHT)
- Sensor de pressão atmosférica
- Sensor de umidade

Os dados são armazenados no ThingSpeak e consumidos via API REST.

---

## 🧠 Inteligência Artificial

O sistema utiliza:

- Prophet (Meta) para previsão de:
  - Temperatura
  - Umidade
  - Pressão

Além disso, implementa um modelo próprio:

### 📊 IAI — Índice Atmosférico de Instabilidade

O índice combina:

- Condensação atmosférica
- Variação de pressão
- Umidade relativa
- Ponto de orvalho

Classificações:

| IAI | Estado |
|-----|--------|
| 0–20 | Atmosfera Estável ☀️ |
| 20–40 | Atenção |
| 40–60 | Instável |
| 60–80 | Tempestade ⛈️ |
| 80–100 | Tempestade Severa 🌩️ |

---

## 🖥️ Painéis Disponíveis

### 📊 Painel Digital
- Dados reais em gauges
- Previsões com deltas
- Tendência de subida/queda
- Estimativa de chance de chuva

### 🔬 Painel Científico
- Gauge do IAI
- Ponto de orvalho
- Tendência de pressão
- Classificação atmosférica em tempo real

---

## 🔐 Segurança

A aplicação está protegida por autenticação via senha utilizando variáveis de ambiente:

APP_USER  
APP_PASS  

---

## ☁️ Deploy

Hospedado gratuitamente na Render (Free Tier).

Tecnologias usadas:

- Python
- Flask
- Prophet
- Plotly
- Pandas
- Gunicorn

---

## 📂 Estrutura

smart_climate_ia_online/
│
├── app.py
├── download.py
├── dashboard_online.py
├── cientifica_online.py
├── requirements.txt
├── Procfile
└── README.md


---

## 🎯 Objetivo do Projeto

Demonstrar integração completa entre:

- IoT
- Cloud
- Machine Learning
- Backend Web
- Visualização de Dados
- Deploy em Produção

---

## 👨‍💻 Autor

Renan Ferreira  
Projeto pessoal de pesquisa e desenvolvimento em Inteligência Atmosférica.

---

## 🌎 Próximos Passos

- Histórico temporal do IAI
- Integração com sensor de qualidade do ar (MQ-135)
- Sistema de alertas automáticos
- Versão mobile PWA
