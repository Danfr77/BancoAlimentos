import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Crear un DataFrame en memoria para almacenar la información
if "users_data" not in st.session_state:
    st.session_state["users_data"] = pd.DataFrame(columns=["Alimento","Tipo", "Cantidad", "Fecha de recepción", "Fecha de caducidad", "Estado"])

# Menú de navegación en la barra lateral
st.sidebar.title("Menú de Navegación")
menu = st.sidebar.radio("Ir a:", ["Registrar Alimento", "Inventario de alimentos", "Organizaciones y personas"])

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
                if dias_cad > 7:
                    estado = ("apto para consumo")
                elif dias_cad < 7 and dias_cad > 0 :
                    estado = ("Proximo a caducar")
                else:
                    estado = ("caducado")
                nuevo_usuario = {"Alimento": alimento,"Tipo": tipo, "Cantidad": cantidad, "Fecha de recepción": fecha_recepcion, "Fecha de caducidad": fecha_caducidad, "Estado": estado}
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

# 3. Generar alertas
elif menu == "Generar Alertas":
    st.title("Alertas de Registros Recientes")
    
    if st.session_state["users_data"].empty:
        st.warning("No hay usuarios registrados.")
    else:
        # Validar y convertir "Fecha de Registro" a datetime si es necesario
        if not pd.api.types.is_datetime64_any_dtype(st.session_state["users_data"]["Fecha de Registro"]):
            st.session_state["users_data"]["Fecha de Registro"] = pd.to_datetime(
                st.session_state["users_data"]["Fecha de Registro"], errors="coerce"
            )
        
        # Comprobar si hay fechas inválidas
        if st.session_state["users_data"]["Fecha de Registro"].isnull().any():
            st.error("Algunas fechas de registro no son válidas. Por favor, verifica los datos.")
        else:
            # Calcular la diferencia de días
            hoy = datetime.today().date()
            st.session_state["users_data"]["Días desde registro"] = (
                hoy - st.session_state["users_data"]["Fecha de Registro"].dt.date
            ).dt.days
            
            # Filtrar usuarios registrados en los últimos 7 días
            usuarios_recientes = st.session_state["users_data"][
                st.session_state["users_data"]["Días desde registro"] < 7
            ]
            
            if usuarios_recientes.empty:
                st.info("No hay usuarios registrados en los últimos 7 días.")
            else:
                st.success("Usuarios registrados en los últimos 7 días:")
                st.dataframe(usuarios_recientes)
