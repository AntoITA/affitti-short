import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Impostazioni pagina

st.set\_page\_config(page\_title="Analisi Redditività Affitto", layout="wide")
st.title("📊 Dashboard Affitto Breve vs Lungo Periodo - Redditività Immobiliare")

# 🏠 Dati di acquisto e investimento iniziale

st.header("🏠 Dati di acquisto e investimento iniziale")
col1, col2 = st.columns(2)
with col1:
prezzo\_acquisto = st.number\_input("Prezzo di acquisto immobile (€)", min\_value=0.0, value=100000.0)
spese\_notarili = st.number\_input("Spese notarili / agenzia (€)", min\_value=0.0, value=3000.0)
with col2:
ristrutturazione = st.number\_input("Ristrutturazione / Arredo (€)", min\_value=0.0, value=8000.0)
altre\_spese = st.number\_input("Altre spese iniziali (€)", min\_value=0.0, value=1000.0)

totale\_investimento\_iniziale = prezzo\_acquisto + spese\_notarili + ristrutturazione + altre\_spese

# 📈 Entrate previste

st.header("📈 Entrate previste")
col1, col2, col3 = st.columns(3)
with col1:
prezzo\_notte = st.number\_input("Prezzo medio per notte (€)", min\_value=0.0, value=90.0)
with col2:
occupazione = st.slider("Occupazione media (%)", 0, 100, 70)
with col3:
notti\_affittabili = st.number\_input("Notti affittabili al mese", min\_value=0, max\_value=31, value=25)

ricavo\_lordo\_mensile = prezzo\_notte \* (occupazione / 100) \* notti\_affittabili
st.metric("Ricavo lordo stimato mensile", f"€ {ricavo\_lordo\_mensile:,.2f}")

# 💸 Costi fissi mensili

st.header("💸 Costi fissi mensili")
costi\_fissi = {}
costi\_fissi\['Condominio'] = st.number\_input("Condominio (€)", min\_value=0.0, value=100.0)
costi\_fissi\['Utenze (luce/gas/internet)'] = st.number\_input("Utenze (€)", min\_value=0.0, value=120.0)
costi\_fissi\['Pulizie'] = st.number\_input("Pulizie (€)", min\_value=0.0, value=100.0)
costi\_fissi\['Commissioni piattaforme'] = st.number\_input("Commissioni piattaforme (€)", min\_value=0.0, value=80.0)
costi\_fissi\['Manutenzione'] = st.number\_input("Manutenzione media (€)", min\_value=0.0, value=50.0)
costi\_fissi\['Tassa soggiorno / gestione'] = st.number\_input("Tassa soggiorno / gestione (€)", min\_value=0.0, value=30.0)

totale\_costi\_fissi = sum(costi\_fissi.values())

# 💰 Mutuo (opzionale)

inserisci\_mutuo = st.checkbox("Considera Mutuo nei calcoli")
if inserisci\_mutuo:
st.header("💰 Dati Mutuo")
importo\_mutuo = st.number\_input("Importo del mutuo (€)", min\_value=0.0, value=70000.0)
durata\_mutuo = st.number\_input("Durata del mutuo (anni)", min\_value=5, max\_value=30, value=20)
tasso\_mutuo = st.number\_input("Tasso d'interesse annuale (%)", min\_value=0.0, max\_value=10.0, value=3.5)
rata\_mutuo = (importo\_mutuo \* tasso\_mutuo / 100) / 12  # Calcolo semplificato del mutuo (senza ammortamento complesso)
st.metric("Rata mensile mutuo", f"€ {rata\_mutuo:,.2f}")
else:
rata\_mutuo = 0

# Calcoli principali

profitto\_mensile = ricavo\_lordo\_mensile - totale\_costi\_fissi - rata\_mutuo
profitto\_annuo = profitto\_mensile \* 12
roi = (profitto\_annuo / totale\_investimento\_iniziale \* 100) if totale\_investimento\_iniziale > 0 else 0
payback = (totale\_investimento\_iniziale / profitto\_annuo) if profitto\_annuo > 0 else float('inf')

# 📊 Indicatori di redditività

st.header("📊 Indicatori di redditività")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI annuo (%)", f"{roi:.2f}%")
col2.metric("Payback period (anni)", f"{payback:.1f}" if payback != float('inf') else "N/D")
col3.metric("Cash flow mensile", f"€ {profitto\_mensile:,.2f}")
col4.metric("Cash flow annuo", f"€ {profitto\_annuo:,.2f}")

# 📉 Grafico entrate e costi mensili

st.header("📉 Grafico entrate e costi mensili")
data = pd.DataFrame({
'Categoria': \['Entrate', 'Costi fissi', 'Mutuo', 'Profitto netto'],
'Euro': \[ricavo\_lordo\_mensile, totale\_costi\_fissi, rata\_mutuo, profitto\_mensile]
})
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(data\['Categoria'], data\['Euro'], color=\['green', 'red', 'purple', 'blue'])
ax.set\_ylabel('€')
ax.set\_title('Confronto entrate, costi e mutuo mensili')
st.pyplot(fig)

# 📈 Link calcolo mutuo

st.subheader("🔗 Calcolo mutuo e spese notarili")
st.markdown("[Clicca qui per calcolare mutuo e spese notarili](https://www.mutuisupermarket.it/calcolo-mutuo/calcolo-spese-acquisto-casa)")

# 💼 Opzione per comparare affitto breve e lungo termine

st.header("💼 Confronto Affitto Breve vs Lungo Periodo")
affitto\_lungo\_termine = st.checkbox("Considera Affitto Lungo Periodo", value=False)

if affitto\_lungo\_termine:
\# Dati per affitto lungo periodo (ad esempio, contratto 12 mesi)
canone\_mensile\_lungo = st.number\_input("Canone mensile affitto lungo periodo (€)", min\_value=0.0, value=500.0)
durata\_contratto = st.number\_input("Durata del contratto (anni)", min\_value=1, value=1)

```
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
```

# ⬇️ Esporta dati

st.header("⬇️ Esporta dati")
dati\_export = {
'Prezzo medio per notte': prezzo\_notte,
'Occupazione media (%)': occupazione,
'Notti affittabili': notti\_affittabili,
'Ricavo lordo mensile': ricavo\_lordo\_mensile,
'Totale costi fissi': totale\_costi\_fissi,
'Totale investimento iniziale': totale\_investimento\_iniziale,
'Profitto mensile': profitto\_mensile,
'Profitto annuo': profitto\_annuo,
'ROI annuo (%)': roi,
'Payback (anni)': payback,
'Affitto lungo periodo ROI (%)': roi\_lungo if affitto\_lungo\_termine else None,
'Affitto lungo periodo Payback (anni)': payback\_lungo if affitto\_lungo\_termine else None
}
df\_export = pd.DataFrame(dati\_export.items(), columns=\['Voce', 'Valore'])
csv = df\_export.to\_csv(index=False).encode('utf-8')
st.download\_button(
label="Scarica dati in CSV",
data=csv,
file\_name='report\_affitto.csv',
mime='text/csv'
)
# Titolo
st.title("📍 Mappa rendimenti affitti a Milano 2024")
st.markdown("Fonte: *Immobiliare.it - aprile 2024*")

# Dati
data = [
    ["Centrale", 4.2, "Alta", 2.1, "Bassa"],
    ["Isola-Garibaldi", 4.0, "Alta", 2.3, "Bassa"],
    ["Brera-Montenapoleone", 3.9, "Alta", 2.4, "Bassa"],
    ["Porta Romana", 4.1, "Alta", 2.6, "Media"],
    ["Buenos Aires", 4.0, "Alta", 2.7, "Media"],
    ["Navigli", 3.8, "Alta", 2.8, "Media"],
    ["Città Studi", 3.7, "Alta", 2.9, "Media"],
    ["Bicocca", 3.4, "Media", 2.6, "Media"],
    ["Lambrate", 3.3, "Media", 2.7, "Media"],
    ["Fiera-San Siro", 3.2, "Media", 2.8, "Media"],
    ["Affori-Bovisa", 3.1, "Media", 2.7, "Media"],
    ["Corvetto", 3.2, "Media", 2.9, "Media"],
    ["Bande Nere", 3.0, "Media", 2.8, "Media"],
    ["Forlanini", 2.9, "Bassa", 2.7, "Media"],
    ["Baggio", 2.8, "Bassa", 2.7, "Media"],
    ["Vigentino", 2.9, "Bassa", 2.8, "Media"],
    ["Quarto Oggiaro", 2.6, "Bassa", 2.7, "Media"],
    ["Gratosoglio", 2.5, "Bassa", 2.8, "Media"]
]

columns = ["Zona", "ROI Affitto Breve", "Redditività Breve", "ROI Affitto Lungo", "Redditività Lungo"]
df = pd.DataFrame(data, columns=columns)
df["Differenza ROI"] = df["ROI Affitto Breve"] - df["ROI Affitto Lungo"]

# Legenda
st.markdown("""
Legenda:
- 🟢 Alta: ROI ≥ 3,8%
- 🟡 Media: ROI 3,0% – 3,7%
- 🔴 Bassa: ROI < 3,0%
""")

# Mostra tabella
df_display = df.copy()
df_display["ROI Affitto Breve"] = df_display["ROI Affitto Breve"].map(lambda x: f"{x:.1f}%")
df_display["ROI Affitto Lungo"] = df_display["ROI Affitto Lungo"].map(lambda x: f"{x:.1f}%")
df_display["Differenza ROI"] = df["Differenza ROI"].map(lambda x: f"{x:+.1f}%")
st.dataframe(df_display.set_index("Zona"))

# Filtro interattivo
diff_threshold = st.slider("Filtra per differenza ROI (maggiore di):", min_value=-1.0, max_value=3.0, step=0.1, value=0.5)
df_filtered = df[df["Differenza ROI"] > diff_threshold]

# Grafico
if not df_filtered.empty:
    df_plot = df_filtered.melt(id_vars=["Zona"], value_vars=["ROI Affitto Breve", "ROI Affitto Lungo"], var_name="Tipo Affitto", value_name="ROI")
    fig = px.bar(df_plot, x="Zona", y="ROI", color="Tipo Affitto", barmode="group",
                 color_discrete_map={"ROI Affitto Breve": "green", "ROI Affitto Lungo": "red"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nessuna zona supera la soglia selezionata di differenza ROI.")

# Conclusione
st.markdown("""
💡 Le zone centrali e semicentrali mostrano una **chiara superiorità del ROI da affitto breve**,
mentre nelle zone periferiche la differenza è **molto ridotta o nulla**.
""")



# Footer

st.markdown("---")
st.caption("App creata con ❤️ usando Streamlit - Tutti i dati sono simulazioni modificabili")
