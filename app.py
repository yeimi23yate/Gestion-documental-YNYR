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
# VARIABLES DE SESIÓN
# =====================================================

if "pendientes" not in st.session_state:
    st.session_state.pendientes = []

if "aprobados" not in st.session_state:
    st.session_state.aprobados = []

if "rechazados" not in st.session_state:
    st.session_state.rechazados = []

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
        "🔄 Control de Versiones",
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

    ### Centralice, controle y asegure la trazabilidad de la documentación de sus iniciativas.

    Este sistema permite gestionar el ciclo de vida documental de forma integral: registro, revisión, aprobación, publicación y consulta, garantizando control de versiones, trazabilidad y acceso oportuno a la información.
    """)

    st.divider()

    st.subheader("🎯 Beneficios")

    col1, col2 = st.columns(2)

    with col1:
        st.success("📈 Centralización documental")
        st.success("📈 Control de versiones")
        st.success("📈 Trazabilidad completa")

    with col2:
        st.success("📈 Flujo de aprobación")
        st.success("📈 Consulta rápida")
        st.success("📈 Indicadores de gestión")

# =====================================================
# REGISTRO DOCUMENTO
# =====================================================

elif menu == "📝 Registrar Documento":

    st.header("📄 Registro de Documento")

    nombre = st.text_input("Nombre del documento")

    tipo = st.selectbox(
        "Tipo",
        [
            "Caso de Prueba",
            "Manual",
            "Requerimiento",
            "Documento Técnico"
        ]
    )

    version = st.text_input("Versión")
    responsable = st.text_input("Responsable")

    archivo = st.file_uploader(
        "Adjuntar documento",
        type=["pdf", "docx", "xlsx", "txt"]
    )

    if st.button("Enviar a revisión"):

        if nombre and version and responsable:

            documento = {
                "Documento": nombre,
                "Tipo": tipo,
                "Version": version,
                "Responsable": responsable,
                "Estado": "Pendiente",
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "NombreArchivo": archivo.name if archivo else "",
                "Contenido": archivo.read() if archivo else b"",
                "Observaciones": ""
            }

            st.session_state.pendientes.append(documento)

            st.success("Documento enviado a revisión")

        else:
            st.warning("Complete los campos obligatorios")

# =====================================================
# APROBACIONES
# =====================================================

elif menu == "✅ Aprobaciones":

    st.header("📥 Bandeja de Aprobaciones")

    if len(st.session_state.pendientes) == 0:
        st.info("No existen documentos pendientes")

    else:

        nombres = [doc["Documento"] for doc in st.session_state.pendientes]

        seleccion = st.selectbox(
            "Seleccione documento",
            ["-- Seleccione --"] + nombres
        )

        if seleccion != "-- Seleccione --":

            doc = next(
                d for d in st.session_state.pendientes
                if d["Documento"] == seleccion
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Documento:** {doc['Documento']}")
                st.write(f"**Tipo:** {doc['Tipo']}")
                st.write(f"**Versión:** {doc['Version']}")
                st.write(f"**Responsable:** {doc['Responsable']}")

            with col2:
                st.write(f"**Estado:** {doc['Estado']}")
                st.write(f"**Fecha:** {doc['Fecha']}")

            if doc["NombreArchivo"]:
                st.download_button(
                    "📥 Descargar documento",
                    doc["Contenido"],
                    file_name=doc["NombreArchivo"]
                )

            observaciones = st.text_area("Observaciones")

            colA, colB = st.columns(2)

            with colA:
                if st.button("✅ Aprobar"):

                    doc["Estado"] = "Aprobado"
                    doc["Observaciones"] = observaciones

                    st.session_state.aprobados.append(doc)
                    st.session_state.pendientes.remove(doc)

                    st.success("Documento aprobado")
                    st.rerun()

            with colB:
                if st.button("❌ Rechazar"):

                    doc["Estado"] = "Rechazado"
                    doc["Observaciones"] = observaciones

                    st.session_state.rechazados.append(doc)
                    st.session_state.pendientes.remove(doc)

                    st.error("Documento rechazado")
                    st.rerun()

# =====================================================
# REPOSITORIO
# =====================================================

elif menu == "📚 Repositorio":

    st.header("📚 Repositorio Documental")

    if len(st.session_state.aprobados) == 0:
        st.info("No existen documentos aprobados")

    else:
        df = pd.DataFrame(st.session_state.aprobados)

        st.dataframe(
            df[[
                "Documento",
                "Tipo",
                "Version",
                "Responsable",
                "Estado",
                "Fecha"
            ]],
            use_container_width=True
        )

# =====================================================
# CONTROL DE VERSIONES
# =====================================================

elif menu == "🔄 Control de Versiones":

    st.header("🔄 Control de Versiones")

    if len(st.session_state.aprobados) == 0:
        st.info("No existen documentos aprobados")

    else:
        df = pd.DataFrame(st.session_state.aprobados)

        st.dataframe(
            df[[
                "Documento",
                "Version",
                "Responsable",
                "Fecha"
            ]],
            use_container_width=True
        )

# =====================================================
# CONSULTA
# =====================================================

elif menu == "🔍 Consulta":

    st.header("🔍 Consulta Documental")

    criterio = st.text_input("Buscar documento")

    if criterio:

        df = pd.DataFrame(st.session_state.aprobados)

        if not df.empty:

            resultado = df[
                df["Documento"].str.contains(criterio, case=False, na=False)
            ]

            st.dataframe(resultado, use_container_width=True)

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
    # GRÁFICO + PORCENTAJES
    # =====================================================
    if total > 0:

        st.subheader("📈 Distribución del flujo (Azure DevOps style)")

        data = pd.DataFrame({
            "Estado": ["Pendientes", "Aprobados", "Rechazados"],
            "Cantidad": [pendientes, aprobados, rechazados]
        })

        data["%"] = (data["Cantidad"] / total * 100).round(2)

        # =====================================================
        # COLORES TIPO AZURE DEVOPS
        # =====================================================
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

        # =====================================================
        # TABLA DETALLE
        # =====================================================
        st.subheader("📊 Distribución porcentual")
        st.dataframe(data, use_container_width=True)

    else:
        st.info("No hay datos para mostrar el dashboard aún.")
