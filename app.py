import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================

st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📁",
    layout="wide"
)
# =====================================================
# VARIABLES DE SESIÓN
# =====================================================

if "documentos" not in st.session_state:
    st.session_state.documentos = []

if "documento_pendiente" not in st.session_state:
    st.session_state.documento_pendiente = None
# =====================================================
# ENCABEZADO
# =====================================================

st.image("log_CCB.png", width=180)

# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.title("🗃️ Gestión Documental")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "🏠 Inicio",
        "📝 Registrar Documento",
        "📚 Repositorio Documental",
        "✅ Aprobaciones",
        "🔄 Control de Versiones",
        "🔍 Consulta",
        "📊 Dashboard"
    ]
)

# =====================================================
# INICIO
# =====================================================

if menu == "🏠 Inicio":

    st.title("📁 Gestión Documental de Iniciativas IT")

    st.markdown("""
    ### Modelo de Gestión Documental Centralizada basado en Azure DevOps

    Este prototipo permite centralizar la documentación de las iniciativas IT,
    garantizando trazabilidad, control de versiones, aprobaciones y consulta
    oportuna de la información.
    """)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Documentos", "125")
    col2.metric("Versiones", "320")
    col3.metric("Aprobaciones", "98%")
    col4.metric("Usuarios", "45")

    st.divider()

    st.subheader("Beneficios de la Solución")

    st.write("""
    ✅ Centralización documental

    ✅ Control de versiones

    ✅ Gestión de aprobaciones

    ✅ Trazabilidad de cambios

    ✅ Consulta rápida de información

    ✅ Indicadores para la toma de decisiones
    """)

# =====================================================
# REPOSITORIO DOCUMENTAL
# =====================================================

if menu == "📚 Repositorio Documental":

    st.title("📚 Repositorio Documental")

    if len(st.session_state.documentos) == 0:

        st.info(
            "No existen documentos aprobados."
        )

    else:

        documentos = pd.DataFrame(
            st.session_state.documentos
        )

        st.dataframe(
            documentos,
            use_container_width=True
        )
# =====================================================
# REPOSITORIO DOCUMENTAL
# =====================================================

if menu == "📚 Repositorio Documental":

    st.title("📚 Repositorio Documental")

    documentos = pd.DataFrame({
        "Documento": [
            "CP Login",
            "HU Marketplace",
            "Manual Usuario",
            "Arquitectura Solución",
            "Plan de Pruebas"
        ],
        "Versión": [
            "1.2",
            "2.0",
            "1.5",
            "3.1",
            "2.4"
        ],
        "Estado": [
            "Aprobado",
            "Aprobado",
            "En revisión",
            "Aprobado",
            "Aprobado"
        ],
        "Responsable": [
            "Analista QA",
            "Product Owner",
            "Líder QA",
            "Arquitecto",
            "Analista QA"
        ]
    })

    st.dataframe(
        documentos,
        use_container_width=True
    )

# =====================================================
# CONTROL DE VERSIONES
# =====================================================

if menu == "🔄 Control de Versiones":

    st.title("🔄 Control de Versiones")

    historial = pd.DataFrame({
        "Versión": [
            "1.0",
            "1.1",
            "1.2",
            "1.3"
        ],
        "Fecha": [
            "01/05/2026",
            "15/05/2026",
            "01/06/2026",
            "10/06/2026"
        ],
        "Responsable": [
            "Analista QA",
            "Analista QA",
            "Líder QA",
            "Líder QA"
        ],
        "Descripción": [
            "Versión inicial",
            "Actualización de contenido",
            "Ajustes funcionales",
            "Corrección de observaciones"
        ]
    })

    st.dataframe(
        historial,
        use_container_width=True
    )

    if st.button("Crear Nueva Versión"):

        st.success(
            "Versión 1.4 creada correctamente"
        )

# =====================================================
# APROBACIONES
# =====================================================

if menu == "✅ Aprobaciones":

    st.title("🔄 Workflow de Gestión Documental")

    if st.session_state.documento_pendiente is None:

        st.warning(
            "No existen documentos pendientes por aprobar."
        )

    else:

        doc = st.session_state.documento_pendiente

        st.info(
            "📝 Registrado → 👀 En revisión → ✅ Aprobado → 📚 Publicado"
        )

        st.progress(75)

        st.divider()

        col1, col2 = st.columns([1, 2])

        # Información del documento

        with col1:

            st.subheader("📋 Información del Documento")

            st.write(f"**Documento:** {doc['Documento']}")
            st.write(f"**Versión:** {doc['Versión']}")
            st.write(f"**Responsable:** {doc['Responsable']}")
            st.write(f"**Estado:** {doc['Estado']}")

        # Vista previa

        with col2:

            st.subheader("👁️ Vista previa")

            st.text_area(
                "Contenido",
                doc["Contenido"],
                height=300,
                disabled=True
            )

        st.divider()

        observaciones = st.text_area(
            "📝 Observaciones del Revisor"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("✅ Aprobar Documento"):

                doc["Estado"] = "Aprobado"
                doc["Observaciones"] = observaciones

                st.session_state.documentos.append(doc)

                st.session_state.documento_pendiente = None

                st.success(
                    "Documento aprobado y publicado en el repositorio documental."
                )

        with col2:

            if st.button("❌ Rechazar Documento"):

                st.error(
                    "Documento rechazado. Se requiere ajuste por parte del responsable."
                )
# =====================================================
# CONSULTA DOCUMENTAL
# =====================================================

if menu == "🔍 Consulta":

    st.title("🔍 Consulta Documental")

    buscar = st.text_input(
        "Buscar Documento"
    )

    if buscar:

        resultado = pd.DataFrame({
            "Documento": ["CP Login"],
            "Versión": ["1.3"],
            "Estado": ["Aprobado"],
            "Responsable": ["Analista QA"],
            "Fecha": ["10/06/2026"]
        })

        st.dataframe(
            resultado,
            use_container_width=True
        )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "📊 Dashboard":

    st.title("📊 Indicadores de Gestión Documental")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Documentos Centralizados",
        "125",
        "+20%"
    )

    col2.metric(
        "Tiempo de Consulta",
        "2 min",
        "-80%"
    )

    col3.metric(
        "Documentos Actualizados",
        "95%",
        "+15%"
    )

    st.divider()

    st.subheader(
        "Crecimiento del Repositorio Documental"
    )

    datos = pd.DataFrame({
        "Mes": [
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun"
        ],
        "Documentos": [
            20,
            35,
            50,
            80,
            110,
            125
        ]
    })

    st.line_chart(
        datos.set_index("Mes")
    )

    st.subheader(
        "Estado de los Documentos"
    )

    estados = pd.DataFrame({
        "Estado": [
            "Aprobados",
            "En revisión",
            "Pendientes"
        ],
        "Cantidad": [
            95,
            20,
            10
        ]
    })

    st.bar_chart(
        estados.set_index("Estado")
    )
