import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================
# Aquí le damos el nombre a la pestaña y le decimos que use todo el ancho de la pantalla
st.set_page_config(
    page_title="Plataforma de Estudio Médico", 
    page_icon="🎓", 
    layout="wide"
)

# Título principal de la aplicación
st.title("🩺 Mi Plataforma Clínica de Estudio")
st.markdown("---")

# ==========================================
# 2. BARRA LATERAL (HISTORIAL Y AJUSTES)
# ==========================================
with st.sidebar:
    st.header("📁 Historial de Clases")
    
    # Simulando clases pasadas
    st.button("📄 Bioética - Introducción")
    st.button("📄 Fisiología - Ciclo Cardíaco")
    st.button("📄 Gastroenterología - Jornada I")
    
    st.markdown("---")
    st.header("⚙️ Ajustes")
    # Switch para alternar un modo "Turno de Noche" (Oscuro)
    modo_oscuro = st.toggle("🌙 Modo Noche")

# ==========================================
# 3. PESTAÑAS PRINCIPALES (TABS)
# ==========================================
# Creamos las 3 áreas de trabajo que definimos
tab_transcripcion, tab_anki, tab_simulador = st.tabs([
    "🎙️ Transcripción y Edición", 
    "🎴 Taller Anki", 
    "🎯 Simulador Rápido"
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
    
    # El sistema híbrido: Editor de texto + Banco de imágenes al lado
    col_texto, col_imagenes = st.columns([3, 1])
    
    with col_texto:
        # Aquí aparecerá el texto que podrás editar
        st.text_area("Apunte estructurado listo para editar:", height=300, 
                     value="Aquí aparecerá tu apunte con el formato médico de siempre...")
        
        col_btn1, col_btn2 = st.columns(2)
        col_btn1.button("💾 Guardar en el Historial")
        # Botón rápido para compartir el resumen con tu grupo de estudio
        col_btn2.button("📤 Exportar PDF para Benjamín, Marcos y Sofía")
        
    with col_imagenes:
        st.info("🖼️ Banco de Diapositivas")
        st.caption("Arrastra las imágenes al editor cuando lo necesites.")
        # Aquí irían las miniaturas de las imágenes generadas

# ------------------------------------------
# PESTAÑA 2: TALLER ANKI
# ------------------------------------------
with tab_anki:
    st.subheader("Control de Calidad de Tarjetas")
    st.write("Revisa las flashcards generadas por la IA antes de exportarlas a tu mazo.")
    
    # Simulamos una tabla interactiva donde puedes corregir o borrar
    st.data_editor(
        {
            "Frente (Pregunta)": ["¿Año del Código de Núremberg?", "¿Qué es Aktion T4?"],
            "Reverso (Respuesta)": ["1947", "Eliminación sistemática de personas con discapacidad"],
            "Aprobar": [True, True]
        },
        num_rows="dynamic"
    )
    
    st.button("🟩 DESCARGAR MAZO (.apkg)", type="primary")

# ------------------------------------------
# PESTAÑA 3: SIMULADOR (ACTIVE RECALL)
# ------------------------------------------
with tab_simulador:
    st.subheader("Repaso Activo de la Clase Seleccionada")
    st.write("Lee la pregunta, piénsala, y presiona el botón para revelar la respuesta.")
    
    st.info("**Pregunta 1:** ¿Cuáles son los 4 principios de la bioética de Beauchamp y Childress?")
    if st.button("Revelar Respuesta"):
        st.success("Autonomía, No Maleficencia, Beneficencia, y Justicia.")
