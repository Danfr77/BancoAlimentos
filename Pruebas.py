import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Crear un DataFrame en memoria para almacenar la información
if "users_data" and "users2_data" not in st.session_state:
    st.session_state["users_data"] = pd.DataFrame(columns=["Alimento","Tipo", "Cantidad", "Fecha de recepción", "Fecha de caducidad", "Días para caducar"])
    st.session_state["users2_data"] = pd.DataFrame(columns=["Nombre", "Correo", "Necesidades"])

# Menú de navegación en la barra lateral
st.sidebar.title("Menú de Navegación")
menu = st.sidebar.radio("Ir a:", ["Registrar Alimento", "Inventario de alimentos", "Registrar Usuario", "Organizaciones y personas"])

# 1. Registrar información de usuarios
if menu == "Registrar Alimento":
    st.title("Registro de Alimentos")
    with st.form("form_registro"):
        alimento = st.text_input("Alimento:")
        tipo = st.text_input("Tipo:")
        cantidad = st.text_input("Cantidad:")
        fecha_recepcion = st.date_input("Fecha de recepción:", value=datetime.today())
        fecha_caducidad = st.date_input("Fecha de caducidad:", value=datetime.today())
        
        # Botón de envío
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            if alimento and tipo and cantidad and fecha_recepcion and fecha_caducidad:
                hoy = datetime.today().date()
                dias_cad = hoy - fecha_caducidad
                nuevo_usuario = {"Alimento": alimento,"Tipo": tipo, "Cantidad": cantidad, "Fecha de recepción": fecha_recepcion, "Fecha de caducidad": fecha_caducidad, "Días para caducar": dias_cad}
                st.session_state["users_data"] = pd.concat(
                    [st.session_state["users_data"], pd.DataFrame([nuevo_usuario])],
                    ignore_index=True
                )
                st.success(f"Alimento {alimento} registrado exitosamente.")
            else:
                st.error("Por favor, completa todos los campos.")

# 2. Consultar información de usuarios
elif menu == "Inventario de alimentos":
    st.title("Inventario de alimentos")
    
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

# 3. Registrar información de usuarios
if menu == "Registrar Usuario":
    st.title("Registro de Usuarios")
    with st.form("form_registro"):
        nombre = st.text_input("Nombre:")
        correo = st.text_input("Correo:")
        necesidad = st.text_input("Necesidades:")
        
        # Botón de envío
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            if nombre and correo:
                nuevo_usuario = {"Nombre": nombre, "Correo": correo, "Necesidades": necesidad}
                st.session_state["users2_data"] = pd.concat(
                    [st.session_state["users2_data"], pd.DataFrame([nuevo_usuario])],
                    ignore_index=True
                )
                st.success(f"Usuario {nombre} registrado exitosamente.")
            else:
                st.error("Por favor, completa todos los campos.")


# 2. Consultar información de usuarios
elif menu == "Organizaciones y personas":
    st.title("Organizaciones y personas")
    
    if st.session_state["users2_data"].empty:
        st.warning("No hay usuarios registrados.")
    else:
        st.dataframe(st.session_state["users2_data"])
