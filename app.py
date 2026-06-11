import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gestión Documental",
    page_icon="📁",
    layout="wide"
)
st.sidebar.title("📁 Gestión Documental")

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

if menu == "🏠 Inicio":

    st.title("Documentación de iniciativas IT")

    st.subheader(
        "Documentación centralizada con servicios Azure DevOps"
    )

    st.write("""
    Este prototipo permite:

    🚀 Centralizar documentación
    
    🚀 Controlar versiones
    
    🚀 Gestionar aprobaciones
    
    🚀 Consultar información actualizada
    
    🚀 Visualizar indicadores
    
    """)

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

if menu == "🔍 Consulta":

    st.title("Consulta Documental")

    buscar = st.text_input(
        "Buscar Documento"
    )

    if buscar:

        st.table({
            "Documento":["CP_Login"],
            "Versión":["1.1"],
            "Estado":["Aprobado"]
        })

if menu == "📊 Dashboard":

    st.title("Indicadores")

    col1,col2,col3 = st.columns(3)

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
        "Estado":[
            "Aprobados",
            "Pendientes"
        ],
        "Cantidad":[
            20,
            5
        ]
    })

    st.bar_chart(
        datos.set_index("Estado")
    )
