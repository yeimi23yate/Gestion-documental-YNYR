import streamlit as st
import pandas as pd
import base64

# =====================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================

st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📈",
    layout="wide"
)
import os

st.write("logo.png existe:", os.path.exists("logo.png"))
# =====================================================
# FUNCIÓN PARA CARGAR IMAGEN DE FONDO
# =====================================================

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Logo para marca de agua
logo = get_base64("logo.png")

# =====================================================
# ESTILOS - MARCA DE AGUA
# =====================================================

st.markdown(
    f"""
    <style>

    .stApp::before {{
        content: "";
        position: fixed;
        top: 50%;
        left: 60%;
        width: 250px;
        height: 250px;
        transform: translate(-50%, -50%);
        background-image: url("data:image/png;base64,{logo}");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.03;
        pointer-events: none;
        z-index: 0;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# ENCABEZADO
# =====================================================

st.image("log_CCB.png", width=150)
st.image("logo.png", width=300)

# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.title("🗃️ Gestión Documental")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "🏠 Inicio",
        "📝 Registrar Documento",
        "🔄 Control de Versiones",
        "✅ Aprobaciones",
        "🔍 Consulta",
        "📊 Dashboard"
    ]
)

# =====================================================
# INICIO
# =====================================================

if menu == "🏠 Inicio":

    st.title("Documentación de Iniciativas IT")

    st.markdown(
        """
        <p style='margin-top:-20px; color:gray; font-size:16px;'>
        Modelo de Gestión Documental Centralizada basado en Azure DevOps
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("""
    Este prototipo permite:

    🚀 Centralizar documentación

    🚀 Controlar versiones

    🚀 Gestionar aprobaciones

    🚀 Consultar información actualizada

    🚀 Visualizar indicadores
    """)

# =====================================================
# REGISTRO DOCUMENTAL
# =====================================================

if menu == "📝 Registrar Documento":

    st.title("Registro de Documento")

    nombre = st.text_input(
        "Nombre del documento"
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

    version = st.text_input("Versión")

    responsable = st.text_input(
        "Responsable"
    )

    if st.button("Guardar Documento"):

        st.success(
            "Documento registrado correctamente"
        )

# =====================================================
# CONTROL DE VERSIONES
# =====================================================

if menu == "🔄 Control de Versiones":

    st.title("Control de Versiones")

    documento = st.selectbox(
        "Seleccione documento",
        [
            "CP_Login",
            "Manual_App"
        ]
    )

    st.write("Versión actual: 1.0")

    if st.button("Crear Nueva Versión"):

        st.success(
            "Nueva versión creada: 1.1"
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
# CONSULTA
# =====================================================

if menu == "🔍 Consulta":

    st.title("Consulta Documental")

    buscar = st.text_input(
        "Buscar Documento"
    )

    if buscar:

        st.table({
            "Documento": ["CP_Login"],
            "Versión": ["1.1"],
            "Estado": ["Aprobado"]
        })

# =====================================================
# DASHBOARD
# =====================================================

if menu == "📊 Dashboard":

    st.title("Indicadores")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Documentos",
        "25"
    )

    col2.metric(
        "Aprobados",
        "20"
    )

    col3.metric(
        "Pendientes",
        "5"
    )

    datos = pd.DataFrame({
        "Estado": [
            "Aprobados",
            "Pendientes"
        ],
        "Cantidad": [
            20,
            5
        ]
    })

    st.bar_chart(
        datos.set_index("Estado")
    )
