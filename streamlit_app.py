import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

# --------------------------
# PARAMETRI PRINCIPALI
# --------------------------

st.title("Analisi Investimento Immobiliare - Milano")

st.sidebar.header("Parametri Immobile")
prezzo_acquisto = st.sidebar.number_input("Prezzo di acquisto (€)", min_value=50000, max_value=1500000, value=300000, step=1000)
rendita_lorda = st.sidebar.slider("Rendimento lordo annuo stimato (%)", 1.0, 10.0, 5.0)
spese_gestione_annua = st.sidebar.number_input("Spese di gestione e mantenimento annuali (€)", value=1800)
sfitto_percent = st.sidebar.slider("Percentuale sfitto annuale (%)", 0.0, 20.0, 5.0)
tasse_cedolare = st.sidebar.slider("Cedolare secca / tassazione affitto (%)", 15, 26, 21)

# Rivalutazione immobile
rivalutazione_annua = st.sidebar.slider("Rivalutazione immobile annua (%)", 0.0, 5.0, 1.5)
anni_orizzonte = st.sidebar.slider("Orizzonte temporale analisi (anni)", 5, 30, 15)

# Spese straordinarie
spese_straordinarie = st.sidebar.number_input("Spese straordinarie previste totali in orizzonte (€)", value=5000)

# --------------------------
# PARAMETRI MUTUO (FACOLTATIVO)
# --------------------------

st.sidebar.header("Finanziamento (Mutuo)")
usa_mutuo = st.sidebar.checkbox("Acquisto con mutuo?", value=False)

if usa_mutuo:
    percentuale_mutuo = st.sidebar.slider("Percentuale finanziata dal mutuo (%)", 50, 90, 70)
    tasso_interesse = st.sidebar.slider("Tasso interesse mutuo (%)", 1.0, 5.0, 3.0)
    durata_anni = st.sidebar.slider("Durata mutuo (anni)", 10, 35, 25)

# --------------------------
# COMPARAZIONE CON AFFITTO
# --------------------------

st.sidebar.header("Alternativa: Affitto Long-Term")
canone_affitto = st.sidebar.number_input("Canone affitto mensile equivalente (€)", value=1100)
invest_alt_rendimento = st.sidebar.slider("Rendimento alternativo investimento (%)", 2.0, 8.0, 4.0)

# --------------------------
# CALCOLI ECONOMICI
# --------------------------

rendita_lorda_euro = prezzo_acquisto * rendita_lorda / 100
rendita_netto_post_sfitto = rendita_lorda_euro * (1 - sfitto_percent / 100)
rendita_netto_post_tasse = rendita_netto_post_sfitto * (1 - tasse_cedolare / 100)
cashflow_netto_annuo = rendita_netto_post_tasse - spese_gestione_annua

valore_attuale = prezzo_acquisto
storico_valori = []

for anno in range(1, anni_orizzonte + 1):
    valore_attuale *= (1 + rivalutazione_annua / 100)
    storico_valori.append({
        "Anno": anno,
        "Valore Immobile": valore_attuale,
        "Rendita Netta": cashflow_netto_annuo,
        "Accumulato Netto": cashflow_netto_annuo * anno
    })

df = pd.DataFrame(storico_valori)

# --------------------------
# MUTUO
# --------------------------

if usa_mutuo:
    quota_mutuo = prezzo_acquisto * percentuale_mutuo / 100
    quota_contanti = prezzo_acquisto - quota_mutuo
    r = tasso_interesse / 100 / 12
    n = durata_anni * 12
    rata_mensile = quota_mutuo * r * (1 + r) ** n / ((1 + r) ** n - 1)
    rata_annua = rata_mensile * 12
    cashflow_netto_post_mutuo = cashflow_netto_annuo - rata_annua
    roi_netto = cashflow_netto_post_mutuo / quota_contanti * 100
else:
    quota_contanti = prezzo_acquisto
    rata_annua = 0
    cashflow_netto_post_mutuo = cashflow_netto_annuo
    roi_netto = cashflow_netto_annuo / prezzo_acquisto * 100

# --------------------------
# ALTERNATIVA AFFITTO
# --------------------------

investimento_equivalente = quota_contanti * (invest_alt_rendimento / 100)
costo_affitto_annuo = canone_affitto * 12
differenza = investimento_equivalente - costo_affitto_annuo

# --------------------------
# RISULTATI
# --------------------------

st.header("📊 Risultati Economici")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Reddito Immobiliare")
    st.metric("Cashflow netto annuo (€)", f"{cashflow_netto_post_mutuo:,.0f}")
    st.metric("ROI netto (%)", f"{roi_netto:.2f}")
    st.metric("Valore finale immobile (€)", f"{valore_attuale:,.0f}")

with col2:
    st.subheader("Alternativa: Affitto")
    st.metric("Rendita alternativa (€)", f"{investimento_equivalente:,.0f}")
    st.metric("Costo annuo affitto (€)", f"{costo_affitto_annuo:,.0f}")
    st.metric("Differenza (€)", f"{differenza:,.0f}")

st.markdown("---")
st.subheader("📈 Evoluzione del Valore Immobiliare")
st.line_chart(df.set_index("Anno")["Valore Immobile"])

st.subheader("📄 Tabella riepilogativa")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("💡 *Il calcolo include rivalutazione, tasse, sfitto, spese di mantenimento, mutuo (opzionale), e confronto con investimento alternativo e affitto.*")
