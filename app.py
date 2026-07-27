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
    st.caption("Documentos recientes")
    st.button("📄 Ingreso Hospital Regional")
    st.button("📄 Anamnesis - Paciente Cama 4")
    st.button("📄 Apuntes Medicina Interna")

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
        col_btn1, col_btn2 = st.columns(2)
        col_btn1.button("📤 Exportar a PDF")
        col_btn2.button("📝 Descargar en Word")
        
    with col_imagenes:
        st.info("🖼️ Banco de Diapositivas")
        st.caption("Las imágenes de la presentación aparecerán aquí para arrastrarlas al apunte.")

# ------------------------------------------
# PESTAÑA 2: FÁBRICA DE ANKI
# ------------------------------------------
with tab_anki:
    st.subheader("Generador Automático de Tarjetas")
    st.write("Genera flashcards directas a partir de tu apunte estructurado.")
    if st.button("🧠 Crear Tarjetas Anki"):
        st.info("Próximamente: La IA extraerá los conceptos clave para memorizar.")
        
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
    st.write("Ideal para comparar patologías (Fisiopatología, Cuadro Clínico, Diagnóstico, Tratamiento).")
    
    tema_tabla = st.text_input("¿De qué temas quieres generar la tabla? (Ej: Patologías biliares)")
    if st.button("🚀 Generar Tabla Comparativa", type="primary"):
        st.info("Próximamente: La IA armará la tabla clínica perfecta.")
        
    st.markdown("---")
    st.write("**Vista Previa:**")
    st.markdown("| Enfermedad | Fisiopatología | Cuadro Clínico | Diagnóstico | Tratamiento |\n| :--- | :--- | :--- | :--- | :--- |\n| **Colecistitis** | Obstrucción cístico. | Fiebre, Murphy (+). | Eco: Pared >4mm. | Colecistectomía. |")
