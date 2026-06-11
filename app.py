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
        "🔄 Control de Versiones",
        "✅ WorkFlow",
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
# REGISTRO DOCUMENTAL
# =====================================================

if menu == "📝 Registrar Documento":

    st.title("📝 Registro de Documento")

    col1, col2 = st.columns(2)

    with col1:

        nombre = st.text_input(
            "Nombre del documento"
        )

        iniciativa = st.selectbox(
            "Iniciativa",
            [
                "Marketplace",
                "Crédito Digital",
                "Canales",
                "Seguros"
            ]
        )

        tipo = st.selectbox(
            "Tipo de documento",
            [
                "Caso de Prueba",
                "Manual",
                "Requerimiento",
                "Documento Técnico"
            ]
        )

    with col2:

        version = st.text_input(
            "Versión"
        )

        responsable = st.text_input(
            "Responsable"
        )

        estado = st.selectbox(
            "Estado",
            [
                "Borrador",
                "En revisión",
                "Aprobado"
            ]
        )

    archivo = st.file_uploader(
        "Adjuntar documento",
        type=["pdf", "docx", "xlsx"]
    )

    if st.button("Guardar Documento"):

        st.success(
            "Documento registrado correctamente"
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

    st.title("Aprobación Documental")

    st.write("Documento: CP_Login")

    estado = st.selectbox(
        "Estado",
        [
            "Pendiente",
            "Aprobado",
            "Rechazado"
        ]
    )

    st.write("Estado actual:", estado)

    if st.button("Aprobar"):

        st.success(
            "Documento aprobado"
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
