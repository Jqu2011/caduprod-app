import streamlit as st
import pandas as pd
import datetime

# Cargar el archivo CSV
@st.cache_data
def load_data():
    return pd.read_csv("productos_demo.csv", parse_dates=["Fecha Vencimiento", "Fecha Ingreso"])

df = load_data()

# Calcular días restantes si no existe
if "Días Restantes" not in df.columns:
    today = datetime.date.today()
    df["Días Restantes"] = (df["Fecha Vencimiento"] - pd.Timestamp(today)).dt.days

# Clasificar estado
def get_estado(dias):
    if dias < 0:
        return "🔴 Vencido"
    elif dias <= 5:
        return "🟠 Por vencer"
    else:
        return "🟢 Vigente"

df["Estado"] = df["Días Restantes"].apply(get_estado)

# Título
st.title("🧀 Gestión de Productos por Caducidad")

# Filtros
estado = st.multiselect("Filtrar por estado", df["Estado"].unique(), default=df["Estado"].unique())
ubicacion = st.multiselect("Filtrar por ubicación", df["Ubicación"].unique(), default=df["Ubicación"].unique())

# Aplicar filtros
filtered_df = df[df["Estado"].isin(estado) & df["Ubicación"].isin(ubicacion)]

# Mostrar resultados
st.dataframe(filtered_df, use_container_width=True)

# Agregar nuevo producto (modo demo)
with st.expander("➕ Agregar nuevo producto"):
    with st.form("nuevo_producto"):
        id_lote = st.text_input("ID Lote")
        producto = st.text_input("Producto")
        marca = st.text_input("Marca")
        fecha_v = st.date_input("Fecha Vencimiento")
        cantidad = st.number_input("Cantidad", min_value=0, step=1)
        tienda = st.text_input("Tienda")
        ubicacion = st.text_input("Ubicación")
        fecha_ing = st.date_input("Fecha Ingreso")

        if st.form_submit_button("Guardar"):
            st.success("Producto agregado (modo demo, no guarda en el archivo original)")

