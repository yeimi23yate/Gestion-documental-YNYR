import streamlit as st
import pandas as pd

from datetime import datetime
import os

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
        "📊 Dashboard",
        "📜 Auditoría"
    ]
)
# =====================================================
# CREACIÓN DE ARCHIVOS
# =====================================================

if not os.path.exists("documentos.csv"):

    pd.DataFrame(
        columns=[
            "Documento",
            "Version",
            "Responsable",
            "Estado",
            "Contenido",
            "Observaciones"
        ]
    ).to_csv(
        "documentos.csv",
        index=False
    )

if not os.path.exists("auditoria.csv"):

    pd.DataFrame(
        columns=[
            "Fecha",
            "Accion",
            "Documento",
            "Usuario"
        ]
    ).to_csv(
        "auditoria.csv",
        index=False
    )

if not os.path.exists("versiones.csv"):

    pd.DataFrame(
        columns=[
            "Documento",
            "Version",
            "Fecha",
            "Responsable",
            "Descripcion"
        ]
    ).to_csv(
        "versiones.csv",
        index=False
    )

def registrar_auditoria(
    accion,
    documento,
    usuario
):

    auditoria = pd.read_csv(
        "auditoria.csv"
    )

    nuevo = pd.DataFrame(
        [{
            "Fecha": datetime.now(),
            "Accion": accion,
            "Documento": documento,
            "Usuario": usuario
        }]
    )

    auditoria = pd.concat(
        [auditoria, nuevo],
        ignore_index=True
    )

    auditoria.to_csv(
        "auditoria.csv",
        index=False
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
# REGISTRAR DOCUMENTO
# =====================================================

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
    "Estado": "En revisión",
    "Archivo": archivo.name if archivo else "",
    "Aprobador": "",
    "Observaciones": ""
}
            st.session_state.documento_pendiente = documento

            st.success("Documento enviado correctamente al flujo de aprobación.")

        else:
            st.warning("Completa todos los campos y adjunta un archivo.")

{
    "Documento": nombre,
    "Versión": version,
    "Responsable": responsable,
    "Estado": "En revisión"
}

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

        # Selección de registros por página

        registros_por_pagina = st.selectbox(
            "Registros por página",
            [5, 10, 20, 50],
            key="repo_paginacion"
        )

        total_paginas = max(
            1,
            (len(documentos) + registros_por_pagina - 1)
            // registros_por_pagina
        )

        pagina = st.number_input(
            "Página",
            min_value=1,
            max_value=total_paginas,
            value=1,
            key="repo_pagina"
        )

        inicio = (pagina - 1) * registros_por_pagina
        fin = inicio + registros_por_pagina

        # Columnas para mostrar

        columnas = [
            "Documento",
            "Tipo",
            "Versión",
            "Responsable",
            "Estado",
            "Aprobador",
            "Archivo",
            "Observaciones"
        ]

        # Crear columnas faltantes si aún no existen

        for col in columnas:

            if col not in documentos.columns:
                documentos[col] = ""

        st.dataframe(
            documentos[columnas].iloc[inicio:fin],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Página {pagina} de {total_paginas}"
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
        
        if st.button("➕ Crear Nueva Versión"):

            st.success(
                f"Se ha generado una nueva versión basada en la versión {documento['Versión']}."
            )
# ==========================
# APROBACIONES
# ==========================

if menu == "✅ Aprobaciones":

    import base64

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

    if "Observaciones" in doc and doc["Observaciones"]:

        st.write("**Observaciones anteriores:**")

        st.info(doc["Observaciones"])

# ==========================
# VISTA PREVIA
# ==========================

with col2:

    st.subheader("👁️ Vista previa del documento")

    archivo_nombre = doc.get(
        "NombreArchivo",
        "documento"
    )

    st.info(
        "📄 Vista previa mediante descarga del archivo"
    )

    st.download_button(
        label="📥 Descargar documento",
        data=doc["Contenido"],
        file_name=archivo_nombre,
        mime="application/octet-stream"
    )

st.divider()

# ==========================
# APROBADOR
# ==========================

aprobador = st.text_input(
    "Nombre del Aprobador",
    key="aprobador_workflow"
)

# ==========================
# OBSERVACIONES
# ==========================

st.subheader(
    "📝 Observaciones del Revisor"
)

observaciones = st.text_area(
    "Escribe observaciones sobre el documento",
    key="observaciones_workflow"
)

st.divider()

# ==========================
# ACCIONES
# ==========================

colA, colB = st.columns(2)

with colA:

    if st.button("📤 Aprobar documento"):

        doc["Estado"] = "Aprobado"
        doc["Observaciones"] = observaciones
        doc["Aprobador"] = aprobador

        st.session_state.documentos.append(doc)

        st.session_state.documento_pendiente = None

        st.success(
            "✅ Documento aprobado y publicado en el repositorio."
        )

with colB:

    if st.button("❌ Rechazar Documento"):

        doc["Estado"] = "Rechazado"
        doc["Observaciones"] = observaciones
        doc["Aprobador"] = aprobador

        st.session_state.documento_pendiente = None

        st.error(
            "❌ Documento rechazado."
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
# =====================================================
# AUDITORIA
# =====================================================

if menu == "📜 Auditoría":

    st.title(
        "📜 Historial de Auditoría"
    )

    auditoria = pd.read_csv(
        "auditoria.csv"
    )

    registros_por_pagina = st.selectbox(
        "Registros por página",
        [5,10,20,50]
    )

    total_paginas = max(
        1,
        (
            len(auditoria)
            + registros_por_pagina
            - 1
        )
        // registros_por_pagina
    )

    pagina = st.number_input(
        "Página",
        min_value=1,
        max_value=total_paginas,
        value=1
    )

    inicio = (
        pagina - 1
    ) * registros_por_pagina

    fin = inicio + registros_por_pagina

    st.dataframe(
        auditoria.iloc[
            inicio:fin
        ],
        use_container_width=True
    )

    st.write(
        f"Página {pagina} de {total_paginas}"
    )
