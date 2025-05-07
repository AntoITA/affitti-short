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
    
# BOTTONI LINK
# Creiamo due colonne per i bottoni affiancati
col1, col2, col3 = st.columns(3)

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

with col3:
    # Secondo bottone con il link per il calcolo dei costi
    st.markdown("""
        <a href="https://www.tuttoimu.it/app/calcolo-imu.html" target="_blank">
            <button style="padding: 0.5em 1em; font-size: 16px; border: none; background-color: #7B68EE; color: white; border-radius: 5px; cursor: pointer;">
            Calcola IMU
            </button>
        </a>
    """, unsafe_allow_html=True)

totale_investimento_iniziale = prezzo_acquisto + spese_notarili + ristrutturazione + altre_spese

# Opzione di mutuo
mutuo = st.checkbox("Considera mutuo nel calcolo", value=True)
if mutuo:
    tasso_mutuo = st.slider("Tasso d'interesse mutuo (%)", 0.0, 10.0, 3.0, step=0.1)
    durata_mutuo = st.slider("Durata mutuo (anni)", 1, 30, 20)
    importo_mutuo = st.number_input("Importo mutuo (€)", min_value=0.0, value=prezzo_acquisto)
    spese_notarili += 2000  # es. per il mutuo

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

# Calcolo profitto
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

# 📉 Grafico entrate e costi mensili
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

# 🔄 Confronto ROI netto tra affitto breve e lungo
st.markdown("## 📊 Confronto ROI netto: Affitto breve vs. Affitto lungo")
st.markdown("Personalizza i dati per valutare quale modalità di affitto conviene di più, al netto dei costi e delle imposte.")

col1, col2 = st.columns(2)

# Dati per affitto breve
with col1:
    ricavo_breve_annuo = st.number_input("Ricavo annuo affitto breve (€)", value=ricavo_lordo_mensile * 12)
    costi_breve_annui = st.number_input("Costi annuali gestione breve (€)", value=totale_costi_fissi * 12)
    tasse_breve = st.slider("Aliquota tasse affitto breve (%)", 0.0, 30.0, 21.0)

# Dati per affitto lungo
with col2:
    ricavo_lungo_annuo = st.number_input("Ricavo annuo affitto lungo (€)", value=11000.0)
    costi_lungo_annui = st.number_input("Costi annuali gestione lungo (€)", value=1000.0)
    tasse_lungo = st.slider("Aliquota tasse affitto lungo (%)", 0.0, 30.0, 21.0)

# Calcolo ROI netto
netto_breve = (ricavo_breve_annuo - costi_breve_annui) * (1 - tasse_breve / 100)
netto_lungo = (ricavo_lungo_annuo - costi_lungo_annui) * (1 - tasse_lungo / 100)

roi_netto_breve = netto_breve / totale_investimento_iniziale * 100 if totale_investimento_iniziale > 0 else 0
roi_netto_lungo = netto_lungo / totale_investimento_iniziale * 100 if totale_investimento_iniziale > 0 else 0

# Visualizzazione ROI
col1, col2 = st.columns(2)
col1.metric("ROI Netto Affitto Breve (%)", f"{roi_netto_breve:.2f}%")
col2.metric("ROI Netto Affitto Lungo (%)", f"{roi_netto_lungo:.2f}%")

# Grafico comparativo
df_roi = pd.DataFrame({
    "Tipo": ["Affitto Breve", "Affitto Lungo"],
    "ROI Netto": [roi_netto_breve, roi_netto_lungo]
})
fig, ax = plt.subplots()
ax.bar(df_roi["Tipo"], df_roi["ROI Netto"], color=["green", "blue"])
ax.set_ylabel("ROI Netto (%)")
ax.set_title("Confronto ROI Netto")
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("App creata con ❤️ usando Streamlit - Tutti i dati sono simulazioni modificabili")
