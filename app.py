import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Plataforma de Estudio Médico", 
    page_icon="🎓", 
    layout="wide"
)

st.title("🩺 Mi Plataforma Clínica de Estudio")
st.markdown("---")

# ==========================================
# 2. BARRA LATERAL (HISTORIAL)
# ==========================================
with st.sidebar:
    st.header("📁 Mis Apuntes")
    st.caption("Historial de estudio")
    
    # Botón de ejemplo para visualizar cómo se verán los archivos guardados
    st.button("📄 Ejemplo: Patología Biliar") 
    
    st.info("Al hacer clic en un apunte, se abrirá en la pantalla principal para que puedas editarlo o descargarlo (PDF/Word).")

# ==========================================
# 3. PESTAÑAS PRINCIPALES (LA TRINIDAD DE ORO)
# ==========================================
tab_apuntes, tab_anki, tab_tablas = st.tabs([
    "📝 Apuntes y Diapos", 
    "🎴 Fábrica de Anki", 
    "📊 Tablas Med Interna"
])

# ------------------------------------------
# PESTAÑA 1: APUNTES ESTRUCTURADOS Y DIAPOS
# ------------------------------------------
with tab_apuntes:
    st.subheader("Transformador de Clases a Formato Clínico")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        texto_crudo = st.text_area("1. Pega aquí el texto bruto de tu clase (transcrito con otra app):", height=150)
    with col_input2:
        archivo_clase = st.file_uploader("2. Sube la presentación del profe (.pdf, .pptx) para extraer imágenes:", type=["pdf", "pptx"])
        
    if st.button("✨ Estructurar Apunte y Extraer Diapos", type="primary"):
        st.info("Próximamente: Aquí la IA estructurará el texto con tu formato ideal y recortará las imágenes.")
        
    st.markdown("---")
    
    col_texto, col_imagenes = st.columns([3, 1])
    with col_texto:
        st.text_area("Apunte estructurado listo para editar:", height=300, value="Aquí aparecerá el apunte médico ordenado con viñetas y negritas...")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        col_btn1.button("💾 Guardar en Mis Apuntes")
        col_btn2.button("📤 Exportar a PDF")
        col_btn3.button("📝 Descargar en Word")
        
    with col_imagenes:
        st.info("🖼️ Banco de Diapositivas")
        st.caption("Las imágenes de la presentación aparecerán aquí para arrastrarlas al apunte.")

# ------------------------------------------
# PESTAÑA 2: FÁBRICA DE ANKI
# ------------------------------------------
with tab_anki:
    st.subheader("Generador Automático de Tarjetas")
    st.write("Genera flashcards directas cruzando tus apuntes con literatura médica.")
    
    col_fuente1, col_fuente2 = st.columns(2)
    with col_fuente1:
        apuntes_seleccionados_anki = st.multiselect(
            "📚 1. Selecciona los apuntes base:", 
            ["Apunte actual en pantalla", "Apuntes guardados (Próximamente)"], 
            default=["Apunte actual en pantalla"]
        )
    with col_fuente2:
        bibliografia_anki = st.file_uploader(
            "📎 2. Sube bibliografía complementaria (Opcional - PDF, DOCX):", 
            type=["pdf", "docx"], 
            accept_multiple_files=True,
            key="biblio_anki"
        )

    if st.button("🧠 Crear Tarjetas Anki"):
        st.info("Próximamente: La IA extraerá los conceptos clave fusionando tus apuntes y la bibliografía.")
        
    st.data_editor(
        {
            "Frente (Pregunta)": ["¿Fisiopatología principal de la Colecistitis?"],
            "Reverso (Respuesta)": ["Obstrucción del conducto cístico, generalmente por un lito."],
            "Aprobar": [True]
        },
        num_rows="dynamic",
        use_container_width=True
    )
    st.button("🟩 DESCARGAR MAZO (.apkg)", type="primary")

# ------------------------------------------
# PESTAÑA 3: TABLAS DE MEDICINA INTERNA
# ------------------------------------------
with tab_tablas:
    st.subheader("Generador de Tablas de Alto Rendimiento")
    st.write("Compara patologías cruzando la clase del profesor con guías clínicas o papers.")
    
    col_fuente3, col_fuente4 = st.columns(2)
    with col_fuente3:
        apuntes_seleccionados_tablas = st.multiselect(
            "📚 1. Selecciona los apuntes base:", 
            ["Apunte actual en pantalla", "Apuntes guardados (Próximamente)"], 
            default=["Apunte actual en pantalla"],
            key="select_tablas"
        )
    with col_fuente4:
        bibliografia_tablas = st.file_uploader(
            "📎 2. Sube guías o papers complementarios (Opcional - PDF):", 
            type=["pdf", "docx"], 
            accept_multiple_files=True,
            key="biblio_tablas"
        )
        
    tema_tabla = st.text_input("¿De qué temas quieres generar la tabla? (Ej: Patologías biliares)")
    if st.button("🚀 Generar Tabla Comparativa", type="primary"):
        st.info("Próximamente: La IA armará la tabla clínica perfecta cruzando ambas fuentes de información.")
        
    st.markdown("---")
    st.write("**Vista Previa Editable:**")
    
    st.data_editor(
        {
            "Enfermedad": ["Colecistitis", "Colangitis"],
            "Fisiopatología": ["Obstrucción del conducto cístico.", "Infección de la vía biliar."],
            "Cuadro Clínico": ["Fiebre, dolor, Murphy (+).", "Fiebre, Ictericia, Dolor (Tríada de Charcot)."],
            "Diagnóstico": ["Eco: Pared engrosada.", "Eco + Alteración de pruebas hepáticas."],
            "Tratamiento": ["Colecistectomía.", "Antibióticos y Drenaje biliar."]
        },
        num_rows="dynamic",
        use_container_width=True
    )
    
    # Nuevos botones de descarga que incluyen PDF
    col_btn_tabla1, col_btn_tabla2, col_btn_tabla3 = st.columns(3)
    col_btn_tabla1.button("📥 Descargar Tabla en Excel (.csv)", type="primary")
    col_btn_tabla2.button("📝 Descargar Tabla en Word")
    col_btn_tabla3.button("📤 Descargar Tabla en PDF")
