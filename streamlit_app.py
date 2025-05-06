import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funzione per calcolare ROI
def calcola_roi(entrate_annue, prezzo_acquisto, spese_iniziali, anni):
    investimento_totale = prezzo_acquisto + spese_iniziali
    ritorno_totale = entrate_annue * anni + valore_finale - investimento_totale
    return ritorno_totale / investimento_totale * 100  # ROI in %

# Funzione per il calcolo delle entrate e del ROI
def calcola():
    try:
        # Recupero dei dati inseriti
        prezzo_acquisto = float(entry_acquisto.get())
        spese_iniziali = float(entry_spese.get())
        costi_operativi_mensili = float(entry_costi.get())
        occupazione_media_breve_termine = float(entry_occupazione.get())
        tariffa_per_notte = float(entry_tariffa.get())
        affitto_mensile_lungo_termine = float(entry_affitto.get())
        anni = int(entry_anni.get())
        tasso_apprezzamento = float(entry_apprezzamento.get()) / 100
        inflazione = float(entry_inflazione.get()) / 100
        
        # Calcolo per affitto breve termine
        occupazione_annua_breve = occupazione_media_breve_termine * 365  # giorni di occupazione annua
        entrate_annue_breve = occupazione_annua_breve * tariffa_per_notte  # entrate annue da affitto breve
        entrate_annue_breve -= costi_operativi_mensili * 12  # Sottrai i costi operativi annuali

        # Calcolo per affitto lungo termine
        entrate_annue_lungo = affitto_mensile_lungo_termine * 12  # entrate annue da affitto lungo termine
        entrate_annue_lungo -= costi_operativi_mensili * 12  # Sottrai i costi operativi annuali

        # Calcolo dell'apprezzamento dell'immobile
        valore_finale_breve = prezzo_acquisto * ((1 + tasso_apprezzamento) ** anni)
        valore_finale_lungo = prezzo_acquisto * ((1 + tasso_apprezzamento) ** anni)

        # Calcolo del ROI per entrambi gli scenari
        roi_breve = calcola_roi(entrate_annue_breve, prezzo_acquisto, spese_iniziali, anni)
        roi_lungo = calcola_roi(entrate_annue_lungo, prezzo_acquisto, spese_iniziali, anni)
        
        # Visualizzazione dei risultati nel testo
        risultato_1.config(text=f"ROI Affitto Breve Termine: {roi_breve:.2f}%")
        risultato_2.config(text=f"ROI Affitto Lungo Termine: {roi_lungo:.2f}%")

        # Grafico
        anni_array = np.arange(1, anni + 1)
        entrate_breve_array = [entrate_annue_breve * anno for anno in anni_array]
        entrate_lungo_array = [entrate_annue_lungo * anno for anno in anni_array]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(anni_array, entrate_breve_array, label="Affitto Breve Termine", color='blue')
        ax.plot(anni_array, entrate_lungo_array, label="Affitto Lungo Termine", color='green')
        ax.set_xlabel("Anni")
        ax.set_ylabel("Entrate cumulative (€)")
        ax.set_title("Comparazione tra Affitto Breve e Lungo Termine")
        ax.legend()
        ax.grid(True)

        # Aggiunta del grafico alla GUI
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except ValueError:
        messagebox.showerror("Errore", "Per favore, inserisci solo valori numerici validi!")

# Creazione della finestra principale
root = tk.Tk()
root.title("Comparazione Affitto Breve e Lungo Termine")
root.geometry("800x600")

# Frame per i parametri di input
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10, fill=tk.X)

tk.Label(frame_input, text="Prezzo di acquisto (€):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_acquisto = tk.Entry(frame_input)
entry_acquisto.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Spese iniziali (€):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_spese = tk.Entry(frame_input)
entry_spese.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Costi operativi mensili (€):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_costi = tk.Entry(frame_input)
entry_costi.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Occupazione media (0-1) per affitto breve:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_occupazione = tk.Entry(frame_input)
entry_occupazione.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Tariffa per notte (€):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_tariffa = tk.Entry(frame_input)
entry_tariffa.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Affitto mensile lungo termine (€):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
entry_affitto = tk.Entry(frame_input)
entry_affitto.grid(row=5, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Numero di anni:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
entry_anni = tk.Entry(frame_input)
entry_anni.grid(row=6, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Tasso di apprezzamento (%):").grid(row=7, column=0, sticky="e", padx=5, pady=5)
entry_apprezzamento = tk.Entry(frame_input)
entry_apprezzamento.grid(row=7, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Tasso di inflazione (%):").grid(row=8, column=0, sticky="e", padx=5, pady=5)
entry_inflazione = tk.Entry(frame_input)
entry_inflazione.grid(row=8, column=1, padx=5, pady=5)

# Pulsante per calcolare
button_calcola = tk.Button(root, text="Calcola", command=calcola)
button_calcola.pack(pady=20)

# Risultati
frame_risultati = tk.Frame(root)
frame_risultati.pack(pady=10)

risultato_1 = tk.Label(frame_risultati, text="ROI Affitto Breve Termine: -")
risultato_1.pack()

risultato_2 = tk.Label(frame_risultati, text="ROI Affitto Lungo Termine: -")
risultato_2.pack()

# Frame per il grafico
frame_grafico = tk.Frame(root)
frame_grafico.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Avvio della GUI
root.mainloop()
