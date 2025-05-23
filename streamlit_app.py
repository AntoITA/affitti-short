import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm
from scipy.optimize import brentq

st.title("Superficie di Volatilità Implicita - Opzioni")

# Input generali
S0 = st.number_input("Prezzo attuale dell'azione (S0)", value=100.0)
r = st.number_input("Tasso risk-free (decimale)", value=0.01)

st.markdown("### Inserisci i dati delle opzioni")
num_opzioni = st.number_input("Numero di opzioni", min_value=1, max_value=50, value=5)

strike_list = []
maturity_list = []
option_price_list = []

for i in range(num_opzioni):
    st.markdown(f"**Opzione {i+1}**")
    strike = st.number_input(f"Strike price (K) {i+1}", key=f"strike_{i}", value=100.0 + i * 5)
    maturity = st.number_input(f"Tempo alla scadenza (anni) {i+1}", key=f"maturity_{i}", value=0.5 + i * 0.1)
    price = st.number_input(f"Prezzo dell'opzione {i+1}", key=f"price_{i}", value=5.0 + i)

    strike_list.append(strike)
    maturity_list.append(maturity)
    option_price_list.append(price)

# Calcolo della volatilità implicita
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

def implied_volatility(S, K, T, r, market_price):
    try:
        iv = brentq(lambda sigma: black_scholes_call(S, K, T, r, sigma) - market_price, 1e-6, 5.0)
        return iv
    except:
        return np.nan

vol_surface = np.array([implied_volatility(S0, K, T, r, P) for K, T, P in zip(strike_list, maturity_list, option_price_list)])

# Visualizzazione superficie
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(strike_list, maturity_list, vol_surface, c=vol_surface, cmap='viridis')
ax.set_title("Superficie di Volatilità Implicita")
ax.set_xlabel("Strike")
ax.set_ylabel("Maturity (anni)")
ax.set_zlabel("Volatilità Implicita")
st.pyplot(fig)
