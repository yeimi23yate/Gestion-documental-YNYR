import streamlit as st
import pandas as pd
from datetime import datetime
import os
import altair as alt  # ✅ IMPORT NECESARIO

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📁",
    layout="wide"
)

# =====================================================
# ESTADO CENTRAL DEL SISTEMA
# =====================================================
if "db" not in st.session_state:
    st.session_state.db = {
        "pendientes": [],
        "aprobados": [],
        "rechazados": [],
        "versiones": [],
        "auditoria": []
    }

if "form" not in st.session_state:
    st.session_state.form = {}

# =====================================================
# ARCHIVOS PERSISTENCIA
# =====================================================
if not os.path.exists("auditoria.csv"):
    pd.DataFrame(columns=["Fecha", "Accion", "Documento", "Usuario"]).to_csv("auditoria.csv", index=False)

if not os.path.exists("documentos.csv"):
    pd.DataFrame(columns=[
        "Documento", "Version", "Responsable",
        "Estado", "Aprobador", "Observaciones"
    ]).to_csv("documentos.csv", index=False)

# =====================================================
# AUDITORÍA
# =====================================================
def registrar_auditoria(accion, documento, usuario):
    df = pd.read_csv("auditoria.csv")

    nuevo = pd.DataFrame([{
        "Fecha": datetime.now(),
        "Accion": accion,
        "Documento": documento,
        "Usuario": usuario
    }])

    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv("auditoria.csv", index=False)

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🗃️ Gestión Documental")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "🏠 Inicio",
        "📝 Registrar Documento",
        "✅ Aprobaciones",
        "📚 Repositorio",
        "📊 Dashboard",
        "📜 Auditoría"
    ]
)

st.image("log_CCB.png", width=180)

# =====================================================
# DASHBOARD
# =====================================================
if menu == "📊 Dashboard":

    st.title("📊 Indicadores tipo Azure DevOps")

    pendientes = len(st.session_state.db["pendientes"])
    aprobados = len(st.session_state.db["aprobados"])
    rechazados = len(st.session_state.db["rechazados"])

    total = pendientes + aprobados + rechazados

    # =====================================================
    # KPIs
    # =====================================================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📌 Total documentos", total)
    col2.metric("🟡 Pendientes", pendientes)
    col3.metric("🟢 Aprobados", aprobados)
    col4.metric("🔴 Rechazados", rechazados)

    st.divider()

    # =====================================================
    # GRÁFICO CON COLORES
    # =====================================================
    if total > 0:

        st.subheader("📈 Distribución del flujo (Azure DevOps style)")

        data = pd.DataFrame({
            "Estado": ["Pendientes", "Aprobados", "Rechazados"],
            "Cantidad": [pendientes, aprobados, rechazados]
        })

        data["%"] = (data["Cantidad"] / total * 100).round(2)

        # 🎨 COLORES TIPO AZURE DEVOPS
        color_scale = alt.Scale(
            domain=["Pendientes", "Aprobados", "Rechazados"],
            range=["#FFB020", "#2ECC71", "#E74C3C"]
        )

        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X("Estado:N", title="Estado"),
            y=alt.Y("Cantidad:Q", title="Cantidad"),
            color=alt.Color("Estado:N", scale=color_scale),
            tooltip=["Estado", "Cantidad", "%"]
        )

        st.altair_chart(chart, use_container_width=True)

        st.subheader("📊 Distribución porcentual")
        st.dataframe(data, use_container_width=True)

    else:
        st.info("No hay datos para mostrar el dashboard aún.")

# =====================================================
# AUDITORÍA
# =====================================================
if menu == "📜 Auditoría":

    st.title("📜 Historial de Auditoría")

    df = pd.read_csv("auditoria.csv")

    st.dataframe(df, use_container_width=True)
