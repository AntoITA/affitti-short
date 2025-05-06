import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Funzione per calcolare il piano di ammortamento
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

# Funzione per simulare l'affitto a breve termine
def calcola_affitto_breve(rent_per_night, occupancy_rate, days_per_month):
    return rent_per_night * occupancy_rate * days_per_month

# Funzione per simulare l'affitto a lungo termine
def calcola_affitto_lungo(canone_mensile):
    return canone_mensile * 12  # Stima annuale

# Funzione per analisi fiscale
def calcolo_tasse(guadagni_annuali, aliquota_imposta):
    return guadagni_annuali * aliquota_imposta / 100

# Funzione per calcolo scenario futuro
def scenario_futuro(valore_iniziale, crescita_percentuale, anni):
    return valore_iniziale * (1 + crescita_percentuale/100)**anni

# Interfaccia utente con Streamlit
st.title("Analisi Investimento Immobiliare")

# Sezione per input dell'utente
st.sidebar.header("Dati Iniziali")
importo_mutuo = st.sidebar.number_input("Importo del Mutuo (€)", value=100000, min_value=0)
tasso_mutuo = st.sidebar.number_input("Tasso di Interesse Mutuo (%)", value=3.5, min_value=0.0)
durata_mutuo = st.sidebar.number_input("Durata Mutuo (Anni)", value=20, min_value=1)
spese_notarili = st.sidebar.number_input("Spese Notarili (€)", value=5000, min_value=0)
inserisci_mutuo = st.sidebar.checkbox("Considerare il mutuo nel calcolo?", value=True)

# Sezione per affitto a breve o lungo termine
affitto_breve = st.sidebar.checkbox("Affitto Breve")
canone_mensile = st.sidebar.number_input("Canone Mensile Affitto Lungo (€)", value=1000, min_value=0)

# Parametri per l'affitto breve
if affitto_breve:
    rent_per_night = st.sidebar.number_input("Prezzo per notte (€)", value=100, min_value=0)
    occupancy_rate = st.sidebar.slider("Tasso di Occupazione (%)", min_value=0, max_value=100, value=80)
    days_per_month = 30  # Numero fisso di giorni per mese

# Calcoli e simulazioni
# Calcolo del mutuo
if inserisci_mutuo:
    ammortamento_df = calcola_ammortamento(importo_mutuo, tasso_mutuo, durata_mutuo)
    st.subheader("Piano di Ammortamento del Mutuo")
    st.dataframe(ammortamento_df)

    # Grafico dell'ammortamento
    fig_ammortamento, ax_ammortamento = plt.subplots(figsize=(6, 4))
    ax_ammortamento.plot(ammortamento_df['Mese'], ammortamento_df['Capitale Residuo'], label="Capitale Residuo", color='red')
    ax_ammortamento.set_title("Ammortamento del Mutuo nel Tempo")
    ax_ammortamento.set_xlabel("Mese")
    ax_ammortamento.set_ylabel("€")
    st.pyplot(fig_ammortamento)

# Calcoli per l'affitto
if affitto_breve:
    ricavi_affitto_breve = calcola_affitto_breve(rent_per_night, occupancy_rate, days_per_month)
    st.subheader(f"Ricavi Annui Affitto Breve: {ricavi_affitto_breve:.2f} €")

# Calcoli per l'affitto lungo termine
ricavi_affitto_lungo = calcola_affitto_lungo(canone_mensile)
st.subheader(f"Ricavi Annui Affitto Lungo: {ricavi_affitto_lungo:.2f} €")

# Calcolo delle tasse sugli affitti
tasse_affitto_breve = calcolo_tasse(ricavi_affitto_breve, 20)  # esempio aliquota 20%
tasse_affitto_lungo = calcolo_tasse(ricavi_affitto_lungo, 20)  # esempio aliquota 20%

st.subheader(f"Tasse Affitto Breve: {tasse_affitto_breve:.2f} €")
st.subheader(f"Tasse Affitto Lungo: {tasse_affitto_lungo:.2f} €")

# Scenario di crescita a lungo termine per l'affitto
scenari_lungo_periodo_breve = scenario_futuro(ricavi_affitto_breve, 3, 10)  # 3% di crescita annuale
scenari_lungo_periodo_lungo = scenario_futuro(ricavi_affitto_lungo, 2, 10)  # 2% di crescita annuale

st.subheader(f"Ricavi Affitto Breve a 10 anni: {scenari_lungo_periodo_breve:.2f} €")
st.subheader(f"Ricavi Affitto Lungo a 10 anni: {scenari_lungo_periodo_lungo:.2f} €")

# Grafico di comparazione tra i due
fig_comparazione, ax_comparazione = plt.subplots(figsize=(6, 4))
ax_comparazione.plot([1, 2], [ricavi_affitto_breve, ricavi_affitto_lungo], label="Ricavi Affitto", color='blue')
ax_comparazione.set_xticks([1, 2])
ax_comparazione.set_xticklabels(['Affitto Breve', 'Affitto Lungo'])
ax_comparazione.set_title("Comparazione tra Affitto Breve e Lungo")
ax_comparazione.set_ylabel("€ Annui")
st.pyplot(fig_comparazione)

# Esportazione in PDF o Excel
if st.button("Esporta Report"):
    # Codice per esportare il report in formato PDF o Excel
    pass  # da implementare secondo necessità

# Link utile per calcolo delle spese notarili
st.markdown("Per il calcolo delle spese notarili puoi visitare il [calcolatore online](https://www.mutuisupermarket.it/calcolo-mutuo/calcolo-spese-acquisto-casa).")
