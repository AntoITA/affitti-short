import streamlit as st

# Funzione per calcolare la redditività dell'investimento
def calcola_redditivita(acquisto, ristrutturazione, affitto_mensile, utenze, pulizie_per_check, manutenzione, assicurazione, marketing_continuo, servizio_gestione, tasso_occupazione, prezzo_notte, commissione_piattaforma, anni):
    # Costi iniziali
    investimento_iniziale = acquisto + ristrutturazione + 2000 + 1500  # Licenze e marketing iniziali
    costi_fissi_annuali = (affitto_mensile * 12) + (utenze * 12) + (manutenzione * 12) + (assicurazione * 12) + (marketing_continuo * 12) + (servizio_gestione * 12)
    
    # Dati per ogni anno
    ricavi_netti = []
    costi_operativi = []
    flusso_cassa = []

    for anno in range(1, anni+1):
        # Calcolo ricavi e commissioni per anno
        notti_occupate = 365 * tasso_occupazione[anno-1]
        ricavi_lordi_annuali = notti_occupate * prezzo_notte
        commissione_annuale = ricavi_lordi_annuali * commissione_piattaforma
        ricavi_netto = ricavi_lordi_annuali - commissione_annuale
        
        # Costi pulizie per anno
        numero_prenotazioni = notti_occupate / 3  # Durata media del soggiorno 3 notti
        costo_pulizie_annuale = numero_prenotazioni * pulizie_per_check
        
        # Costi operativi totali
        costi_totali_annuali = costi_fissi_annuali + costo_pulizie_annuale
        
        # Calcolo utile operativo
        utile_operativo = ricavi_netto - costi_totali_annuali
        
        # Flusso di cassa
        if anno == 1:
            flusso_cassa_annuale = utile_operativo - investimento_iniziale
        else:
            flusso_cassa_annuale = utile_operativo
        
        # Aggiorniamo i risultati
        ricavi_netti.append(ricavi_netto)
        costi_operativi.append(costi_totali_annuali)
        flusso_cassa.append(flusso_cassa_annuale)
        
        # Aggiornamento per l'anno successivo
        tasso_occupazione[anno] += 0.05  # Incremento del 5% sul tasso di occupazione per ogni anno
        
    return ricavi_netti, costi_operativi, flusso_cassa, investimento_iniziale


# Streamlit UI
st.title("Valutazione Acquisto Immobile per Affitti Brevi a Milano")

# Parametri di input
acquisto = st.number_input("Prezzo di Acquisto dell'Immobili (€):", min_value=50000, max_value=1000000, value=250000)
ristrutturazione = st.number_input("Ristrutturazione e Arredamento (€):", min_value=0, max_value=100000, value=20000)
affitto_mensile = st.number_input("Canone di Affitto Mensile (€):", min_value=500, max_value=5000, value=1200)
utenze = st.number_input("Utenze Mensili (€):", min_value=50, max_value=1000, value=250)
pulizie_per_check = st.number_input("Costo Pulizie per Check-out (€):", min_value=10, max_value=100, value=30)
manutenzione = st.number_input("Manutenzione Ordinaria Mensile (€):", min_value=0, max_value=1000, value=100)
assicurazione = st.number_input("Assicurazione Mensile (€):", min_value=0, max_value=500, value=50)
marketing_continuo = st.number_input("Marketing Continuo Mensile (€):", min_value=0, max_value=1000, value=100)
servizio_gestione = st.number_input("Servizio di Gestione Mensile (€):", min_value=0, max_value=1000, value=200)

# Assunzioni di occupazione e prezzo per notte
tasso_occupazione = [0.5, 0.6, 0.65, 0.7, 0.75]  # Tasso di occupazione per ogni anno
prezzo_notte = st.number_input("Prezzo Medio per Notte (€):", min_value=50, max_value=500, value=125)
commissione_piattaforma = 0.15  # Commissione media piattaforme

# Calcolare la redditività
ricavi_netti, costi_operativi, flusso_cassa, investimento_iniziale = calcola_redditivita(
    acquisto, ristrutturazione, affitto_mensile, utenze, pulizie_per_check, manutenzione, assicurazione,
    marketing_continuo, servizio_gestione, tasso_occupazione, prezzo_notte, commissione_piattaforma, 5
)

# Visualizzare i risultati
st.subheader("Risultati Anno per Anno")

for anno in range(1, 6):
    st.write(f"**Anno {anno}:**")
    st.write(f" - Ricavi Netti: €{ricavi_netti[anno-1]:,.2f}")
    st.write(f" - Costi Operativi: €{costi_operativi[anno-1]:,.2f}")
    st.write(f" - Flusso di Cassa: €{flusso_cassa[anno-1]:,.2f}")

st.subheader("Investimento Iniziale")
st.write(f"Investimento Iniziale: €{investimento_iniziale:,.2f}")

# Grafico flusso di cassa
import matplotlib.pyplot as plt
plt.plot(range(1, 6), flusso_cassa, marker='o', color='blue', label="Flusso di Cassa Annuale")
plt.xlabel("Anno")
plt.ylabel("Flusso di Cassa (€)")
plt.title("Flusso di Cassa Annuale")
plt.grid(True)
st.pyplot(plt)

# Conclusione
if flusso_cassa[-1] > 0:
    st.success("L'investimento è redditizio a partire dal quarto anno.")
else:
    st.warning("L'investimento non risulta redditizio nei primi anni. Potresti considerare una riduzione dei costi o aumentare l'occupazione per migliorare i risultati.")
