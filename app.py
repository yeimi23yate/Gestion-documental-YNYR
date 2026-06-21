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
st.title("📁 Gestión Documental de Iniciativas IT")
# =====================================================
# MENÚ
# =====================================================

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "🏠 Inicio",
        "📝 Registrar Documento",
        "✅ Aprobaciones",
        "📚 Repositorio",
        "🔄 Control de Versiones",
        "🔍 Consulta",
        "📊 Dashboard"
    ]
)

# =====================================================
# INICIO
# =====================================================

if menu == "🏠 Inicio":

    st.markdown("""
    ## Esta solución permite gestionar el ciclo de vida documental de forma integral, desde el registro y revisión hasta la aprobación, publicación y consulta, garantizando control de versiones, trazabilidad y acceso oportuno a la información para la toma de decisiones.
    
    st.markdown("""
    ### Funcionalidades

    ⭐ Registro documental
    ⭐ Flujo de aprobación
    ⭐ Repositorio centralizado
    ⭐ Consulta documental
    ⭐ Control de versiones
    ⭐ Dashboard de indicadores
    """)

# =====================================================
# REGISTRO
# =====================================================

if menu == "📝 Registrar Documento":

    st.header("Registro de Documento")

    nombre = st.text_input("Nombre")

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

if menu == "✅ Aprobaciones":

    st.header("Bandeja de Aprobaciones")

    if len(st.session_state.pendientes) == 0:

        st.info("No existen documentos pendientes")

    else:

        nombres = [
            doc["Documento"]
            for doc in st.session_state.pendientes
        ]

        seleccion = st.selectbox(
            "Seleccione documento",
            ["-- Seleccione --"] + nombres
        )

        if seleccion != "-- Seleccione --":

            doc = next(
                d
                for d in st.session_state.pendientes
                if d["Documento"] == seleccion
            )

            st.subheader("Información")

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
                    "Descargar documento",
                    doc["Contenido"],
                    file_name=doc["NombreArchivo"]
                )

            observaciones = st.text_area(
                "Observaciones"
            )

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

if menu == "📚 Repositorio":

    st.header("Repositorio Documental")

    if len(st.session_state.aprobados) == 0:

        st.info("No existen documentos aprobados")

    else:

        df = pd.DataFrame(st.session_state.aprobados)

        columnas = [
            "Documento",
            "Tipo",
            "Version",
            "Responsable",
            "Estado",
            "Fecha"
        ]

        st.dataframe(
            df[columnas],
            use_container_width=True
        )

# =====================================================
# CONTROL VERSIONES
# =====================================================

if menu == "🔄 Control de Versiones":

    st.header("Control de Versiones")

    if len(st.session_state.aprobados) == 0:

        st.info("No existen documentos aprobados")

    else:

        df = pd.DataFrame(
            st.session_state.aprobados
        )

        st.dataframe(
            df[
                [
                    "Documento",
                    "Version",
                    "Responsable",
                    "Fecha"
                ]
            ],
            use_container_width=True
        )

# =====================================================
# CONSULTA
# =====================================================

if menu == "🔍 Consulta":

    st.header("Consulta Documental")

    criterio = st.text_input(
        "Buscar documento"
    )

    if criterio:

        df = pd.DataFrame(
            st.session_state.aprobados
        )

        if not df.empty:

            resultado = df[
                df["Documento"].str.contains(
                    criterio,
                    case=False,
                    na=False
                )
            ]

            st.dataframe(
                resultado,
                use_container_width=True
            )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "📊 Dashboard":

    st.header("Indicadores de Gestión")

    pendientes = len(st.session_state.pendientes)
    aprobados = len(st.session_state.aprobados)
    rechazados = len(st.session_state.rechazados)

    total = pendientes + aprobados + rechazados

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total)
    col2.metric("Pendientes", pendientes)
    col3.metric("Aprobados", aprobados)
    col4.metric("Rechazados", rechazados)

    if total > 0:

        estados = pd.DataFrame({
            "Estado": [
                "Pendientes",
                "Aprobados",
                "Rechazados"
            ],
            "Cantidad": [
                pendientes,
                aprobados,
                rechazados
            ]
        })

        st.subheader("Distribución del Flujo")

        st.bar_chart(
            estados.set_index("Estado")
        )

        porcentaje_aprobacion = round(
            (aprobados / total) * 100,
            2
        )

        st.metric(
            "Porcentaje de aprobación",
            f"{porcentaje_aprobacion}%"
        )

    else:
        st.info("No existen datos para mostrar")
