import streamlit as st
import numpy as np
import pandas as pd

# Funzione per calcolare il ROI dell'acquisto
def calcola_roi_acquisto(prezzo_acquisto, canone_annuo, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, rivalutazione_annua=0.02):
    # Calcolare l'affitto netto (togliendo le spese e le imposte)
    reddito_netto = canone_annuo - spese_annual - imposte_annual
    
    # Se c'è un mutuo, calcoliamo la rata annuale
    if mutuo > 0:
        rata_annua = mutuo * (tasso_mutuo / 100) * (1 + tasso_mutuo / 100)**durata_mutuo / ((1 + tasso_mutuo / 100)**durata_mutuo - 1)
    else:
        rata_annua = 0
    
    # Reddito netto post mutuo
    reddito_netto_post_mutuo = reddito_netto - rata_annua
    
    # Calcolo ROI
    investimento_totale = prezzo_acquisto + spese_annual + imposte_annual
    ritorno_annuo = reddito_netto_post_mutuo + (prezzo_acquisto * (1 + rivalutazione_annua) - prezzo_acquisto) / durata_mutuo
    
    roi = (ritorno_annuo / investimento_totale) * 100  # ROI in percentuale
    return roi, reddito_netto_post_mutuo, rata_annua

# Funzione per calcolare ROI affitto (breve vs lungo termine)
def calcola_roi_affitto(prezzo_acquisto, canone_annuo, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, tipo_affitto="lungo", rivalutazione_annua=0.02):
    if tipo_affitto == "lungo":
        # Affitto lungo termine: reddito da affitto per 12 mesi
        reddito_annuo_affitto = canone_annuo - spese_annual - imposte_annual
    else:
        # Affitto breve termine (ad esempio, 30 giorni al mese)
        reddito_annuo_affitto = (canone_annuo * 0.7) - spese_annual - imposte_annual  # Sconto del 30% per turnover e gestione affitto breve

    # Se c'è un mutuo, calcoliamo la rata annuale
    if mutuo > 0:
        rata_annua = mutuo * (tasso_mutuo / 100) * (1 + tasso_mutuo / 100)**durata_mutuo / ((1 + tasso_mutuo / 100)**durata_mutuo - 1)
    else:
        rata_annua = 0

    # Reddito netto post mutuo
    reddito_netto_post_mutuo = reddito_annuo_affitto - rata_annua

    # Calcolo ROI per affitto (netto delle spese)
    investimento_totale = prezzo_acquisto + spese_annual + imposte_annual
    ritorno_annuo_affitto = reddito_netto_post_mutuo + (prezzo_acquisto * (1 + rivalutazione_annua) - prezzo_acquisto) / durata_mutuo
    
    roi_affitto = (ritorno_annuo_affitto / investimento_totale) * 100
    return roi_affitto, reddito_netto_post_mutuo, rata_annua

# Interfaccia Streamlit
st.title("Analisi Investimento Immobiliare a Milano")

# Parametri di input
prezzo_acquisto = st.number_input("Prezzo di acquisto dell'immobile (€):", min_value=50000, max_value=5000000, step=10000, value=300000)
canone_annuo = st.number_input("Canone di affitto annuale (€):", min_value=0, step=100, value=12000)
spese_annual = st.number_input("Spese annuali di gestione (assicurazione, manutenzione, ecc.): (€)", min_value=0, step=100, value=2000)
imposte_annual = st.number_input("Imposte annuali (cedolare secca, IMU, ecc.): (€)", min_value=0, step=100, value=1500)
mutuo = st.number_input("Importo mutuo (€):", min_value=0, max_value=prezzo_acquisto, step=10000, value=200000)
durata_mutuo = st.number_input("Durata del mutuo (anni):", min_value=5, max_value=30, step=1, value=20)
tasso_mutuo = st.number_input("Tasso di interesse mutuo (%):", min_value=0.1, max_value=10.0, step=0.1, value=3.0)
rivalutazione_annua = st.number_input("Rivalutazione annua dell'immobile (%):", min_value=0.0, max_value=10.0, step=0.1, value=2.0)

# Tipo di affitto
tipo_affitto = st.selectbox("Tipo di affitto:", ("Lungo", "Breve"))

# Calcolo ROI per acquisto e affitto
roi_acquisto, reddito_netto_post_mutuo_acquisto, rata_annua_acquisto = calcola_roi_acquisto(prezzo_acquisto, canone_annuo, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, rivalutazione_annua)
roi_affitto, reddito_netto_post_mutuo_affitto, rata_annua_affitto = calcola_roi_affitto(prezzo_acquisto, canone_annuo, spese_annual, imposte_annual, mutuo, durata_mutuo, tasso_mutuo, tipo_affitto.lower(), rivalutazione_annua)

# Visualizzazione dei risultati
st.subheader("Risultati ROI e Dettagli:")
st.write(f"**ROI per Acquisto Immobiliare**: {roi_acquisto:.2f}% annuo")
st.write(f"**ROI per Affitto ({tipo_affitto} Termine)**: {roi_affitto:.2f}% annuo")

# Confronto tra ROI Acquisto vs Affitto
if roi_acquisto > roi_affitto:
    st.write("L'acquisto dell'immobile è più vantaggioso rispetto all'affitto.")
else:
    st.write("L'affitto risulta più vantaggioso rispetto all'acquisto dell'immobile.")

# Dettaglio della rata annuale del mutuo
if mutuo > 0:
    st.write(f"**Rata annuale mutuo (Acquisto)**: {rata_annua_acquisto:.2f} €")
    st.write(f"**Rata annuale mutuo (Affitto)**: {rata_annua_affitto:.2f} €")

# Dettaglio delle spese di gestione e imposte
st.write(f"**Spese annuali di gestione**: {spese_annual:.2f} €")
st.write(f"**Imposte annuali**: {imposte_annual:.2f} €")

# Dettaglio del reddito netto post mutuo
st.write(f"**Reddito netto post mutuo (Acquisto)**: {reddito_netto_post_mutuo_acquisto:.2f} €")
st.write(f"**Reddito netto post mutuo (Affitto {tipo_affitto} Termine)**: {reddito_netto_post_mutuo_affitto:.2f} €")
