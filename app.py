import streamlit as st
import pandas as pd

# =====================================
# CONFIGURACIÓN DE PÁGINA
# =====================================

st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📈",
    layout="wide"
)

# =====================================
# MARCA DE AGUA
# =====================================

st.markdown("""
<style>

.stApp {
    background-image: url("https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/logo.png");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 300px;
    background-attachment: fixed;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# MENÚ LATERAL
# =====================================

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

# =====================================
# INICIO
# =====================================

if menu == "🏠 Inicio":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image("log_CCB.png", width=180)

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

# =====================================
# REGISTRO DOCUMENTO
# =====================================

if menu == "📝 Registrar Documento":

    st.title("Registro de Documento")

    nombre = st.text_input("Nombre del documento")

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

    responsable = st.text_input("Responsable")

    if st.button("Guardar Documento"):
        st.success("Documento registrado correctamente")

# =====================================
# VERSIONES
# =====================================

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
        st.success("Nueva versión creada: 1.1")

# =====================================
# APROBACIONES
# =====================================

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
        st.success("Documento aprobado")

# =====================================
# CONSULTA
# =====================================

if menu == "🔍 Consulta":

    st.title("Consulta Documental")

    buscar = st.text_input("Buscar Documento")

    if buscar:

        st.table({
            "Documento": ["CP_Login"],
            "Versión": ["1.1"],
            "Estado": ["Aprobado"]
        })

# =====================================
# DASHBOARD
# =====================================

if menu == "📊 Dashboard":

    st.title("Indicadores")

    col1, col2, col3 = st.columns(3)

    col1.metric("Documentos", "25")
    col2.metric("Aprobados", "20")
    col3.metric("Pendientes", "5")

    datos = pd.DataFrame({
        "Estado": ["Aprobados", "Pendientes"],
        "Cantidad": [20, 5]
    })

    st.bar_chart(datos.set_index("Estado"))
