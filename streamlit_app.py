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

# BOTTONI LINK
# Creiamo due colonne per i bottoni affiancati
col1, col2 = st.columns(2)

with col1:
    # Primo bottone con il link al calcolo mutuo
    st.markdown("""
        <a href="https://www.mutuisupermarket.it/calcolo-mutuo/calcolo-spese-acquisto-casa" target="_blank">
            <button style="padding: 0.5em 1em; font-size: 16px; border: none; background-color: #4CAF50; color: white; border-radius: 5px; cursor: pointer;">
            Calcola Spese Acquisto Casa (Mutuo)
            </button>
        </a>
    """, unsafe_allow_html=True)

with col2:
    # Secondo bottone con il link per il calcolo dei costi
    st.markdown("""
        <a href="https://www.idealista.it/ristrutturazione/ristrutturazione-della-casa/" target="_blank">
            <button style="padding: 0.5em 1em; font-size: 16px; border: none; background-color: #008CBA; color: white; border-radius: 5px; cursor: pointer;">
            Calcola Costi Acquisto Casa
            </button>
        </a>
    """, unsafe_allow_html=True)

# Opzione di mutuo
mutuo = st.checkbox("Considera mutuo nel calcolo", value=True)
if mutuo:
    tasso_mutuo = st.number_input("Tasso d'interesse mutuo (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.01)
    durata_mutuo = st.slider("Durata mutuo (anni)", 1, 30, 20)
    importo_mutuo = st.number_input("Importo mutuo (€)", min_value=0.0, value=prezzo_acquisto)
    spese_notarili += 2000  # aggiunta spese mutuo

# 📈 Entrate previste affitto breve
st.header("📈 Entrate previste - Affitto breve")
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

# Aliquota tasse
tasse_breve = st.slider("Aliquota tasse affitto breve (%)", 0.0, 30.0, 21.0, key="tasse_breve")
tasse_mensili_breve = ricavo_lordo_mensile * (tasse_breve / 100)

# Profitto netto affitto breve
profitto_mensile = ricavo_lordo_mensile - totale_costi_fissi - tasse_mensili_breve
profitto_annuo = profitto_mensile * 12
roi = (profitto_annuo / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0
payback = (totale_investimento_iniziale / profitto_annuo) if profitto_annuo > 0 else float('inf')

# 📊 Indicatori di redditività affitto breve
st.header("📊 Indicatori di redditività - Affitto breve")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI annuo (%)", f"{roi:.2f}%")
col2.metric("Payback period (anni)", f"{payback:.1f}" if payback != float('inf') else "N/D")
col3.metric("Cash flow mensile", f"€ {profitto_mensile:,.2f}")
col4.metric("Cash flow annuo", f"€ {profitto_annuo:,.2f}")

# Calcolo del ROI e del Payback
roi = (profitto_annuo / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0
payback = (totale_investimento_iniziale / profitto_annuo) if profitto_annuo > 0 else float('inf')

# Indicatori di redditività
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


# 📈 Grafico entrate e costi mensili affitto breve
st.header("📉 Grafico entrate e costi mensili - Affitto breve")
data = pd.DataFrame({
    'Categoria': ['Entrate', 'Costi fissi', 'Tasse', 'Profitto netto'],
    'Euro': [ricavo_lordo_mensile, totale_costi_fissi, tasse_mensili_breve, profitto_mensile]
})
fig, ax = plt.subplots()
ax.bar(data['Categoria'], data['Euro'], color=['green', 'red', 'orange', 'blue'])
ax.set_ylabel('€')
ax.set_title('Confronto mensile affitto breve')
st.pyplot(fig)

import streamlit as st

# 📘 AFFITTO LUNGO
st.header("🏡 Affitto lungo termine")

# Input dati affitto lungo
affitto_lungo_mensile = st.number_input("Canone affitto lungo (€ / mese)", min_value=0.0, value=900.0)
spese_lungo = {}
spese_lungo["Condominio"] = st.number_input("Spese condominiali a carico locatore", min_value=0.0, value=100.0, key="condo_lungo")
spese_lungo["Manutenzione"] = st.number_input("Manutenzione ordinaria", min_value=0.0, value=50.0, key="manut_lungo")
spese_lungo["IMU / Tasse"] = st.number_input("Tasse (IMU ecc.)", min_value=0.0, value=100.0, key="imu_lungo")
tasse_lungo = st.slider("Aliquota tasse affitto lungo (%)", 0.0, 30.0, 21.0, key="tasse_lungo")

# Calcolo delle spese e profitto
totale_spese_lungo = sum(spese_lungo.values())
tasse_mensili_lungo = affitto_lungo_mensile * (tasse_lungo / 100)
profitto_mensile_lungo = affitto_lungo_mensile - totale_spese_lungo - tasse_mensili_lungo
profitto_annuo_lungo = profitto_mensile_lungo * 12
# Aggiungi qui la variabile totale_investimento_iniziale per calcolare il ROI
totale_investimento_iniziale = 100000  # esempio
roi_lungo = (profitto_annuo_lungo / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0

# Aggiungere il bottone in una colonna singola
col1, = st.columns([1])  # crea una colonna a larghezza singola
with col1:
    # Primo bottone con il link al calcolo mutuo
    st.markdown("""
        <a href="https://www.tuttoimu.it/app/calcolo-imu.html" target="_blank">
            <button style="padding: 0.5em 1em; font-size: 16px; border: none; background-color: #4CAF50; color: white; border-radius: 5px; cursor: pointer;">
            Vai al calcolatore IMU
            </button>
        </a>
    """, unsafe_allow_html=True)

# Confronto affitto lungo vs breve
st.header("📊 Confronto Affitto Breve vs Lungo")
col1, col2, col3 = st.columns(3)
col1.metric("Profitto mensile breve", f"€ {profitto_mensile_lungo:,.2f}")
col1.metric("Profitto mensile lungo", f"€ {profitto_mensile_lungo:,.2f}")
col2.metric("ROI annuo breve", f"{roi_lungo:.2f}%")
col2.metric("ROI annuo lungo", f"{roi_lungo:.2f}%")
col3.metric("Payback lungo", f"{(totale_investimento_iniziale / profitto_annuo_lungo):.1f}" if profitto_annuo_lungo > 0 else "N/D")


# 📉 Grafico confronto
df_confronto = pd.DataFrame({
    'Tipo': ['Breve', 'Lungo'],
    'Profitto mensile': [profitto_mensile, profitto_mensile_lungo],
    'ROI annuo (%)': [roi, roi_lungo]
})
fig2, ax2 = plt.subplots()
df_confronto.set_index('Tipo')[['Profitto mensile', 'ROI annuo (%)']].plot(kind='bar', ax=ax2)
ax2.set_title('Confronto affitto breve vs lungo')
ax2.set_ylabel('€ / %')
st.pyplot(fig2)

# Esportazione dati
st.header("⬇️ Esporta dati")
dati_export = {
    'Prezzo medio per notte': prezzo_notte,
    'Occupazione media (%)': occupazione,
    'Notti affittabili': notti_affittabili,
    'Ricavo lordo mensile': ricavo_lordo_mensile,
    'Totale costi fissi': totale_costi_fissi,
    'Tasse affitto breve': tasse_mensili_breve,
    'Profitto mensile breve': profitto_mensile,
    'Profitto annuo breve': profitto_annuo,
    'ROI breve (%)': roi,
    'Affitto lungo mensile': affitto_lungo_mensile,
    'Spese lungo': totale_spese_lungo,
    'Tasse affitto lungo': tasse_mensili_lungo,
    'Profitto mensile lungo': profitto_mensile_lungo,
    'Profitto annuo lungo': profitto_annuo_lungo,
    'ROI lungo (%)': roi_lungo,
}
df_export = pd.DataFrame(dati_export.items(), columns=['Voce', 'Valore'])
csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Scarica dati in CSV",
    data=csv,
    file_name='report_confronto_affitto.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.caption("App creata con ❤️ usando Streamlit - Tutti i dati sono simulazioni modificabili")
