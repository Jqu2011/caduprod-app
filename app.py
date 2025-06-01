import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="CaduProd", layout="wide")
st.title("📦 Control de Productos y Caducidades")

# Función para cargar los datos
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("productos_demo.csv")
        df["Fecha Vencimiento"] = pd.to_datetime(df["Fecha Vencimiento"], errors='coerce')
        df["Días Restantes"] = (df["Fecha Vencimiento"] - pd.to_datetime(datetime.now())).dt.days
        df["Estado"] = df["Días Restantes"].apply(
            lambda x: "🔴 Vencido" if x < 0 else "🟠 Por vencer" if x <= 5 else "🟢 Vigente"
        )
        return df
    except:
        return pd.DataFrame()

# Cargar datos
df = load_data()

# --- REGISTRO DE NUEVO PRODUCTO ---
st.sidebar.header("➕ Añadir nuevo producto")
with st.sidebar.form("form_nuevo"):
    nuevo_id = st.text_input("ID Lote")
    nuevo_producto = st.text_input("Producto")
    nueva_marca = st.text_input("Marca")
    nueva_fecha = st.date_input("Fecha Vencimiento")
    nueva_cantidad = st.number_input("Cantidad", min_value=1, step=1)
    nueva_tienda = st.text_input("Tienda")
    nueva_ubicacion = st.text_input("Ubicación")
    enviar = st.form_submit_button("Registrar")

if enviar:
    dias_restantes = (pd.to_datetime(nueva_fecha) - datetime.now()).days
    estado = "🔴 Vencido" if dias_restantes < 0 else "🟠 Por vencer" if dias_restantes <= 5 else "🟢 Vigente"

    nuevo = pd.DataFrame([{
        "ID Lote": nuevo_id,
        "Producto": nuevo_producto,
        "Marca": nueva_marca,
        "Fecha Vencimiento": nueva_fecha,
        "Cantidad": nueva_cantidad,
        "Tienda": nueva_tienda,
        "Ubicación": nueva_ubicacion,
        "Fecha Ingreso": datetime.now().strftime('%Y-%m-%d'),
        "Días Restantes": dias_restantes,
        "Estado": estado
    }])

    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv("productos_demo.csv", index=False)
    st.success("✅ Producto registrado correctamente. Refresca para visualizar.")

# --- FILTROS ---
with st.expander("🔍 Filtros"):
    estados = st.multiselect("Filtrar por Estado", options=df["Estado"].unique(), default=df["Estado"].unique())
    productos = st.multiselect("Filtrar por Producto", options=sorted(df["Producto"].dropna().unique()))
    ubicaciones = st.multiselect("Filtrar por Ubicación", options=sorted(df["Ubicación"].dropna().unique()))
    fecha_limite = st.date_input("Mostrar productos que vencen antes de:", datetime.today() + timedelta(days=30))

# Aplicar filtros
df_filtrado = df[
    df["Estado"].isin(estados) &
    (df["Producto"].isin(productos) if productos else True) &
    (df["Ubicación"].isin(ubicaciones) if ubicaciones else True) &
    (df["Fecha Vencimiento"] <= pd.to_datetime(fecha_limite))
]

# --- VISUALIZACIÓN ---
st.subheader("📋 Productos en Inventario")
st.dataframe(df_filtrado.sort_values("Fecha Vencimiento"), use_container_width=True)

st.caption("Desarrollado con ❤️ por Inncorporah - 2025")
