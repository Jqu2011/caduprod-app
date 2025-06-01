
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CaduProd", layout="wide")

st.title("🧀 Control de Productos con Fecha de Vencimiento")

@st.cache_data
def load_data():
    return pd.read_csv("productos_demo.csv")

df = load_data()

# Convertir fechas si no están en datetime
df["Fecha Vencimiento"] = pd.to_datetime(df["Fecha Vencimiento"])
df["Fecha Ingreso"] = pd.to_datetime(df["Fecha Ingreso"])

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    estado_filter = st.selectbox("Filtrar por estado", ["Todos"] + sorted(df["Estado"].dropna().unique().tolist()))
with col2:
    tienda_filter = st.selectbox("Filtrar por tienda", ["Todos"] + sorted(df["Tienda"].dropna().unique().tolist()))
with col3:
    ubicacion_filter = st.selectbox("Filtrar por ubicación", ["Todos"] + sorted(df["Ubicación"].dropna().unique().tolist()))

filtered_df = df.copy()
if estado_filter != "Todos":
    filtered_df = filtered_df[filtered_df["Estado"] == estado_filter]
if tienda_filter != "Todos":
    filtered_df = filtered_df[filtered_df["Tienda"] == tienda_filter]
if ubicacion_filter != "Todos":
    filtered_df = filtered_df[filtered_df["Ubicación"] == ubicacion_filter]

# Mostrar tabla
st.dataframe(
    filtered_df.sort_values(by="Fecha Vencimiento"),
    use_container_width=True
)

# Subir nuevo producto
st.subheader("📦 Agregar nuevo producto")
with st.form("form_nuevo"):
    col1, col2 = st.columns(2)
    with col1:
        id_lote = st.text_input("ID Lote")
        producto = st.text_input("Producto")
        marca = st.text_input("Marca")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
    with col2:
        fecha_vencimiento = st.date_input("Fecha Vencimiento")
        tienda = st.text_input("Tienda")
        ubicacion = st.text_input("Ubicación")
    enviado = st.form_submit_button("Guardar")
    if enviado:
        st.success("✅ Producto registrado (simulado, no se guarda en el archivo CSV).")
