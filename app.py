import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Título principal
st.set_page_config(page_title="CaduProd", layout="wide")
st.title("🧀 CaduProd - Control de Productos Perecibles")

# Cargar CSV
csv_path = "productos_demo.csv"

# Si el archivo existe, cargarlo
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df["Fecha Vencimiento"] = pd.to_datetime(df["Fecha Vencimiento"])
    df["Fecha Ingreso"] = pd.to_datetime(df["Fecha Ingreso"])
else:
    st.error("⚠️ El archivo productos_demo.csv no se encuentra en el repositorio.")
    st.stop()

# Calcular días restantes
today = pd.to_datetime(datetime.today().date())
df["Días Restantes"] = (df["Fecha Vencimiento"] - today).dt.days

# Clasificar estado con emoji
def calcular_estado(dias):
    if dias < 0:
        return "❌ Vencido"
    elif dias <= 5:
        return "⚠️ Por vencer"
    else:
        return "🟢 Vigente"

df["Estado"] = df["Días Restantes"].apply(calcular_estado)

# Filtros laterales
st.sidebar.header("Filtros")
ubicaciones = st.sidebar.multiselect("Ubicación", options=df["Ubicación"].unique(), default=df["Ubicación"].unique())
estado = st.sidebar.multiselect("Estado", options=df["Estado"].unique(), default=df["Estado"].unique())
producto = st.sidebar.text_input("Buscar producto")

# Aplicar filtros
df_filtrado = df[
    df["Ubicación"].isin(ubicaciones) &
    df["Estado"].isin(estado) &
    df["Producto"].str.contains(producto, case=False, na=False)
]

# Mostrar tabla
st.subheader("📋 Lista de productos")
st.dataframe(df_filtrado.sort_values(by="Días Restantes"), use_container_width=True)

# Formulario para agregar nuevo producto
st.subheader("➕ Registrar nuevo producto")
with st.form("nuevo_producto_form"):
    col1, col2 = st.columns(2)
    with col1:
        id_lote = st.text_input("ID Lote")
        producto_nuevo = st.text_input("Producto")
        marca = st.text_input("Marca")
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
    with col2:
        fecha_venc = st.date_input("Fecha Vencimiento")
        fecha_ing = st.date_input("Fecha Ingreso", value=datetime.today())
        tienda = st.text_input("Tienda")
        ubicacion = st.text_input("Ubicación")

    submitted = st.form_submit_button("Guardar")

    if submitted:
        nuevo = pd.DataFrame([{
            "ID Lote": id_lote,
            "Producto": producto_nuevo,
            "Marca": marca,
            "Fecha Vencimiento": fecha_venc,
            "Cantidad": cantidad,
            "Tienda": tienda,
            "Ubicación": ubicacion,
            "Fecha Ingreso": fecha_ing
        }])
        nuevo["Fecha Vencimiento"] = pd.to_datetime(nuevo["Fecha Vencimiento"])
        nuevo["Fecha Ingreso"] = pd.to_datetime(nuevo["Fecha Ingreso"])
        nuevo["Días Restantes"] = (nuevo["Fecha Vencimiento"] - today).dt.days
        nuevo["Estado"] = nuevo["Días Restantes"].apply(calcular_estado)

        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("✅ Producto registrado correctamente. Actualiza la página para verlo en la lista.")

