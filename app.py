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
# 2. BARRA LATERAL (HISTORIAL LIMPIO)
# ==========================================
with st.sidebar:
    st.header("📁 Mis Apuntes")
    st.caption("Documentos recientes (Maquetas visuales)")
    st.button("📄 Ingreso Hospital Regional")
    st.button("📄 Anamnesis - Paciente Cama 4")
    st.button("📄 Apuntes Medicina Interna")

# ==========================================
# 3. PESTAÑAS PRINCIPALES (4 ÁREAS)
# ==========================================
tab_transcripcion, tab_anki, tab_simulador, tab_tablas = st.tabs([
    "🎙️ Transcripción y Edición", 
    "🎴 Taller Anki", 
    "🎯 Simulador Rápido",
    "📊 Tablas Clínicas"
])

# ------------------------------------------
# PESTAÑA 1: TRANSCRIPCIÓN
# ------------------------------------------
with tab_transcripcion:
    st.subheader("Paso 1: Sube tu material")
    col1, col2 = st.columns(2)
    with col1:
        st.file_uploader("Sube el audio de la clase (.m4a, .mp3)", type=["m4a", "mp3"])
    with col2:
        st.file_uploader("Sube la presentación (.pptx, .pdf)", type=["pptx", "pdf"])
        
    st.button("✨ Procesar Clase y Extraer Imágenes", type="primary")
    st.markdown("---")
    
    st.subheader("Paso 2: Edición del Apunte")
    col_texto, col_imagenes = st.columns([3, 1])
    
    with col_texto:
        st.text_area("Apunte estructurado listo para editar:", height=300, 
                     value="Aquí aparecerá tu apunte con el formato médico de siempre...")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        col_btn1.button("💾 Guardar en el Historial")
        col_btn2.button("📤 Exportar a PDF")
        col_btn3.button("📝 Descargar en formato Word")
        
    with col_imagenes:
        st.info("🖼️ Banco de Diapositivas")
        st.caption("Arrastra las imágenes al editor cuando lo necesites.")

# ------------------------------------------
# PESTAÑA 2: TALLER ANKI
# ------------------------------------------
with tab_anki:
    st.subheader("Control de Calidad de Tarjetas")
    st.write("Revisa las flashcards generadas antes de exportarlas a tu mazo.")
    
    st.data_editor(
        {
            "Frente (Pregunta)": ["¿Año del Código de Núremberg?", "¿Qué es Aktion T4?"],
            "Reverso (Respuesta)": ["1947", "Eliminación sistemática de personas con discapacidad"],
            "Aprobar": [True, True]
        },
        num_rows="dynamic",
        use_container_width=True
    )
    
    st.button("🟩 DESCARGAR MAZO (.apkg)", type="primary")

# ------------------------------------------
# PESTAÑA 3: SIMULADOR (ACTIVE RECALL)
# ------------------------------------------
with tab_simulador:
    st.subheader("Repaso Activo de la Clase Seleccionada")
    st.info("**Pregunta 1:** ¿Cuáles son los 4 principios de la bioética de Beauchamp y Childress?")
    if st.button("Revelar Respuesta"):
        st.success("Autonomía, No Maleficencia, Beneficencia, y Justicia.")

# ------------------------------------------
# PESTAÑA 4: TABLAS CLÍNICAS
# ------------------------------------------
with tab_tablas:
    st.subheader("Generador de Tablas de Alto Rendimiento")
    st.write("Sube material adicional para que la plataforma lo fusione con tu clase y genere una tabla comparativa.")
    
    st.file_uploader("📚 Sube bibliografía extra (.pdf, .docx)", type=["pdf", "docx"])
    st.button("🚀 Generar Tabla de Enfermedades", type="primary")
    
    st.markdown("---")
    st.write("**Vista Previa del Formato:**")
    
    st.markdown("""
    | Enfermedad | Definición / Etiología | Fisiopatología | Cuadro Clínico | Diagnóstico | Tratamiento |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | **Colecistitis Aguda** | Inflamación de vesícula. 90% por litiasis. | Obstrucción del cístico → isquemia de pared. | Fiebre, náuseas. <br>📘 **[EXAMEN]** Signo de Murphy (+). | Ecografía. <br>🚨 **[ALERTA ROJA]** Pared >4mm. | Quirúrgico + ATB. |
    """)
    
    col_tab1, col_tab2 = st.columns(2)
    col_tab1.button("📤 Exportar Tabla a PDF")
    col_tab2.button("📝 Descargar Tabla en formato Word")
