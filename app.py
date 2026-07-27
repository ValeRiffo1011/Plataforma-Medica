import streamlit as st
import google.generativeai as genai

# ==========================================
# 0. CONFIGURACIÓN DE LA IA Y MEMORIA
# ==========================================
# Cargar la llave desde los secretos de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Crear la memoria para guardar el apunte generado
if "apunte_generado" not in st.session_state:
    st.session_state.apunte_generado = "Aquí aparecerá el apunte médico ordenado con viñetas y negritas..."

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Plataforma de Estudio Médico", page_icon="🎓", layout="wide")

st.title("🩺 Mi Plataforma Clínica de Estudio")
st.markdown("---")

# ==========================================
# 2. BARRA LATERAL (HISTORIAL)
# ==========================================
with st.sidebar:
    st.header("📁 Mis Apuntes")
    st.caption("Historial de estudio")
    st.button("📄 Ejemplo: Patología Biliar") 
    st.info("Al hacer clic en un apunte, se abrirá en la pantalla principal para que puedas editarlo o descargarlo (PDF/Word).")

# ==========================================
# 3. PESTAÑAS PRINCIPALES
# ==========================================
tab_apuntes, tab_anki, tab_tablas = st.tabs(["📝 Apuntes y Diapos", "🎴 Fábrica de Anki", "📊 Tablas Med Interna"])

# ------------------------------------------
# PESTAÑA 1: APUNTES ESTRUCTURADOS Y DIAPOS
# ------------------------------------------
with tab_apuntes:
    st.subheader("Transformador de Clases a Formato Clínico")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        texto_crudo = st.text_area("1. Pega aquí el texto bruto de tu clase:", height=150)
    with col_input2:
        archivo_clase = st.file_uploader("2. Sube la presentación (.pdf, .pptx):", type=["pdf", "pptx"])
        
    if st.button("✨ Estructurar Apunte", type="primary"):
        if texto_crudo.strip() == "":
            st.warning("⚠️ Por favor, pega el texto de la clase primero.")
        else:
            with st.spinner("🧠 Ordenando y estructurando clínicamente tu apunte..."):
                try:
                    # Instrucciones estrictas para la IA
                    modelo = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"""
                    Toma la siguiente transcripción bruta de una clase de medicina y transfórmala en un apunte clínico de alto rendimiento.
                    Debes usar la siguiente estructura estrictamente:
                    - Títulos principales para los temas.
                    - Viñetas y sub-viñetas para organizar la información.
                    - Destaca en negrita los conceptos clave, síntomas cardinales, diagnósticos y tratamientos.
                    - Elimina los titubeos del profesor y ve directo al grano.
                    
                    Texto de la clase:
                    {texto_crudo}
                    """
                    respuesta = modelo.generate_content(prompt)
                    
                    # Guardar el resultado en la memoria y actualizar la página
                    st.session_state.apunte_generado = respuesta.text
                    st.rerun()
                except Exception as e:
                    st.error(f"Ocurrió un error con la IA: {e}")
        
    st.markdown("---")
    
    col_texto, col_imagenes = st.columns([3, 1])
    with col_texto:
        # Aquí la caja de texto lee lo que haya en la memoria
        texto_final = st.text_area("Apunte estructurado listo para editar:", height=400, value=st.session_state.apunte_generado)
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        col_btn1.button("💾 Guardar en Mis Apuntes")
        col_btn2.button("📤 Exportar a PDF")
        col_btn3.button("📝 Descargar en Word")
        
    with col_imagenes:
        st.info("🖼️ Banco de Diapositivas")
        st.caption("Próximamente: Las imágenes se recortarán aquí.")

# ------------------------------------------
# PESTAÑA 2: FÁBRICA DE ANKI
# ------------------------------------------
with tab_anki:
    st.subheader("Generador Automático de Tarjetas")
    st.write("Genera flashcards directas cruzando tus apuntes con literatura médica.")
    
    col_fuente1, col_fuente2 = st.columns(2)
    with col_fuente1:
        st.multiselect("📚 1. Apuntes base:", ["Apunte actual en pantalla"], default=["Apunte actual en pantalla"])
    with col_fuente2:
        st.file_uploader("📎 2. Bibliografía complementaria (PDF, DOCX):", type=["pdf", "docx"], accept_multiple_files=True, key="biblio_anki")

    st.button("🧠 Crear Tarjetas Anki")
    st.data_editor({"Frente (Pregunta)": ["¿Fisiopatología de la Colecistitis?"], "Reverso": ["Obstrucción del cístico."], "Aprobar": [True]}, num_rows="dynamic", use_container_width=True)
    st.button("🟩 DESCARGAR MAZO (.apkg)", type="primary")

# ------------------------------------------
# PESTAÑA 3: TABLAS DE MEDICINA INTERNA
# ------------------------------------------
with tab_tablas:
    st.subheader("Generador de Tablas de Alto Rendimiento")
    st.write("Compara patologías cruzando la clase con guías clínicas.")
    
    col_fuente3, col_fuente4 = st.columns(2)
    with col_fuente3:
        st.multiselect("📚 1. Apuntes base:", ["Apunte actual en pantalla"], default=["Apunte actual en pantalla"], key="select_tablas")
    with col_fuente4:
        st.file_uploader("📎 2. Bibliografía complementaria (PDF):", type=["pdf", "docx"], accept_multiple_files=True, key="biblio_tablas")
        
    st.text_input("¿De qué temas quieres generar la tabla? (Ej: Patologías biliares)")
    st.button("🚀 Generar Tabla Comparativa", type="primary")
    st.markdown("---")
    st.write("**Vista Previa Editable:**")
    st.data_editor({"Enfermedad": ["Colecistitis"], "Fisiopatología": ["Obstrucción cístico."], "Tratamiento": ["Colecistectomía."]}, num_rows="dynamic", use_container_width=True)
    
    col_btn_tabla1, col_btn_tabla2, col_btn_tabla3 = st.columns(3)
    col_btn_tabla1.button("📥 Excel (.csv)", type="primary")
    col_btn_tabla2.button("📝 Word")
    col_btn_tabla3.button("📤 PDF")
