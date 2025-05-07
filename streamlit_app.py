import streamlit as st
import matplotlib.pyplot as plt

# 📘 Dati iniziali di acquisto e spese generiche
st.set_page_config(page_title="Calcolo Affitto", layout="wide")
st.title("🏡 Calcolo Affitto - Breve vs Lungo")
st.markdown("In questa app puoi calcolare il profitto derivante dall'affitto breve e lungo.")

# 📚 Sezione Dati di acquisto e spese generali
st.header("🔹 Dati di acquisto e spese generali")

# Inserimento del prezzo d'acquisto iniziale
prezzo_acquisto = st.number_input("Prezzo di acquisto iniziale (€)", min_value=0.0, value=150000.0)

# Inserimento del mutuo, con spunta per calcolare il mutuo
mutuo_attivo = st.checkbox("Attiva calcolo mutuo")
if mutuo_attivo:
    importo_mutuo = st.number_input("Importo del mutuo (€)", min_value=0.0, value=100000.0)
    durata_mutuo = st.number_input("Durata del mutuo (anni)", min_value=1, value=20)
    tasso_interesse = st.number_input("Tasso di interesse del mutuo (%)", min_value=0.0, value=2.5)
else:
    importo_mutuo = 0.0
    durata_mutuo = 0
    tasso_interesse = 0.0

# 📊 Sezione Spese fisse mensili
st.header("🔹 Spese fisse e tasse")
spese_fisse = {}
spese_fisse["Condominio"] = st.number_input("Spese condominiali mensili (€)", min_value=0.0, value=100.0)
spese_fisse["Manutenzione ordinaria"] = st.number_input("Manutenzione ordinaria mensile (€)", min_value=0.0, value=50.0)
spese_fisse["IMU / Tasse"] = st.number_input("Tasse (IMU ecc.) mensili (€)", min_value=0.0, value=100.0)
tasse_mensili = st.slider("Aliquota tasse affitto (%)", 0.0, 30.0, 21.0)

# 📘 Affitto breve vs lungo
st.header("🔹 Dettagli affitto breve e lungo")

# Seleziona tipo di affitto
affitto_breve = st.checkbox("Affitto breve attivo")
affitto_lungo = st.checkbox("Affitto lungo attivo")

# Costi di gestione per affitto breve
spese_gestione_breve = {}
if affitto_breve:
    canone_breve = st.number_input("Canone affitto breve mensile (€)", min_value=0.0, value=1000.0)
    spese_gestione_breve["Costi di gestione"] = st.number_input("Costi di gestione affitto breve mensili (€)", min_value=0.0, value=200.0)
    commissioni_perc = st.number_input("Commissioni piattaforma (%)", min_value=0.0, value=15.0) / 100
    commissioni_piattaforma = commissioni_perc * canone_breve
    spese_gestione_breve["Commissioni piattaforma"] = commissioni_piattaforma
    spese_gestione_breve["Pulizia lenzuola e biancheria"] = st.number_input("Pulizia lenzuola e biancheria mensile (€)", min_value=0.0, value=50.0)
    spese_gestione_breve["Manutenzione straordinaria"] = st.number_input("Manutenzione straordinaria mensile (€)", min_value=0.0, value=100.0)

# Costi di gestione per affitto lungo
spese_gestione_lungo = {}
if affitto_lungo:
    canone_lungo = st.number_input("Canone affitto lungo mensile (€)", min_value=0.0, value=900.0)
    spese_gestione_lungo["Costi di gestione"] = st.number_input("Costi di gestione affitto lungo mensili (€)", min_value=0.0, value=50.0)

# 📘 Calcolo ROI
st.header("📈 Calcolo ROI")

# Calcolo profitto mensile
profitto_breve_mensile = 0.0
profitto_lungo_mensile = 0.0
if affitto_breve:
    profitto_breve_mensile = canone_breve - sum(spese_fisse.values()) - sum(spese_gestione_breve.values())
    profitto_breve_annuo = profitto_breve_mensile * 12
else:
    profitto_breve_annuo = 0.0

if affitto_lungo:
    profitto_lungo_mensile = canone_lungo - sum(spese_fisse.values()) - sum(spese_gestione_lungo.values())
    profitto_lungo_annuo = profitto_lungo_mensile * 12
else:
    profitto_lungo_annuo = 0.0

# Dati per calcolare ROI e Payback
totale_investimento_iniziale = prezzo_acquisto + importo_mutuo
roi_breve = (profitto_breve_annuo / totale_investimento_iniziale) * 100 if totale_investimento_iniziale > 0 else 0
roi_lungo = (profitto_lungo_annuo / totale_investimento_iniziale) * 100 if totale_investimento_iniziale > 0 else 0
payback_breve = totale_investimento_iniziale / profitto_breve_annuo if profitto_breve_annuo > 0 else float('inf')
payback_lungo = totale_investimento_iniziale / profitto_lungo_annuo if profitto_lungo_annuo > 0 else float('inf')

# Visualizzazione grafica
col1, col2 = st.columns(2)

col1.metric("ROI annuo affitto breve", f"{roi_breve:.2f}%")
col1.metric("Payback affitto breve", f"{payback_breve:.1f} anni" if payback_breve != float('inf') else "N/D")
col2.metric("ROI annuo affitto lungo", f"{roi_lungo:.2f}%")
col2.metric("Payback affitto lungo", f"{payback_lungo:.1f} anni" if payback_lungo != float('inf') else "N/D")

# Grafico ROI
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(["Affitto breve", "Affitto lungo"], [roi_breve, roi_lungo], color=['#FF5733', '#33B5FF'])
ax.set_title("Confronto ROI Annui")
ax.set_ylabel("ROI (%)")
st.pyplot(fig)

# Grafico Payback Period
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(["Affitto breve", "Affitto lungo"], [payback_breve, payback_lungo], color=['#FF5733', '#33B5FF'])
ax.set_title("Confronto Payback Period")
ax.set_ylabel("Anni")
st.pyplot(fig)

# Visualizzazione finale
if affitto_breve or affitto_lungo:
    st.write(f"Profitto mensile affitto breve: € {profitto_breve_mensile:.2f}")
    st.write(f"Profitto mensile affitto lungo: € {profitto_lungo_mensile:.2f}")
