import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisi Redditività Affitto", layout="wide")

st.title("📊 Dashboard Affitto Breve - Redditività Immobiliare")

# 📈 Entrate previste
st.header("📈 Entrate previste")
col1, col2, col3 = st.columns(3)
with col1:
    prezzo_notte = st.number_input("Prezzo medio per notte (€)", min_value=0.0, value=90.0)
with col2:
    occupazione = st.slider("Occupazione media (%)", 0, 100, 70)
with col3:
    notti_affittabili = st.number_input("Notti affittabili al mese", min_value=0, max_value=31, value=25)

ricavo_lordo_mensile = prezzo_notte * (occupazione/100) * notti_affittabili
st.metric("Ricavo lordo stimato mensile", f"€ {ricavo_lordo_mensile:,.2f}")

# 💸 Costi fissi mensili
st.header("💸 Costi fissi mensili")
costi_fissi = {}
costi_fissi['Condominio'] = st.number_input("Condominio", min_value=0.0, value=100.0)
costi_fissi['Utenze (luce/gas/internet)'] = st.number_input("Utenze", min_value=0.0, value=120.0)
costi_fissi['Pulizie'] = st.number_input("Pulizie", min_value=0.0, value=100.0)
costi_fissi['Commissioni piattaforme'] = st.number_input("Commissioni piattaforme", min_value=0.0, value=80.0)
costi_fissi['Manutenzione'] = st.number_input("Manutenzione media", min_value=0.0, value=50.0)
costi_fissi['Tassa soggiorno / gestione'] = st.number_input("Tassa soggiorno / gestione", min_value=0.0, value=30.0)

totale_costi_fissi = sum(costi_fissi.values())

# 💰 Costi una tantum
st.header("💰 Costi una tantum / investimento iniziale")
costi_una_tantum = {}
costi_una_tantum['Arredo e ristrutturazione'] = st.number_input("Arredo e ristrutturazione", min_value=0.0, value=8000.0)
costi_una_tantum['Spese notarili o di agenzia'] = st.number_input("Spese notarili/agenzia", min_value=0.0, value=3000.0)
costi_una_tantum['Acquisto (facoltativo)'] = st.number_input("Acquisto immobile (facoltativo)", min_value=0.0, value=0.0)
costi_una_tantum['Altro'] = st.number_input("Altro (arredi, elettrodomestici, ecc.)", min_value=0.0, value=1000.0)

totale_investimento = sum(costi_una_tantum.values())

# Calcoli
profitto_mensile = ricavo_lordo_mensile - totale_costi_fissi
profitto_annuo = profitto_mensile * 12
roi = (profitto_annuo / totale_investimento * 100) if totale_investimento > 0 else 0
payback = (totale_investimento / profitto_annuo) if profitto_annuo > 0 else float('inf')

# 📊 Indicatori di redditività
st.header("📊 Indicatori di redditività")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI annuo (%)", f"{roi:.2f}%")
col2.metric("Payback period (anni)", f"{payback:.1f}" if payback != float('inf') else "N/D")
col3.metric("Cash flow mensile", f"€ {profitto_mensile:,.2f}")
col4.metric("Cash flow annuo", f"€ {profitto_annuo:,.2f}")

# 📈 Grafico
st.header("📉 Grafico entrate e costi mensili")
data = pd.DataFrame({
    'Categoria': ['Entrate', 'Costi fissi', 'Profitto netto'],
    'Euro': [ricavo_lordo_mensile, totale_costi_fissi, profitto_mensile]
})
fig, ax = plt.subplots()
ax.bar(data['Categoria'], data['Euro'], color=['green', 'red', 'blue'])
ax.set_ylabel('€')
ax.set_title('Confronto mensile')
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("App creata con ❤️ usando Streamlit - Tutti i dati sono simulazioni modificabili")
