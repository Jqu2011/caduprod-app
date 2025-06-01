import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="CaduProd", layout="wide")

# Cargar CSV
@st.cache_data
def load_data():
    return pd.read_csv("productos_demo.csv", parse_dates=["Fecha Vencimiento", "Fecha Ingreso"])

df = load_data()

# Recalcular "Días Restantes" si no está, o actualizarlo
today = datetime.date.today()
df["Días Restantes"] = (df["Fecha Vencimiento"] - pd.Timestamp(today)).dt.days

# Recalcular "Estado"
def calcular_estado(dias):
    if dias < 0:
        return "🔴 Vencido"
    elif dias <= 5:
        return "🟠 Por vencer"
    else:
        return "🟢 Vigente"

df["Estado"] = df["Días Restantes"].apply(calcular_estado)

# Título
st.title("📦 CaduProd – Control de Vencimiento de Productos")

# Filtros
col1, col2 = st.columns(2)
with col1:
    estados = st.multiselect("📌 Filtrar por Estado", df["Estado"].unique(), default=df["Estado"].unique())
with col2:
    ubicaciones = st.multiselect("📍 Filtrar por Ubicación", df["Ubicación"].unique(), default=df["Ubicación"].unique())

# Aplicar filtros
df_filtrado = df[df["Estado"].isin(estados) & df["Ubicación"].isin(ubicaciones)]

# Tabla principal
st.dataframe(df_filtrado.sort_values("Días Restantes"), use_container_width=True)

# Agregar productos nuevos (modo demo)
with st.expander("➕ Agregar nuevo producto"):
    with st.form("formulario_producto"):
        id_lote = st.text_input("ID Lote")
        producto = st.text_input("Producto")
        marca = st.text_input("Marca")
        fecha_v = st.date_input("Fecha Vencimiento")
        cantidad = st.number_input("Cantidad", min_value=1)
        tienda = st.text_input("Tienda")
        ubicacion = st.text_input("Ubicación")
        fecha_ing = st.date_input("Fecha Ingreso", value=datetime.date.today())

        submitted = st.form_submit_button("Guardar producto (solo en pantalla)")
        if submitted:
            nuevo = {
                "ID Lote": id_lote,
                "Producto": producto,
                "Marca": marca,
                "Fecha Vencimiento": fecha_v,
                "Cantidad": cantidad,
                "Tienda": tienda,
                "Ubicación": ubicacion,
                "Fecha Ingreso": fecha_ing,
                "Días Restantes": (fecha_v - today).days,
                "Estado": calcular_estado((fecha_v - today).days)
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("✅ Producto agregado (modo visual, sin guardar en archivo)")
            st.dataframe(df.tail(1), use_container_width=True)

