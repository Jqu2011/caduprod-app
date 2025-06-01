import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="CaduProd", layout="wide")

st.title("🧀 Control de Vencimientos - CaduProd")

# Cargar CSV
csv_file = "productos_demo.csv"
df = pd.read_csv(csv_file, parse_dates=["Fecha Vencimiento", "Fecha Ingreso"], dayfirst=False)

# Calcular días restantes
today = datetime.today().date()
df["Días Restantes"] = (df["Fecha Vencimiento"] - pd.to_datetime(today)).dt.days

# Etiquetas de estado
def etiquetar(dias):
    if dias < 0:
        return "🔴 Vencido"
    elif dias <= 5:
        return "⚠️ Por vencer"
    else:
        return "🟢 Vigente"

df["Estado"] = df["Días Restantes"].apply(etiquetar)

# Filtro
estado_filtro = st.sidebar.multiselect("Filtrar por estado", options=df["Estado"].unique(), default=df["Estado"].unique())
df_filtrado = df[df["Estado"].isin(estado_filtro)]

# Mostrar tabla editable
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("➕ Registrar Retiro de Producto")
with st.form("form_retiro"):
    lote = st.selectbox("Selecciona ID de Lote", df["ID Lote"].unique())
    accion = st.selectbox("Acción de retiro", ["Por consumo", "Vencimiento", "Promoción"])
    fecha_retiro = st.date_input("Fecha de retiro", value=today)
    obs = st.text_area("Observaciones")

    submitted = st.form_submit_button("Registrar")
    if submitted:
        idx = df[df["ID Lote"] == lote].index[0]
        df.at[idx, "Acción Retiro"] = accion
        df.at[idx, "Fecha Retiro"] = fecha_retiro.strftime("%Y-%m-%d")
        df.at[idx, "Observaciones"] = obs
        df.to_csv(csv_file, index=False)
        st.success(f"✅ Retiro registrado para el lote {lote}")

