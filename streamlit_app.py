import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Impostazioni pagina
st.set_page_config(page_title="Analisi Redditività Affitto", layout="wide")
st.title("📊 Dashboard Affitto Breve vs Lungo Periodo - Redditività Immobiliare")

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
costi_fissi['Condominio'] = st.number_input("Condominio (€)", min_value=0.0, value=100.0)
costi_fissi['Utenze (luce/gas/internet)'] = st.number_input("Utenze (€)", min_value=0.0, value=120.0)
costi_fissi['Pulizie'] = st.number_input("Pulizie (€)", min_value=0.0, value=100.0)
costi_fissi['Commissioni piattaforme'] = st.number_input("Commissioni piattaforme (€)", min_value=0.0, value=80.0)
costi_fissi['Manutenzione'] = st.number_input("Manutenzione media (€)", min_value=0.0, value=50.0)
costi_fissi['Tassa soggiorno / gestione'] = st.number_input("Tassa soggiorno / gestione (€)", min_value=0.0, value=30.0)

totale_costi_fissi = sum(costi_fissi.values())

# 💰 Mutuo (opzionale)
inserisci_mutuo = st.checkbox("Considera Mutuo nei calcoli")
if inserisci_mutuo:
    st.header("💰 Dati Mutuo")
    importo_mutuo = st.number_input("Importo del mutuo (€)", min_value=0.0, value=70000.0)
    durata_mutuo = st.number_input("Durata del mutuo (anni)", min_value=5, max_value=30, value=20)
    tasso_mutuo = st.number_input("Tasso d'interesse annuale (%)", min_value=0.0, max_value=10.0, value=3.5)
    rata_mutuo = (importo_mutuo * tasso_mutuo / 100) / 12  # Calcolo semplificato del mutuo (senza ammortamento complesso)
    st.metric("Rata mensile mutuo", f"€ {rata_mutuo:,.2f}")
else:
    rata_mutuo = 0
# 💰 Ammortamento mutuo
import numpy as np

# Calcolare ammortamento mensile
def calcola_ammortamento(importo_mutuo, tasso, durata):
    tasso_mensile = tasso / 100 / 12
    durata_mesi = durata * 12
    rata = importo_mutuo * tasso_mensile / (1 - (1 + tasso_mensile) ** -durata_mesi)
    
    # Calcolo del piano di ammortamento
    ammortamento = []
    capitale_residuo = importo_mutuo
    for mese in range(1, durata_mesi + 1):
        interesse = capitale_residuo * tasso_mensile
        capitale = rata - interesse
        capitale_residuo -= capitale
        ammortamento.append((mese, rata, interesse, capitale, capitale_residuo))
    
    return pd.DataFrame(ammortamento, columns=['Mese', 'Rata', 'Interesse', 'Capitale', 'Capitale Residuo'])

# Mostra piano di ammortamento se il mutuo è selezionato
if inserisci_mutuo:
    ammortamento_df = calcola_ammortamento(importo_mutuo, tasso_mutuo, durata_mutuo)
    st.subheader("Piano di ammortamento del mutuo")
    st.dataframe(ammortamento_df)

# 📈 Grafico di Ammortamento
fig_ammortamento, ax_ammortamento = plt.subplots(figsize=(6, 4))
ax_ammortamento.plot(ammortamento_df['Mese'], ammortamento_df['Capitale Residuo'], label="Capitale Residuo", color='red')
ax_ammortamento.set_title("Ammortamento del Mutuo nel Tempo")
ax_ammortamento.set_xlabel("Mese")
ax_ammortamento.set_ylabel("€")
st.pyplot(fig_ammortamento)

# Calcoli principali
profitto_mensile = ricavo_lordo_mensile - totale_costi_fissi - rata_mutuo
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
    'Categoria': ['Entrate', 'Costi fissi', 'Mutuo', 'Profitto netto'],
    'Euro': [ricavo_lordo_mensile, totale_costi_fissi, rata_mutuo, profitto_mensile]
})
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(data['Categoria'], data['Euro'], color=['green', 'red', 'purple', 'blue'])
ax.set_ylabel('€')
ax.set_title('Confronto entrate, costi e mutuo mensili')
st.pyplot(fig)

# 📈 Link calcolo mutuo
st.subheader("🔗 Calcolo mutuo e spese notarili")
st.markdown("[Clicca qui per calcolare mutuo e spese notarili](https://www.mutuisupermarket.it/calcolo-mutuo/calcolo-spese-acquisto-casa)")

# 💼 Opzione per comparare affitto breve e lungo termine
st.header("💼 Confronto Affitto Breve vs Lungo Periodo")
affitto_lungo_termine = st.checkbox("Considera Affitto Lungo Periodo", value=False)

if affitto_lungo_termine:
    # Dati per affitto lungo periodo (ad esempio, contratto 12 mesi)
    canone_mensile_lungo = st.number_input("Canone mensile affitto lungo periodo (€)", min_value=0.0, value=500.0)
    durata_contratto = st.number_input("Durata del contratto (anni)", min_value=1, value=1)
    
    # Calcolo per affitto lungo periodo
    ricavo_annuo_lungo = canone_mensile_lungo * 12
    profitto_annuo_lungo = ricavo_annuo_lungo - totale_costi_fissi * 12  # Escludendo costi di piattaforma e pulizie

    roi_lungo = (profitto_annuo_lungo / totale_investimento_iniziale * 100) if totale_investimento_iniziale > 0 else 0
    payback_lungo = (totale_investimento_iniziale / profitto_annuo_lungo) if profitto_annuo_lungo > 0 else float('inf')

    # Mostra indicatori lungo periodo
    st.subheader("Indicatori Affitto Lungo Periodo")
    col1, col2 = st.columns(2)
    col1.metric("ROI annuo Affitto Lungo (%)", f"{roi_lungo:.2f}%")
    col2.metric("Payback Period Affitto Lungo (anni)", f"{payback_lungo:.1f}" if payback_lungo != float('inf') else "N/D")
    
    # Grafico comparativo
    st.header("📊 Grafico comparativo Affitto Breve vs Lungo Periodo")
    data_comparativa = pd.DataFrame({
        'Categoria': ['Affitto Breve', 'Affitto Lungo'],
        'ROI (%)': [roi, roi_lungo],
        'Payback Period (anni)': [payback, payback_lungo]
    })
    
    fig_comparativo, ax_comparativo = plt.subplots(figsize=(6, 4))
    data_comparativa.plot(kind='bar', x='Categoria', y=['ROI (%)', 'Payback Period (anni)'], ax=ax_comparativo)
    ax_comparativo.set_title("Confronto ROI e Payback tra Affitto Breve e Lungo")
    st.pyplot(fig_comparativo)

    # Conclusioni finali
    if roi > roi_lungo:
        st.markdown("💡 **Conclusioni:** L'affitto breve offre un ROI annuo più elevato rispetto all" )
