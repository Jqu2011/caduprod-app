
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Configuración inicial
st.set_page_config(page_title="CaduProd - Control de Vencimientos", layout="wide")
st.title("📦 CaduProd - Control de Productos Alimenticios")

# Ruta del archivo CSV (puede integrarse con GitHub o Google Drive)
CSV_FILE = "productos_demo.csv"

# Cargar datos
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=[
        "ID Lote", "Producto", "Marca", "Fecha Vencimiento", "Cantidad",
        "Tienda", "Ubicación", "Fecha Ingreso", "Días Restantes", "Estado",
        "Acción Retiro", "Fecha Retiro", "Observaciones"
    ])

# Actualizar estado dinámicamente
hoy = pd.Timestamp(datetime.today().date())
df["Fecha Vencimiento"] = pd.to_datetime(df["Fecha Vencimiento"], errors='coerce')
df["Días Restantes"] = (df["Fecha Vencimiento"] - hoy).dt.days

def calcular_estado(d):
    if pd.isna(d): return "❓ Sin Fecha"
    elif d < 0: return "🔴 Vencido"
    elif d <= 5: return "🟡 Por vencer"
    else: return "🟢 Vigente"

df["Estado"] = df["Días Restantes"].apply(calcular_estado)

# FILTROS
with st.sidebar:
    st.header("🔍 Filtros")
    estado_filtrado = st.multiselect("Filtrar por Estado", options=df["Estado"].unique(), default=list(df["Estado"].unique()))
    ubicaciones = st.multiselect("Filtrar por Ubicación", options=sorted(df["Ubicación"].dropna().unique()), default=sorted(df["Ubicación"].dropna().unique()))
    tienda = st.multiselect("Filtrar por Tienda", options=df["Tienda"].dropna().unique(), default=list(df["Tienda"].dropna().unique()))

# Aplicar filtros
df_filtrado = df[
    df["Estado"].isin(estado_filtrado) &
    df["Ubicación"].isin(ubicaciones) &
    df["Tienda"].isin(tienda)
]

# Mostrar tabla principal
st.subheader("📋 Productos Registrados")
st.dataframe(df_filtrado.sort_values("Días Restantes"), use_container_width=True)

# FORMULARIO para nuevos registros
with st.expander("➕ Registrar Nuevo Producto"):
    with st.form("nuevo_producto_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            lote = st.text_input("ID Lote")
            producto = st.text_input("Producto")
            marca = st.text_input("Marca")
        with col2:
            fecha_venc = st.date_input("Fecha de Vencimiento")
            cantidad = st.number_input("Cantidad", min_value=1)
            tienda_input = st.text_input("Tienda")
        with col3:
            ubicacion = st.text_input("Ubicación")
            fecha_ingreso = st.date_input("Fecha de Ingreso", value=datetime.today())
            observaciones = st.text_area("Observaciones")

        submitted = st.form_submit_button("Guardar Registro")

        if submitted:
            dias_restantes = (pd.to_datetime(fecha_venc) - hoy).days
            estado = calcular_estado(dias_restantes)
            nuevo_registro = pd.DataFrame([{
                "ID Lote": lote,
                "Producto": producto,
                "Marca": marca,
                "Fecha Vencimiento": fecha_venc,
                "Cantidad": cantidad,
                "Tienda": tienda_input,
                "Ubicación": ubicacion,
                "Fecha Ingreso": fecha_ingreso,
                "Días Restantes": dias_restantes,
                "Estado": estado,
                "Acción Retiro": "",
                "Fecha Retiro": "",
                "Observaciones": observaciones
            }])
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success("✅ Producto registrado correctamente. Recarga la app para ver cambios.")

# Información de pie
st.caption("Creado con ❤️ usando Streamlit")
