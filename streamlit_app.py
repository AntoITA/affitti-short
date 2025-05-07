from pathlib import Path

# Codice aggiornato Streamlit completo con fiscalità, simulazione multi-anno, export
streamlit_code = '''
import streamlit as st
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulatore ROI Immobiliare", layout="centered")

st.title("📊 Simulatore ROI Immobiliare: Affitto Studenti vs Airbnb")

st.header("📌 Dati di base")

col1, col2 = st.columns(2)

with col1:
    prezzo_casa = st.number_input("Prezzo immobile (€)", value=160000, step=5000)
    percentuale_mutuo = st.slider("Percentuale mutuo (%)", 0, 100, 80)
    tasso_interesse = st.slider("Tasso interesse mutuo (%)", 0.0, 10.0, 3.5)
    anni_mutuo = st.slider("Durata mutuo (anni)", 5, 30, 25)

with col2:
    spese_extra = st.number_input("Spese iniziali (notaio, agenzia, ecc.) (€)", value=15000, step=1000)
    spese_annue = st.number_input("Spese fisse annue (IMU, condominio, manutenzioni, ecc.) (€)", value=2000, step=500)
    anni_simulazione = st.slider("Anni simulazione", 1, 30, 10)
    inflazione = st.slider("Inflazione media annua (%)", 0.0, 5.0, 2.0)

# Calcoli mutuo
capitale_proprio = prezzo_casa * (1 - percentuale_mutuo / 100)
importo_mutuo = prezzo_casa - capitale_proprio
rata_mensile = -npf.pmt(tasso_interesse / 100 / 12, anni_mutuo * 12, importo_mutuo)
rata_annua = rata_mensile * 12

st.subheader("📉 Calcolo rata e capitale")
investimento_totale = capitale_proprio + spese_extra
st.write(f"💰 Capitale proprio investito: **€ {investimento_totale:,.0f}**")
st.write(f"🏦 Rata mensile stimata: **€ {rata_mensile:,.2f}**")
st.write(f"📅 Rata annua stimata: **€ {rata_annua:,.2f}**")

# Scenario studenti
st.header("🏠 Scenario 1: Affitto a studenti")
canone_studente = st.number_input("Canone mensile (€)", value=600, step=50)
st.subheader("📈 Simulazione annua")
data = []
valore_immobile = prezzo_casa

for anno in range(1, anni_simulazione + 1):
    canone_attuale = canone_studente * 12 * ((1 + inflazione/100) ** (anno - 1))
    tasse = canone_attuale * 0.21
    netto = canone_attuale - tasse - spese_annue
    valore_immobile *= (1 + inflazione/100)
    roi = netto / investimento_totale * 100
    data.append(["Studenti", anno, netto, roi, valore_immobile])

# Scenario Airbnb
st.header("🛏️ Scenario 2: Affitto breve (Airbnb)")

prezzo_notte = st.number_input("Prezzo medio per notte (€)", value=70, step=5)
occupazione = st.slider("Occupazione annua (%)", 0, 100, 60)

data_airbnb = []
valore_immobile = prezzo_casa

for anno in range(1, anni_simulazione + 1):
    giorni_occupati = 365 * occupazione / 100
    ricavi = prezzo_notte * giorni_occupati * ((1 + inflazione/100) ** (anno - 1))
    costi = ricavi * 0.40
    tasse = (ricavi - costi) * 0.25
    netto = ricavi - costi - tasse - spese_annue
    valore_immobile *= (1 + inflazione/100)
    roi = netto / investimento_totale * 100
    data_airbnb.append(["Airbnb", anno, netto, roi, valore_immobile])

# DataFrame finale
df = pd.DataFrame(data + data_airbnb, columns=["Tipo", "Anno", "Reddito Netto", "ROI (%)", "Valore Immobile"])
pivot = df.pivot(index="Anno", columns="Tipo", values="ROI (%)")

# Grafico ROI
st.subheader("📊 ROI Annuo Comparato")
st.line_chart(pivot)

# Esportazione
st.subheader("📤 Esporta i dati")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Scarica CSV", csv, "simulazione_roi.csv", "text/csv")

# Tabella finale
st.subheader("📋 Tabella di sintesi")
st.dataframe(df[df["Anno"] == anni_simulazione].set_index("Tipo")[["Reddito Netto", "ROI (%)", "Valore Immobile"]])
'''

# Salvataggio file Streamlit
file_path = Path("/mnt/data/calcolo_roi_streamlit.py")
file_path.write_text(streamlit_code)

file_path.name  # To return the filename only for download link

