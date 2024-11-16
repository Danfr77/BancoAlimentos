import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Crear un DataFrame en memoria para almacenar la información
# (En un entorno real, esto se conectaría a una base de datos)
if "users_data" not in st.session_state:
    st.session_state["users_data"] = pd.DataFrame(columns=["Nombre", "Correo", "Fecha de Registro"])

# Menú de navegación en la barra lateral
st.sidebar.title("Menú de Navegación")
menu = st.sidebar.radio("Ir a:", ["Registrar Usuario", "Consultar Usuarios", "Generar Alertas"])

# 1. Registrar información de usuarios
if menu == "Registrar Usuario":
    st.title("Registro de Usuarios")
    with st.form("form_registro"):
        nombre = st.text_input("Nombre:")
        correo = st.text_input("Correo:")
        fecha_registro = st.date_input("Fecha de registro:", value=datetime.today())
        
        # Botón de envío
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            if nombre and correo:
                nuevo_usuario = {"Nombre": nombre, "Correo": correo, "Fecha de Registro": fecha_registro}
                st.session_state["users_data"] = pd.concat(
                    [st.session_state["users_data"], pd.DataFrame([nuevo_usuario])],
                    ignore_index=True
                )
                st.success(f"Usuario {nombre} registrado exitosamente.")
            else:
                st.error("Por favor, completa todos los campos.")

# 2. Consultar información de usuarios
elif menu == "Consultar Usuarios":
    st.title("Consulta de Usuarios")
    
    if st.session_state["users_data"].empty:
        st.warning("No hay usuarios registrados.")
    else:
        st.dataframe(st.session_state["users_data"])
        st.download_button(
            "Descargar datos",
            st.session_state["users_data"].to_csv(index=False),
            file_name="usuarios_registrados.csv",
            mime="text/csv",
        )

# 3. Generar alertas de fechas
elif menu == "Generar Alertas":
    st.title("Generador de Alertas por Fechas")
    
    if st.session_state["users_data"].empty:
        st.warning("No hay usuarios registrados.")
    else:
        dias_alerta = st.number_input("Días para generar alerta:", min_value=1, value=7)
        fecha_limite = datetime.today() - timedelta(days=dias_alerta)
        usuarios_alerta = st.session_state["users_data"][
            st.session_state["users_data"]["Fecha de Registro"] <= fecha_limite
        ]
        
        if usuarios_alerta.empty:
            st.info("No hay usuarios con fechas de alerta.")
        else:
            st.warning(f"Usuarios registrados hace más de {dias_alerta} días:")
            st.dataframe(usuarios_alerta)
