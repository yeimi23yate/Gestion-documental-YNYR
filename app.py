import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📈",
    layout="wide"
)

st.sidebar.title("🗃️ Gestión Documental")

# =====================================================
# INICIALIZACIÓN
# =====================================================

if "documentos" not in st.session_state:
    st.session_state.documentos = []

if "id_doc" not in st.session_state:
    st.session_state.id_doc = 1

# =====================================================
# ENCABEZADO
# =====================================================

if os.path.exists("log_CCB.png"):
    st.image("log_CCB.png", width=180)

# =====================================================
# MENÚ
# =====================================================

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "🏠 Home",
        "📝 Registrar Documento",
        "✅ Aprobaciones",
        "📚 Repositorio",
        "🔍 Consulta",
        "📊 Dashboard"
    ],
    index=0
)

# =====================================================
# HOME
# =====================================================

if menu == "🏠 Home":

    st.markdown("""
    # 🚀 Gestión Documental Inteligente
    Sistema de control con trazabilidad completa del ciclo de vida documental.
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Documentos", len(st.session_state.documentos))
    col2.metric("🟡 Pendientes", len([d for d in st.session_state.documentos if d["Estado"] == "Pendiente"]))
    col3.metric("🟢 Aprobados", len([d for d in st.session_state.documentos if d["Estado"] == "Aprobado"]))

# =====================================================
# REGISTRO
# =====================================================

elif menu == "📝 Registrar Documento":

    st.header("📄 Registro de Documento")

    nombre = st.text_input("Nombre")
    tipo = st.selectbox("Tipo", ["Caso de Prueba", "Manual", "Requerimiento", "Documento Técnico"])
    version = st.text_input("Versión")
    responsable = st.text_input("Responsable")

    archivo = st.file_uploader("Adjuntar documento", type=["pdf", "docx", "xlsx", "txt"])

    if st.button("Enviar a revisión"):

        if nombre and version and responsable:

            doc = {
                "id": st.session_state.id_doc,
                "Documento": nombre,
                "Tipo": tipo,
                "Version": version,
                "Responsable": responsable,
                "Estado": "Pendiente",
                "FechaCreacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "FechaDecision": "",
                "NombreArchivo": archivo.name if archivo else "",
                "Contenido": archivo.read() if archivo else b"",
                "Observaciones": "",
                "Historial": []
            }

            doc["Historial"].append(f"Creado {doc['FechaCreacion']}")

            st.session_state.documentos.append(doc)
            st.session_state.id_doc += 1

            st.success("Documento enviado a revisión")

# =====================================================
# APROBACIONES (CON HISTORIAL)
# =====================================================

elif menu == "✅ Aprobaciones":

    st.header("📥 Bandeja de Aprobaciones")

    pendientes = [d for d in st.session_state.documentos if d["Estado"] == "Pendiente"]

    if not pendientes:
        st.info("No existen documentos pendientes")

    else:

        nombres = [f"{d['id']} - {d['Documento']}" for d in pendientes]

        seleccion = st.selectbox("Seleccione documento", nombres)

        doc_id = int(seleccion.split(" - ")[0])
        doc = next(d for d in st.session_state.documentos if d["id"] == doc_id)

        st.subheader(doc["Documento"])

        st.write(doc)

        observaciones = st.text_area("Observaciones")

        colA, colB = st.columns(2)

        if colA.button("✅ Aprobar"):

            doc["Estado"] = "Aprobado"
            doc["FechaDecision"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            doc["Observaciones"] = observaciones
            doc["Historial"].append(f"Aprobado {doc['FechaDecision']}")

            st.success("Aprobado")
            st.rerun()

        if colB.button("❌ Rechazar"):

            doc["Estado"] = "Rechazado"
            doc["FechaDecision"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            doc["Observaciones"] = observaciones
            doc["Historial"].append(f"Rechazado {doc['FechaDecision']}")

            st.error("Rechazado")
            st.rerun()

        st.divider()
        st.subheader("📜 Historial del documento")

        for h in doc["Historial"]:
            st.write("•", h)

# =====================================================
# REPOSITORIO
# =====================================================

elif menu == "📚 Repositorio":

    st.header("📚 Repositorio")

    aprobados = [d for d in st.session_state.documentos if d["Estado"] == "Aprobado"]

    if not aprobados:
        st.info("No hay documentos aprobados")

    else:
        df = pd.DataFrame(aprobados)

        st.dataframe(df[[
            "Documento",
            "Tipo",
            "Version",
            "Responsable",
            "Estado",
            "FechaCreacion"
        ]], use_container_width=True)

# =====================================================
# CONSULTA GLOBAL (MEJORADA)
# =====================================================

elif menu == "🔍 Consulta":

    st.header("🔍 Consulta Documental Global")

    criterio = st.text_input("Buscar documento")

    df = pd.DataFrame(st.session_state.documentos)

    if not df.empty and criterio:

        resultado = df[df["Documento"].str.contains(criterio, case=False)]

        st.dataframe(resultado, use_container_width=True)

    elif df.empty:
        st.info("No hay documentos registrados")

    else:
        st.dataframe(df, use_container_width=True)

# =====================================================
# DASHBOARD REAL
# =====================================================

elif menu == "📊 Dashboard":

    st.title("📊 Dashboard Documental")

    docs = st.session_state.documentos

    pendientes = len([d for d in docs if d["Estado"] == "Pendiente"])
    aprobados = len([d for d in docs if d["Estado"] == "Aprobado"])
    rechazados = len([d for d in docs if d["Estado"] == "Rechazado"])

    total = len(docs)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total)
    col2.metric("Pendientes", pendientes)
    col3.metric("Aprobados", aprobados)
    col4.metric("Rechazados", rechazados)

    st.divider()

    if total > 0:

        data = pd.DataFrame({
            "Estado": ["Pendientes", "Aprobados", "Rechazados"],
            "Cantidad": [pendientes, aprobados, rechazados]
        })

        st.bar_chart(data.set_index("Estado"))

        data["%"] = data["Cantidad"] / total * 100
        st.dataframe(data, use_container_width=True)

    else:
        st.info("No hay datos para mostrar")
