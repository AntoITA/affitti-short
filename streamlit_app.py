import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Funzione per calcolare l'utile netto per ogni anno
def calcola_utile_annuale(prezzo_acquisto, costi_ristrutturazione, licenze_permessi, marketing_iniziale,
                          tasso_occupazione, prezzo_media_night_alta, prezzo_media_night_bassa,
                          costi_operativi, commissioni_piattaforme, utenze, pulizie, manutenzione,
                          tassa_soggiorno, costi_iniziali, arredo_ristrutturazione, spese_notarili):
    # Calcoliamo il numero di notti occupate
    notti_occupate = 365 * tasso_occupazione / 100

    # Prezzo medio per notte considerando la media tra alta e bassa stagione
    prezzo_media_night = (prezzo_media_night_alta + prezzo_media_night_bassa) / 2

    # Ricavi lordi
    ricavi_lordi = notti_occupate * prezzo_media_night

    # Commissioni piattaforma
    commissioni = ricavi_lordi * (commissioni_piattaforme / 100)

    # Ricavi netti
    ricavi_netti = ricavi_lordi - commissioni

    # Costi fissi mensili
    costi_fissi_mensili = utenze + pulizie + manutenzione + tassa_soggiorno + costi_operativi

    # Costi annuali
    costi_annuali = costi_fissi_mensili * 12

    # Calcoliamo il cash flow mensile e annuo
    cash_flow_annuo = ricavi_netti - costi_annuali

    # Rendimento netto annuale (ROI)
    investimento_totale = prezzo_acquisto + arredo_ristrutturazione + spese_notarili
    rendimento_netto = (cash_flow_annuo / investimento_totale) * 100

    # Payback period
    payback_period = investimento_totale / cash_flow_annuo

    # IRR semplificato (approssimazione)
    irr = (cash_flow_annuo / investimento_totale) * 100

    return ricavi_lordi, commissioni, ricavi_netti, costi_annuali, cash_flow_annuo, rendimento_netto, payback_period, irr

# Interfaccia utente per Streamlit
st.title("Calcolatore di Investimento Immobiliare per Affitti Brevi")

# Input variabili
prezzo_acquisto = st.number_input("Prezzo di Acquisto (€)", min_value=10000, value=200000)
costi_ristrutturazione = st.number_input("Costi di Ristrutturazione (€)", min_value=0, value=15000)
licenze_permessi = st.number_input("Costi Licenze e Permessi (€)", min_value=0, value=5000)
marketing_iniziale = st.number_input("Costi di Marketing Iniziale (€)", min_value=0, value=3000)

# Dati di affitto
tasso_occupazione = st.slider("Tasso di Occupazione (%)", 0, 100, 50)
prezzo_media_night_alta = st.number_input("Prezzo per Notte (Alta Stagione) (€)", min_value=10, value=100)
prezzo_media_night_bassa = st.number_input("Prezzo per Notte (Bassa Stagione) (€)", min_value=10, value=70)

# Costi mensili
utenze = st.number_input("Utenze (Luce/Gas/Internet) (€)", min_value=0, value=150)
pulizie = st.number_input("Costi di Pulizia Mensili (€)", min_value=0, value=100)
manutenzione = st.number_input("Manutenzione Media Mensile (€)", min_value=0, value=50)
tassa_soggiorno = st.number_input("Tassa Soggiorno/Gestione Amministrativa (€)", min_value=0, value=30)
costi_operativi = st.number_input("Altri Costi Operativi Mensili (€)", min_value=0, value=100)

# Costi una tantum
arredo_ristrutturazione = st.number_input("Costi di Arredo/Ristrutturazione (€)", min_value=0, value=10000)
spese_notarili = st.number_input("Spese Notarili/di Agenzia (€)", min_value=0, value=1500)

# Commissioni piattaforme
commissioni_piattaforme = st.slider("Commissioni Piattaforme (%)", 0, 30, 15)

# Calcolo dei risultati
ricavi_lordi, commissioni, ricavi_netti, costi_annuali, cash_flow_annuo, rendimento_netto, payback_period, irr = calcola_utile_annuale(
    prezzo_acquisto, costi_ristrutturazione, licenze_permessi, marketing_iniziale,
    tasso_occupazione, prezzo_media_night_alta, prezzo_media_night_bassa,
    costi_operativi, commissioni_piattaforme, utenze, pulizie, manutenzione,
    tassa_soggiorno, arredo_ristrutturazione, spese_notarili
)

# Visualizzazione dei risultati
st.subheader("Risultati Finanziari")
st.write(f"**Ricavi Lordi Annuali:** €{ricavi_lordi:,.2f}")
st.write(f"**Commissioni Piattaforme:** €{commissioni:,.2f}")
st.write(f"**Ricavi Netti Annuali:** €{ricavi_netti:,.2f}")
st.write(f"**Costi Annuali Totali (Fissi e Operativi):** €{costi_annuali:,.2f}")
st.write(f"**Cash Flow Annuo:** €{cash_flow_annuo:,.2f}")
st.write(f"**Rendimento Netto (ROI):** {rendimento_netto:,.2f}%")
st.write(f"**Payback Period:** {payback_period:,.2f} anni")
st.write(f"**IRR (approssimato):** {irr:,.2f}%")

# Grafico dei Ricavi vs Costi
fig, ax = plt.subplots()
categorie = ['Ricavi Netti', 'Costi Operativi', 'Commissioni Piattaforme']
valori = [ricavi_netti, costi_annuali, commissioni]
ax.bar(categorie, valori, color=['green', 'red', 'blue'])
ax.set_title('Confronto tra Ricavi e Costi')
ax.set_ylabel('€')

st.pyplot(fig)

# Grafico del Cash Flow e Payback Period
fig2, ax2 = plt.subplots()
anni = np.arange(1, int(payback_period)+1)
cash_flow = np.full_like(anni, cash_flow_annuo)
ax2.plot(anni, cash_flow, label="Cash Flow Annuo", color='green')
ax2.axhline(0, color='black',linewidth=1)
ax2.set_title('Cash Flow Annuale e Payback Period')
ax2.set_xlabel('Anno')
ax2.set_ylabel('Cash Flow (€)')
ax2.legend()

st.pyplot(fig2)

