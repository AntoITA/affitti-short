import streamlit as st
import numpy as np
import pandas as pd

# Funzione di calcolo ROI
def calcola_roi(prezzo_acquisto, valore_mercato, canone_annuo, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, rivalutazione_annua=0.02):
    # Calcolo del costo dell'immobile
    valore_finale = prezzo_acquisto * (1 + rivalutazione_annua)
    
    # Calcolo dell'affitto netto (togliendo le spese e le imposte)
    reddito_netto = canone_annuo - spese_annual - imposte_annual
    
    # Se c'è un mutuo, calcoliamo la rata annuale
    if mutuo > 0:
        rata_annua = mutuo * (tasso_mutuo / 100) * (1 + tasso_mutuo / 100)**durata_mutuo / ((1 + tasso_mutuo / 100)**durata_mutuo - 1)
    else:
        rata_annua = 0
    
    # Reddito netto dopo mutuo
    reddito_netto_post_mutuo = reddito_netto - rata_annua
    
    # Calcolo ROI
    investimento_totale = prezzo_acquisto + spese_annual + imposte_annual
    ritorno_annuo = reddito_netto_post_mutuo + (valore_finale - prezzo_acquisto) / durata_mutuo
    
    roi = (ritorno_annuo / investimento_totale) * 100  # ROI in percentuale
    return roi, reddito_netto_post_mutuo, rata_annua, valore_finale

# Funzione di calcolo affitto vs acquisto
def calcola_affitto_vs_acquisto(prezzo_acquisto, valore_mercato, canone_affitto, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, rivalutazione_annua=0.02):
    # Calcolo ROI per acquisto
    roi_acquisto, _, _, _ = calcola_roi(prezzo_acquisto, valore_mercato, canone_affitto, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, rivalutazione_annua)
    
    # Calcolo ROI per affitto (investendo il capitale iniziale)
    capitale_iniziale = prezzo_acquisto * 0.2  # 20% del prezzo di acquisto come acconto
    capitale_investito = capitale_iniziale  # Simuliamo l'investimento di questa cifra in un ETF o altro prodotto con ROI atteso
    ritorno_annuo_affitto = capitale_investito * 0.05  # ROI ipotetico del 5% annuale sull'investimento
    
    # Confronto ROI acquisto vs affitto
    roi_affitto = ritorno_annuo_affitto / capitale_investito * 100  # ROI in percentuale

    return roi_acquisto, roi_affitto

# Interfaccia Streamlit
st.title("Analisi Investimento Immobiliare a Milano")

# Parametri input
prezzo_acquisto = st.number_input("Prezzo di acquisto dell'immobile (€):", min_value=50000, max_value=5000000, step=10000, value=300000)
canone_annuo = st.number_input("Canone di affitto annuale (€):", min_value=0, step=100, value=12000)
spese_annual = st.number_input("Spese annuali di gestione (assicurazione, manutenzione, ecc.): (€)", min_value=0, step=100, value=2000)
imposte_annual = st.number_input("Imposte annuali (cedolare secca, IMU, ecc.): (€)", min_value=0, step=100, value=1500)
mutuo = st.number_input("Importo mutuo (€):", min_value=0, max_value=prezzo_acquisto, step=10000, value=200000)
durata_mutuo = st.number_input("Durata del mutuo (anni):", min_value=5, max_value=30, step=1, value=20)
tasso_mutuo = st.number_input("Tasso di interesse mutuo (%):", min_value=0.1, max_value=10.0, step=0.1, value=3.0)
rivalutazione_annua = st.number_input("Rivalutazione annua dell'immobile (%):", min_value=0.0, max_value=10.0, step=0.1, value=2.0)
canone_affitto = st.number_input("Canone mensile affitto (per comparazione): (€)", min_value=0, step=100, value=900)

# Calcola ROI acquisto e affitto
roi_acquisto, roi_affitto = calcola_affitto_vs_acquisto(prezzo_acquisto, prezzo_acquisto, canone_annuo, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, rivalutazione_annua)

# Visualizzazione
st.subheader("Risultati:")
st.write(f"**ROI Acquisto Immobiliare**: {roi_acquisto:.2f}% annuo")
st.write(f"**ROI Affitto e Investimento Capitale**: {roi_affitto:.2f}% annuo")

# Confronto affitto vs acquisto
if roi_acquisto > roi_affitto:
    st.write("L'acquisto dell'immobile è più vantaggioso rispetto all'affitto e investimento del capitale.")
else:
    st.write("Affittare e investire il capitale iniziale potrebbe essere una scelta migliore rispetto all'acquisto.")

# Dettaglio del mutuo
if mutuo > 0:
    rata_annua = mutuo * (tasso_mutuo / 100) * (1 + tasso_mutuo / 100)**durata_mutuo / ((1 + tasso_mutuo / 100)**durata_mutuo - 1)
    st.write(f"**Rata annuale mutuo**: {rata_annua:.2f} €")
