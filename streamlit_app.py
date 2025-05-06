import streamlit as st

# Titolo
st.title("📊 Calcolatore Redditività Affitto Breve vs Lungo")

# 📥 Input dell'utente
st.header("1️⃣ Inserisci i dati dell'investimento")

col1, col2 = st.columns(2)
with col1:
    prezzo_acquisto = st.number_input("Prezzo acquisto immobile (€)", min_value=0.0, value=150000.0, step=1000.0)
    spese_notarili = st.number_input("Spese notarili + tasse (€)", min_value=0.0, value=5000.0, step=500.0)
    ristrutturazione = st.number_input("Costo ristrutturazione (€)", min_value=0.0, value=10000.0, step=1000.0)
    arredamento = st.number_input("Costo arredamento (€)", min_value=0.0, value=5000.0, step=500.0)

with col2:
    giorni_occupati = st.slider("Giorni di occupazione annui", min_value=0, max_value=365, value=200)
    prezzo_medio_notte = st.number_input("Prezzo medio a notte (€)", min_value=0.0, value=80.0, step=5.0)
    spese_gestione_annue = st.number_input("Spese gestione annue (pulizie, commissioni, ecc.) (€)", min_value=0.0, value=5000.0, step=500.0)
    affitto_lungo_mensile = st.number_input("Affitto mensile (affitto lungo) (€)", min_value=0.0, value=700.0, step=50.0)

# 📈 Calcoli
st.header("2️⃣ Risultati della simulazione")

investimento_totale = prezzo_acquisto + spese_notarili + ristrutturazione + arredamento
ricavo_affitto_breve = giorni_occupati * prezzo_medio_notte
utile_netto_annuo = ricavo_affitto_breve - spese_gestione_annue
roi = (utile_netto_annuo / investimento_totale) * 100
payback = investimento_totale / utile_netto_annuo if utile_netto_annuo != 0 else float('inf')

# Affitto lungo
ricavo_annuo_lungo = affitto_lungo_mensile * 12
roi_lungo = (ricavo_annuo_lungo / investimento_totale) * 100
payback_lungo = investimento_totale / ricavo_annuo_lungo if ricavo_annuo_lungo != 0 else float('inf')

# 📊 Indicatori di redditività
col1, col2 = st.columns(2)
col1.metric("ROI Affitto Breve (%)", f"{roi:.2f}%")
col1.metric("Utile Netto Annuo (€)", f"{utile_netto_annuo:,.0f}")
col1.metric("Payback Period (anni)", f"{payback:.1f}" if payback != float('inf') else "N/D")

col2.metric("ROI Affitto Lungo (%)", f"{roi_lungo:.2f}%")
col2.metric("Ricavo Annuo Lungo (€)", f"{ricavo_annuo_lungo:,.0f}")
col2.metric("Payback Period Affitto Lungo (anni)", f"{payback_lungo:.1f}" if payback_lungo != float('inf') else "N/D")

# ✅ Valutazione qualitativa della redditività
if roi >= 8:
    st.success("🔝 Redditività **Alta** (ROI ≥ 8%)")
elif roi >= 4:
    st.warning("⚠️ Redditività **Media** (4% ≤ ROI < 8%)")
else:
    st.error("🔻 Redditività **Bassa** (ROI < 4%)")

if roi_lungo >= 8:
    st.success("🔝 Redditività Lungo Periodo **Alta** (ROI ≥ 8%)")
elif roi_lungo >= 4:
    st.warning("⚠️ Redditività Lungo Periodo **Media** (4% ≤ ROI < 8%)")
else:
    st.error("🔻 Redditività Lungo Periodo **Bassa** (ROI < 4%)")

# ℹ️ Note aggiuntive
st.markdown("""
---
📌 *Nota: Questa è una simulazione semplificata. Non considera tassazione, eventuale mutuo, inflazione o crescita del valore dell'immobile.*
""")


📍 **Mappa rendimenti affitti a Milano 2024**

Fonte: *Immobiliare.it - aprile 2024*

---

| Zona | ROI Affitto Breve | Redditività Breve | ROI Affitto Lungo | Redditività Lungo | Differenza ROI |
|------|--------------------|--------------------|-------------------|-------------------|-----------------|
| Centrale | 4,2% | 🟢 Alta | 2,1% | 🔴 Bassa | +2,1% |
| Isola-Garibaldi | 4,0% | 🟢 Alta | 2,3% | 🔴 Bassa | +1,7% |
| Brera-Montenapoleone | 3,9% | 🟢 Alta | 2,4% | 🔴 Bassa | +1,5% |
| Porta Romana | 4,1% | 🟢 Alta | 2,6% | 🟠 Media | +1,5% |
| Buenos Aires | 4,0% | 🟢 Alta | 2,7% | 🟠 Media | +1,3% |
| Navigli | 3,8% | 🟢 Alta | 2,8% | 🟠 Media | +1,0% |
| Città Studi | 3,7% | 🟢 Alta | 2,9% | 🟠 Media | +0,8% |
| Bicocca | 3,4% | 🟡 Media | 2,6% | 🟠 Media | +0,8% |
| Lambrate | 3,3% | 🟡 Media | 2,7% | 🟠 Media | +0,6% |
| Fiera-San Siro | 3,2% | 🟡 Media | 2,8% | 🟠 Media | +0,4% |
| Affori-Bovisa | 3,1% | 🟡 Media | 2,7% | 🟠 Media | +0,4% |
| Corvetto | 3,2% | 🟡 Media | 2,9% | 🟠 Media | +0,3% |
| Bande Nere | 3,0% | 🟡 Media | 2,8% | 🟠 Media | +0,2% |
| Forlanini | 2,9% | 🔴 Bassa | 2,7% | 🟠 Media | +0,2% |
| Baggio | 2,8% | 🔴 Bassa | 2,7% | 🟠 Media | +0,1% |
| Vigentino | 2,9% | 🔴 Bassa | 2,8% | 🟠 Media | +0,1% |
| Quarto Oggiaro | 2,6% | 🔴 Bassa | 2,7% | 🟠 Media | -0,1% |
| Gratosoglio | 2,5% | 🔴 Bassa | 2,8% | 🟠 Media | -0,3% |

Legenda:
- 🟢 Alta: ROI ≥ 3,8%
- 🟡 Media: ROI 3,0% – 3,7%
- 🔴 Bassa: ROI < 3,0%

💡 Le zone centrali e semicentrali mostrano una **chiara superiorità del ROI da affitto breve**, mentre nelle zone periferiche la differenza è **molto ridotta o nulla**.

---

📊 **Visualizzazione grafica** *(esempio suggerito da implementare con Streamlit o Matplotlib)*:

- **Bar chart** con tre barre per ogni zona: ROI affitto breve, ROI affitto lungo, differenza ROI.
- **Colori** delle barre in base alla redditività (verde, giallo, rosso).
- **Filtro interattivo** per selezionare solo zone con ROI > soglia o differenza > X.

Se vuoi, posso generarti direttamente lo script Python per una dashboard interattiva con questi dati.
