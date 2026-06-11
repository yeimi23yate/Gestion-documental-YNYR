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
        "✅ Aprobaciones",
        "📚 Repositorio Documental",
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
if menu == "📝 Registrar Documento":

    st.title("📝 Registro de Documento")

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

    archivo = st.file_uploader(
        "📎 Adjuntar documento",
        type=["pdf", "docx", "xlsx", "txt"]
    )

    st.divider()

    if st.button("📤 Enviar a revisión"):

        if nombre and version and responsable and archivo is not None:

            documento = {
                "Documento": nombre,
                "Tipo": tipo,
                "Versión": version,
                "Responsable": responsable,
                "Estado": "Registrado",
                "Contenido": archivo.read(),
                "NombreArchivo": archivo.name
            }

            st.session_state.documento_pendiente = documento

            st.success("Documento enviado correctamente al flujo de aprobación.")

        else:
            st.warning("Completa todos los campos y adjunta un archivo.")
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
# CONTROL DE VERSIONES
# =====================================================

if menu == "🔄 Control de Versiones":

    st.title("🔄 Control de Versiones")

    if len(st.session_state.documentos) == 0:

        st.info(
            "No existen documentos aprobados para consultar versiones."
        )

    else:

        documento_seleccionado = st.selectbox(
            "Seleccione un documento",
            [
                doc["Documento"]
                for doc in st.session_state.documentos
            ]
        )

        documento = next(
            doc
            for doc in st.session_state.documentos
            if doc["Documento"] == documento_seleccionado
        )

        historial = pd.DataFrame({
            "Documento": [documento["Documento"]],
            "Versión": [documento["Versión"]],
            "Responsable": [documento["Responsable"]],
            "Estado": [documento["Estado"]]
        })

        st.dataframe(
            historial,
            use_container_width=True
        )

        st.subheader("📄 Información de la versión")

        st.write(
            f"**Documento:** {documento['Documento']}"
        )

        st.write(
            f"**Versión actual:** {documento['Versión']}"
        )

        st.write(
            f"**Responsable:** {documento['Responsable']}"
        )

        st.write(
            f"**Estado:** {documento['Estado']}"
        )

        st.text_area(
            "Contenido",
            documento["Contenido"],
            height=250,
            disabled=True
        )

        if st.button("➕ Crear Nueva Versión"):

            st.success(
                f"Se ha generado una nueva versión basada en la versión {documento['Versión']}."
            )

if menu == "✅ Aprobaciones":

    st.title("🔄 Workflow de Gestión Documental")

    if st.session_state.documento_pendiente is None:

        st.warning("No existen documentos pendientes por aprobar.")

    else:

        doc = st.session_state.documento_pendiente

        # ==========================
        # FLUJO
        # ==========================
        st.info("📝 Registrado → 👀 En revisión → ✅ Aprobado → 📚 Publicado")
        st.progress(50)

        st.divider()

        col1, col2 = st.columns([1, 2])

        # ==========================
        # INFORMACIÓN
        # ==========================
        with col1:

            st.subheader("📋 Información del Documento")

            st.write(f"**Documento:** {doc['Documento']}")
            st.write(f"**Versión:** {doc['Versión']}")
            st.write(f"**Responsable:** {doc['Responsable']}")
            st.write(f"**Estado:** {doc['Estado']}")

            # Observaciones previas si existen
            if "Observaciones" in doc:
                st.write("**Observaciones anteriores:**")
                st.info(doc["Observaciones"])

        # ==========================
        # VISTA PREVIA VISUAL
        # ==========================
        with col2:

            st.subheader("👁️ Vista previa del documento")

            archivo_nombre = doc.get("NombreArchivo", "")

            if archivo_nombre.endswith(".pdf"):

                st.download_button(
                    label="📥 Descargar PDF",
                    data=doc["Contenido"],
                    file_name=archivo_nombre,
                    mime="application/pdf"
                )

                st.components.v1.html(
                    f"""
                    <iframe
                        src="data:application/pdf;base64,{doc['Contenido'].decode() if isinstance(doc['Contenido'], bytes) else doc['Contenido']}"
                        width="100%"
                        height="500px">
                    </iframe>
                    """,
                    height=500
                )

            else:

                st.info("📄 Este archivo no tiene vista previa visual disponible.")
                st.download_button(
                    "📥 Descargar documento",
                    data=doc["Contenido"],
                    file_name=archivo_nombre
                )

        st.divider()

        # ==========================
        # OBSERVACIONES DEL REVISOR
        # ==========================
        st.subheader("📝 Observaciones del Revisor")

        observaciones = st.text_area(
            "Escribe observaciones sobre el documento",
            placeholder="Ej: Ajustar formato, corregir versión, validar contenido..."
        )

        st.divider()

        # ==========================
        # ACCIONES DEL FLUJO
        # ==========================
        colA, colB = st.columns(2)

        with colA:

            if st.button("📤 Enviar a revisión"):

                doc["Estado"] = "En revisión"
                doc["Observaciones"] = observaciones

                st.session_state.documento_pendiente = doc

                st.success("📤 Documento enviado a revisión correctamente.")

        with colB:

            if st.button("❌ Rechazar Documento"):

                doc["Estado"] = "Rechazado"
                doc["Observaciones"] = observaciones

                st.session_state.documento_pendiente = None

                st.error("❌ Documento rechazado. Requiere ajustes.")
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
