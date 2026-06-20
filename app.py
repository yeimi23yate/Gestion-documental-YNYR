import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📁",
    layout="wide"
)

# =====================================================
# ESTADO CENTRAL DEL SISTEMA (ARQUITECTURA ESTABLE)
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
    pd.DataFrame(columns=[
        "Fecha", "Accion", "Documento", "Usuario"
    ]).to_csv("auditoria.csv", index=False)

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
# INICIO
# =====================================================
if menu == "🏠 Inicio":

    st.title("📁 Sistema de Gestión Documental")

    col1, col2, col3 = st.columns(3)

    col1.metric("Pendientes", len(st.session_state.db["pendientes"]))
    col2.metric("Aprobados", len(st.session_state.db["aprobados"]))
    col3.metric("Rechazados", len(st.session_state.db["rechazados"]))

    st.info("Sistema de flujo documental centralizado con control de estados y trazabilidad.")

# =====================================================
# REGISTRO DOCUMENTO
# =====================================================
if menu == "📝 Registrar Documento":

    st.title("📝 Registro de Documento")

    nombre = st.text_input("Nombre del documento")
    tipo = st.selectbox("Tipo", ["Requerimiento", "Caso de Prueba", "Manual", "Técnico"])
    version = st.text_input("Versión")
    responsable = st.text_input("Responsable")

    archivo = st.file_uploader("Adjuntar archivo", type=["pdf", "docx", "xlsx", "txt"])

    if st.button("Enviar a revisión"):

        if nombre and version and responsable:

            documento = {
                "Documento": nombre,
                "Tipo": tipo,
                "Version": version,
                "Responsable": responsable,
                "Estado": "En revisión",
                "Archivo": archivo.read() if archivo else None,
                "NombreArchivo": archivo.name if archivo else None,
                "Aprobador": "",
                "Observaciones": "",
                "Fecha": str(datetime.now())
            }

            st.session_state.db["pendientes"].append(documento)

            registrar_auditoria("CREACIÓN", nombre, responsable)

            st.success("Documento enviado a revisión")

# =====================================================
# APROBACIONES
# =====================================================
if menu == "✅ Aprobaciones":

    st.title("🔄 Flujo de Aprobación")

    if len(st.session_state.db["pendientes"]) == 0:
        st.warning("No hay documentos pendientes")
    else:

        doc = st.session_state.db["pendientes"][0]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 Documento")
            st.write(f"**Nombre:** {doc['Documento']}")
            st.write(f"**Versión:** {doc['Version']}")
            st.write(f"**Responsable:** {doc['Responsable']}")
            st.write(f"**Estado:** {doc['Estado']}")

        with col2:
            st.subheader("📎 Archivo")

            if doc["Archivo"]:
                st.download_button(
                    "Descargar archivo",
                    data=doc["Archivo"],
                    file_name=doc["NombreArchivo"],
                    mime="application/octet-stream"
                )

        aprobador = st.text_input("Aprobador")
        observaciones = st.text_area("Observaciones")

        colA, colB = st.columns(2)

        with colA:
            if st.button("Aprobar"):

                doc["Estado"] = "Aprobado"
                doc["Aprobador"] = aprobador
                doc["Observaciones"] = observaciones

                st.session_state.db["aprobados"].append(doc)
                st.session_state.db["pendientes"].pop(0)

                pd.DataFrame(st.session_state.db["aprobados"]).to_csv(
                    "documentos.csv", index=False
                )

                registrar_auditoria("APROBACIÓN", doc["Documento"], aprobador)

                st.success("Documento aprobado")

        with colB:
            if st.button("Rechazar"):

                doc["Estado"] = "Rechazado"
                doc["Aprobador"] = aprobador
                doc["Observaciones"] = observaciones

                st.session_state.db["rechazados"].append(doc)
                st.session_state.db["pendientes"].pop(0)

                registrar_auditoria("RECHAZO", doc["Documento"], aprobador)

                st.error("Documento rechazado")

# =====================================================
# REPOSITORIO
# =====================================================
if menu == "📚 Repositorio":

    st.title("📚 Repositorio Documental")

    df = pd.DataFrame(st.session_state.db["aprobados"])

    if df.empty:
        st.info("No hay documentos aprobados")

    else:
        # =====================================================
        # OCULTAR COLUMNA ARCHIVO (BLOQUE CORRECTO)
        # =====================================================
        df_mostrar = df.drop(columns=["Archivo"], errors="ignore")

        st.dataframe(
            df_mostrar,
            use_container_width=True
        )

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
    # KPIs PRINCIPALES
    # =====================================================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📌 Total documentos", total)
    col2.metric("🟡 Pendientes", pendientes)
    col3.metric("🟢 Aprobados", aprobados)
    col4.metric("🔴 Rechazados", rechazados)

    st.divider()

    # =====================================================
    # PORCENTAJES
    # =====================================================
    if total > 0:
        st.subheader("📈 Distribución del flujo")

        data = pd.DataFrame({
            "Estado": ["Pendientes", "Aprobados", "Rechazados"],
            "Cantidad": [pendientes, aprobados, rechazados]
        })

        st.bar_chart(data.set_index("Estado"))

        st.subheader("🥧 Distribución porcentual")

        data["%"] = data["Cantidad"] / total * 100
        st.dataframe(data, use_container_width=True)

    else:
        st.info("No hay datos para mostrar el dashboard aún.")

    # =====================================================
    # SIMULACIÓN TIPO AZURE DEVOPS FLOW
    # =====================================================
    st.subheader("🔄 Flujo tipo pipeline")

    st.progress(
        aprobados / total if total > 0 else 0
    )

# =====================================================
# AUDITORÍA
# =====================================================
if menu == "📜 Auditoría":

    st.title("📜 Historial de Auditoría")

    df = pd.read_csv("auditoria.csv")

    st.dataframe(df, use_container_width=True)
