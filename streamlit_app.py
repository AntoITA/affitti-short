import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisi Redditività Affitto", layout="wide")

st.title("📊 Dashboard Affitto Breve - Redditività Immobiliare")

# Sidebar per i dati di investimento iniziale e parametri fiscali
st.sidebar.header("🏠 Dati di acquisto e investimento iniziale")
col1, col2 = st.sidebar.columns(2)
with col1:
    prezzo_acquisto = st.number_input("Prezzo di acquisto immobile (€)", min_value=0.0, value=100000.0)
    spese_notarili = st.number_input("Spese notarili / agenzia (€)", min_value=0.0, value=3000.0)
with col2:
    ristrutturazione = st.number_input("Ristrutturazione / Arredo (€)", min_value=0.0, value=8000.0)
    altre_spese = st.number_input("Altre spese iniziali (€)", min_value=0.0, value=1000.0)

totale_investimento_iniziale = prezzo_acquisto + spese_notarili + ristrutturazione + altre_spese

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

# Aliquota fiscale
aliquota_fiscale = st.number_input("Aliquota fiscale (%)", min_value=0.0, max_value=100.0, value=21.0)

# Calcoli
profitto_mensile = ricavo_lordo_mensile - totale_costi_fissi
profitto_annuo = profitto_mensile * 12
profitto_annuo_netto = profitto_annuo * (1 - aliquota_fiscale / 100)
roi = (profitto_annuo / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0
roi_netto = (profitto_annuo_netto / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0
payback = (totale_investimento_iniziale / profitto_annuo) if profitto_annuo > 0 else float('inf')
payback_netto = (totale_investimento_iniziale / profitto_annuo_netto) if profitto_annuo_netto > 0 else float('inf')

# 📊 Indicatori di redditività
st.header("📊 Indicatori di redditività")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI annuo (%)", f"{roi:.2f}%")
col2.metric("ROI annuo netto (%)", f"{roi_netto:.2f}%")
col3.metric("Payback period (anni)", f"{payback:.1f}" if payback != float('inf') else "N/D")
col4.metric("Payback period netto (anni)", f"{payback_netto:.1f}" if payback_netto != float('inf') else "N/D")
col1.metric("Cash flow mensile", f"€ {profitto_mensile:,.2f}")
col2.metric("Cash flow annuo", f"€ {profitto_annuo:,.2f}")
col3.metric("Cash flow annuo netto", f"€ {profitto_annuo_netto:,.2f}")

# 💼 Valutazione finale con semaforo
if roi_netto > 8:
    st.success("🔝 Ottima redditività netta")
elif roi_netto > 4:
    st.warning("⚠️ Redditività discreta")
else:
    st.error("🔻 Redditività bassa")

# 📈 Grafico cumulativo
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

# Grafico cumulativo
st.header("📊 Grafico del recupero del capitale e cash flow annuo")
anni = 10
cashflow_annuo = [profitto_annuo_netto] * anni
recupero = [sum(cashflow_annuo[:i+1]) for i in range(anni)]
df_cum = pd.DataFrame({
    'Anno': list(range(1, anni+1)),
    'Cash flow annuo netto': cashflow_annuo,
    'Capitale recuperato': recupero
})
st.line_chart(df_cum.set_index("Anno"))

# 📈 Affitto lungo termine - Confronto
st.header("🏠 Confronto con Affitto Lungo Periodo")
canone_mensile = st.number_input("Canone affitto mensile (€)", min_value=0.0, value=700.0)
spese_condominiali = st.number_input("Spese condominiali / manutenzione (€)", min_value=0.0, value=100.0)
guadagno_affitto = canone_mensile * 12
guadagno_affitto_netto = guadagno_affitto - (spese_condominiali * 12)

# 📊 Confronto finale
st.metric("Guadagno annuo da affitto lungo periodo", f"€ {guadagno_affitto:,.2f}")
st.metric("Guadagno annuo netto da affitto lungo periodo", f"€ {guadagno_affitto_netto:,.2f}")

# ⬇️ Esporta dati
st.header("⬇️ Esporta dati")
dati_export = {
    'Prezzo medio per notte': prezzo_notte,
    'Occupazione media (%)': occupazione,
    'Notti affittabili': notti_affittabili,
    'Ricavo lordo mensile': ricavo_lordo_mensile,
    'Totale costi fissi': totale_costi_fissi,
    'Totale investimento iniziale': totale_investimento_iniziale,
    'Profitto mensile': profitto_mensile,
    'Profitto annuo': profitto_annuo,
    'Profitto annuo netto': profitto_annuo_netto,
    'ROI annuo (%)': roi,
    'ROI annuo netto (%)': roi_netto,
    'Payback (anni)': payback,
    'Payback netto (anni)': payback_netto,
    'Cash flow mensile': profitto_mensile,
    'Cash flow annuo': profitto_annuo,
    'Cash flow annuo netto': profitto_annuo_netto,
    'Guadagno annuo da affitto lungo periodo': guadagno_affitto,
    'Guadagno annuo netto da affitto lungo periodo': guadagno_affitto_netto
}
df_export = pd.DataFrame(dati_export.items(), columns=['Voce', 'Valore'])
csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Scarica dati in CSV",
    data=csv,
    file_name='report_affitto.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.caption("App creata con ❤️ usando Streamlit - Tutti i dati sono simulazioni modificabili")
