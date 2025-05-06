import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titolo della pagina
st.set_page_config(page_title="Analisi Redditività Affitto", layout="wide")

# 🏠 Dati di acquisto e investimento iniziale
st.header("🏠 Dati di acquisto e investimento iniziale")
col1, col2 = st.columns(2)
with col1:
    prezzo_acquisto = st.number_input("Prezzo di acquisto immobile (€)", min_value=0.0, value=100000.0)
    spese_notarili = st.number_input("Spese notarili / agenzia (€)", min_value=0.0, value=3000.0)
with col2:
    ristrutturazione = st.number_input("Ristrutturazione / Arredo (€)", min_value=0.0, value=8000.0)
    altre_spese = st.number_input("Altre spese iniziali (€)", min_value=0.0, value=1000.0)

totale_investimento_iniziale = prezzo_acquisto + spese_notarili + ristrutturazione + altre_spese

# Opzione di mutuo
mutuo = st.checkbox("Considera mutuo nel calcolo", value=True)
if mutuo:
    tasso_mutuo = st.slider("Tasso d'interesse mutuo (%)", 0, 10, 3)
    durata_mutuo = st.slider("Durata mutuo (anni)", 1, 30, 20)
    importo_mutuo = st.number_input("Importo mutuo (€)", min_value=0.0, value=prezzo_acquisto)
    spese_notarili = spese_notarili + 2000  # es. per il mutuo

# 📈 Entrate previste
st.header("📈 Entrate previste")
col1, col2, col3 = st.columns(3)
with col1:
    prezzo_notte = st.number_input("Prezzo medio per notte (€)", min_value=0.0, value=90.0)
with col2:
    occupazione = st.slider("Occupazione media (%)", 0, 100, 70)
with col3:
    notti_affittabili = st.number_input("Notti affittabili al mese", min_value=0, max_value=31, value=25)

ricavo_lordo_mensile = prezzo_notte * (occupazione / 100) * notti_affittabili
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

# Calcolo tasse
def calcolo_tasse(ricavi, aliquota):
    return ricavi * (aliquota / 100)

# Calcolo del profitto
profitto_mensile = ricavo_lordo_mensile - totale_costi_fissi
profitto_annuo = profitto_mensile * 12
roi = (profitto_annuo / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0
payback = (totale_investimento_iniziale / profitto_annuo) if profitto_annuo > 0 else float('inf')

# 📊 Indicatori di redditività
st.header("📊 Indicatori di redditività")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI annuo (%)", f"{roi:.2f}%")
col2.metric("Payback period (anni)", f"{payback:.1f}" if payback != float('inf') else "N/D")
col3.metric("Cash flow mensile", f"€ {profitto_mensile:,.2f}")
col4.metric("Cash flow annuo", f"€ {profitto_annuo:,.2f}")

# Valutazione qualitativa della redditività
if roi >= 8:
    st.success("🔝 Redditività **Alta** (ROI ≥ 8%)")
elif roi >= 4:
    st.warning("⚠️ Redditività **Media** (4% ≤ ROI < 8%)")
else:
    st.error("🔻 Redditività **Bassa** (ROI < 4%)")


# 📈 Grafico entrate e costi mensili
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

# Esporta dati
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
    'ROI annuo (%)': roi,
    'Payback (anni)': payback
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
