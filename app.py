import streamlit as st
import whisper
import os

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

# Cargar el modelo de Whisper (usaremos el tamaño 'tiny' o 'base' para que cargue rápido en la nube)
@st.cache_resource
def cargar_modelo_whisper():
    return whisper.load_model("base")

with st.spinner("Cargando el motor de audio (Whisper)... Por favor espera un momento."):
    modelo_whisper = cargar_modelo_whisper()

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
# 3. PESTAÑAS PRINCIPALES
# ==========================================
tab_transcripcion, tab_anki, tab_simulador, tab_tablas = st.tabs([
    "🎙️ Transcripción y Edición", 
    "🎴 Taller Anki", 
    "🎯 Simulador Rápido",
    "📊 Tablas Clínicas"
])

# ------------------------------------------
# PESTAÑA 1: TRANSCRIPCIÓN (¡CON MOTOR REAL!)
# ------------------------------------------
with tab_transcripcion:
    st.subheader("Paso 1: Sube tu material de audio")
    
    archivo_audio = st.file_uploader("Sube el audio de la clase (.m4a, .mp3)", type=["m4a", "mp3"])
    
    if archivo_audio is not None:
        # Guardar temporalmente el audio en el servidor para que Whisper pueda leerlo
        with open("temp_audio.mp3", "wb") as f:
            f.write(archivo_audio.getbuffer())
            
        if st.button("✨ Procesar y Transcribir Audio", type="primary"):
            with st.spinner("🎧 Escuchando la clase y redactando el apunte... Esto puede tomar unos segundos."):
                try:
                    # Ejecutar la transcripción con Whisper
                    resultado = modelo_whisper.transcribe("temp_audio.mp3", language="es")
                    texto_transcrito = resultado["text"]
                    
                    # Guardarlo en la memoria de la sesión
                    st.session_state['texto_clase'] = texto_transcrito
                    st.success("¡Transcripción completada con éxito!")
                except Exception as e:
                    st.error(f"Ocurrió un error al procesar el audio: {e}")

    st.markdown("---")
    st.subheader("Paso 2: Edición del Apunte")
    
    # Obtener el texto transcrito o mostrar el texto por defecto
    texto_final = st.session_state.get('texto_clase', "Aquí aparecerá el texto de tu clase una vez que subas un audio y presiones procesar...")
    
    col_texto, col_imagenes = st.columns([3, 1])
    
    with col_texto:
        apunte_editado = st.text_area("Apunte estructurado listo para editar:", height=300, value=texto_final)
        
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
    st.data_editor(
        {
            "Frente (Pregunta)": ["¿Año del Código de Núremberg?"],
            "Reverso (Respuesta)": ["1947"],
            "Aprobar": [True]
        },
        num_rows="dynamic",
        use_container_width=True
    )
    st.button("🟩 DESCARGAR MAZO (.apkg)", type="primary")

# ------------------------------------------
# PESTAÑA 3: SIMULADOR
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
    st.file_uploader("📚 Sube bibliografía extra (.pdf, .docx)", type=["pdf", "docx"])
    st.button("🚀 Generar Tabla de Enfermedades", type="primary")
    st.markdown("---")
    st.write("**Vista Previa del Formato:**")
    st.markdown("| Enfermedad | Definición | Fisiopatología | Cuadro Clínico | Diagnóstico | Tratamiento |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **Colecistitis** | Inflamación vesícula. | Obstrucción cístico. | Fiebre. 📘 **[EXAMEN]** Murphy (+). | Ecografía. 🚨 **[ALERTA ROJA]** Pared >4mm. | Quirúrgico. |")
    col_tab1, col_tab2 = st.columns(2)
    col_tab1.button("📤 Exportar Tabla a PDF")
    col_tab2.button("📝 Descargar Tabla en formato Word")
