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
# SESIÓN
# =====================================================
if "documentos" not in st.session_state:
    st.session_state.documentos = []

if "pendientes" not in st.session_state:
    st.session_state.pendientes = []

if "rechazados" not in st.session_state:
    st.session_state.rechazados = []

# =====================================================
# ARCHIVOS BASE
# =====================================================
if not os.path.exists("documentos.csv"):
    pd.DataFrame(columns=[
        "Documento", "Tipo", "Version", "Responsable",
        "Estado", "Archivo", "Aprobador", "Observaciones"
    ]).to_csv("documentos.csv", index=False)

if not os.path.exists("auditoria.csv"):
    pd.DataFrame(columns=[
        "Fecha", "Accion", "Documento", "Usuario"
    ]).to_csv("auditoria.csv", index=False)

if not os.path.exists("versiones.csv"):
    pd.DataFrame(columns=[
        "Documento", "Version", "Fecha", "Responsable", "Descripcion"
    ]).to_csv("versiones.csv", index=False)

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
# UI
# =====================================================
st.sidebar.title("🗃️ Gestión Documental")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "🏠 Inicio",
        "📝 Registrar Documento",
        "✅ Aprobaciones",
        "📚 Repositorio Documental",
        "📊 Dashboard",
        "📜 Auditoría"
    ]
)

st.image("log_CCB.png", width=180)

# =====================================================
# INICIO
# =====================================================
if menu == "🏠 Inicio":
    st.title("📁 Gestión Documental de Iniciativas IT")

    st.markdown("""
    ### Sistema de gestión documental con flujo de aprobación
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Documentos", len(st.session_state.documentos))
    col2.metric("Pendientes", len(st.session_state.pendientes))
    col3.metric("Rechazados", len(st.session_state.rechazados))
    col4.metric("Usuarios", "45")

# =====================================================
# REGISTRO
# =====================================================
if menu == "📝 Registrar Documento":

    st.title("📝 Registro de Documento")

    nombre = st.text_input("Nombre del documento")

    tipo = st.selectbox(
        "Tipo de documento",
        ["Caso de Prueba", "Manual", "Requerimiento", "Documento Técnico"]
    )

    version = st.text_input("Versión")
    responsable = st.text_input("Responsable")

    archivo = st.file_uploader(
        "📎 Adjuntar documento",
        type=["pdf", "docx", "xlsx", "txt"]
    )

    if st.button("📤 Enviar a revisión"):

        if nombre and version and responsable and archivo:

            archivo_bytes = archivo.read()

            documento = {
                "Documento": nombre,
                "Tipo": tipo,
                "Version": version,
                "Responsable": responsable,
                "Estado": "En revisión",
                "Archivo": archivo_bytes,
                "NombreArchivo": archivo.name,
                "Aprobador": "",
                "Observaciones": ""
            }

            st.session_state.pendientes.append(documento)

            registrar_auditoria("CREACIÓN", nombre, responsable)

            st.success("Documento enviado a revisión")
        else:
            st.warning("Complete todos los campos")

# =====================================================
# APROBACIONES
# =====================================================
if menu == "✅ Aprobaciones":

    st.title("🔄 Workflow de Aprobación")

    if len(st.session_state.pendientes) == 0:
        st.warning("No hay documentos pendientes")
    else:

        doc = st.session_state.pendientes[0]

        st.info("📝 Registrado → 👀 En revisión → ✅ Aprobado")

        col1, col2 = st.columns(2)

        # =========================
        # INFORMACIÓN
        # =========================
        with col1:
            st.subheader("📋 Documento")

            st.write(f"**Nombre:** {doc['Documento']}")
            st.write(f"**Versión:** {doc['Version']}")
            st.write(f"**Responsable:** {doc['Responsable']}")
            st.write(f"**Estado:** {doc['Estado']}")

        # =========================
        # DESCARGA
        # =========================
        with col2:
            st.subheader("📄 Archivo")

            st.download_button(
                "📥 Descargar",
                data=doc["Archivo"],
                file_name=doc["NombreArchivo"],
                mime="application/octet-stream"
            )

        aprobador = st.text_input("Aprobador")
        observaciones = st.text_area("Observaciones")

        colA, colB = st.columns(2)

        with colA:
            if st.button("✅ Aprobar"):

                doc["Estado"] = "Aprobado"
                doc["Aprobador"] = aprobador
                doc["Observaciones"] = observaciones

                st.session_state.documentos.append(doc)
                st.session_state.pendientes.pop(0)

                pd.DataFrame(st.session_state.documentos).to_csv(
                    "documentos.csv", index=False
                )

                registrar_auditoria("APROBACIÓN", doc["Documento"], aprobador)

                st.success("Documento aprobado")

        with colB:
            if st.button("❌ Rechazar"):

                doc["Estado"] = "Rechazado"
                doc["Aprobador"] = aprobador
                doc["Observaciones"] = observaciones

                st.session_state.rechazados.append(doc)
                st.session_state.pendientes.pop(0)

                registrar_auditoria("RECHAZO", doc["Documento"], aprobador)

                st.error("Documento rechazado")

# =====================================================
# REPOSITORIO
# =====================================================
if menu == "📚 Repositorio Documental":

    st.title("📚 Repositorio")

    if len(st.session_state.documentos) == 0:
        st.info("Sin documentos aprobados")
    else:

        df = pd.DataFrame(st.session_state.documentos)

        st.dataframe(df, use_container_width=True)

# =====================================================
# DASHBOARD
# =====================================================
if menu == "📊 Dashboard":

    st.title("📊 Indicadores")

    col1, col2, col3 = st.columns(3)

    col1.metric("Aprobados", len(st.session_state.documentos))
    col2.metric("Pendientes", len(st.session_state.pendientes))
    col3.metric("Rechazados", len(st.session_state.rechazados))

# =====================================================
# AUDITORÍA
# =====================================================
if menu == "📜 Auditoría":

    st.title("📜 Auditoría")

    df = pd.read_csv("auditoria.csv")

    st.dataframe(df, use_container_width=True)
