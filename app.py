
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la app
st.set_page_config(page_title="CaduProd", layout="wide")
st.title("🧊 CaduProd - Control de Fechas de Vencimiento")

# Cargar CSV si existe
csv_path = "productos_demo.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=[
        "Producto", "Marca", "Fecha Vencimiento", "Cantidad",
        "Tienda", "Ubicación", "Fecha Ingreso", "Días Restantes",
        "Estado", "Acción Retiro", "Fecha Retiro", "Observaciones"
    ])

# Función para calcular días restantes y estado
def calcular_estado(fecha_venc):
    hoy = datetime.today().date()
    venc = datetime.strptime(fecha_venc, "%Y-%m-%d").date()
    dias = (venc - hoy).days
    if dias < 0:
        estado = "❌ Vencido"
    elif dias <= 5:
        estado = "⚠️ Por vencer"
    else:
        estado = "✅ Vigente"
    return dias, estado

# Formulario para registrar nuevo producto
st.sidebar.header("➕ Registrar Nuevo Producto")
with st.sidebar.form("nuevo_producto"):
    producto = st.text_input("Producto")
    marca = st.text_input("Marca")
    fecha_venc = st.date_input("Fecha Vencimiento")
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    tienda = st.text_input("Tienda")
    ubicacion = st.text_input("Ubicación (Ej: Nevera 1, Hilera 2)")
    submitted = st.form_submit_button("Guardar")
    if submitted and producto and marca:
        dias_restantes, estado = calcular_estado(str(fecha_venc))
        nuevo = {
            "Producto": producto,
            "Marca": marca,
            "Fecha Vencimiento": fecha_venc,
            "Cantidad": cantidad,
            "Tienda": tienda,
            "Ubicación": ubicacion,
            "Fecha Ingreso": datetime.now().strftime("%Y-%m-%d"),
            "Días Restantes": dias_restantes,
            "Estado": estado,
            "Acción Retiro": "",
            "Fecha Retiro": "",
            "Observaciones": ""
        }
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.sidebar.success("Producto registrado exitosamente.")

# Filtros
estado_sel = st.sidebar.multiselect("Filtrar por Estado", df["Estado"].unique())
tienda_sel = st.sidebar.multiselect("Filtrar por Tienda", df["Tienda"].unique())
ubicacion_sel = st.sidebar.multiselect("Filtrar por Ubicación", df["Ubicación"].unique())

filtro = df.copy()
if estado_sel:
    filtro = filtro[filtro["Estado"].isin(estado_sel)]
if tienda_sel:
    filtro = filtro[filtro["Tienda"].isin(tienda_sel)]
if ubicacion_sel:
    filtro = filtro[filtro["Ubicación"].isin(ubicacion_sel)]

# Mostrar tabla
st.subheader("📋 Lista de Productos")
st.dataframe(filtro, use_container_width=True)

# Registro de retiro
st.subheader("🔄 Registrar Retiro")
if not df.empty:
    with st.form("form_retiro"):
        idx = st.selectbox("Selecciona el índice del producto", df.index)
        motivo = st.selectbox("Motivo del retiro", ["Consumo", "Vencimiento", "Promoción"])
        observ = st.text_area("Observaciones")
        retirar = st.form_submit_button("Registrar Retiro")
        if retirar:
            df.at[idx, "Acción Retiro"] = motivo
            df.at[idx, "Fecha Retiro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.at[idx, "Observaciones"] = observ
            df.to_csv(csv_path, index=False)
            st.success(f"Retiro registrado para '{df.at[idx, 'Producto']}'.")

# Guardar cambios al cerrar sesión
df.to_csv(csv_path, index=False)
