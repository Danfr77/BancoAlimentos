import streamlit as st
import pandas as pd
import numpy as np

# Título de la aplicación
st.title("Simulador de Acciones")

# Entrada del usuario
capital_inicial = st.number_input("Capital inicial ($):", min_value=100.0, step=100.0)
rendimiento_anual = st.slider("Rendimiento anual (%)", 0, 20, 5)

# Simulación simple
años = st.slider("Número de años:", 1, 50, 10)
capital_final = capital_inicial * (1 + rendimiento_anual / 100) ** años

# Resultado
st.write(f"El capital final después de {años} años es: **${capital_final:,.2f}**")