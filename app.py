import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA Y API
# ==========================================
st.set_page_config(
    page_title="Plataforma de Estudio Médico", 
    page_icon="🎓", 
    layout="wide"
)

# Conectar el "Cerebro" (IA de Google) con el modelo actualizado (Flash)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_texto = genai.GenerativeModel('gemini-1.5-flash')
    ia_conectada = True
except Exception as e:
    ia_conectada = False

st.title("🩺 Mi Plataforma Clínica de Estudio")
if not ia_conectada:
    st.error("⚠️ La IA no está conectada. Revisa los Secrets en los ajustes.")
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
    
    # La sección de Ajustes fue eliminada según lo solicitado.

# ==========================================
# 3. PESTAÑAS PRINCIPALES
# ==========================================
tab_transcripcion, tab_anki, tab_simulador, tab_tablas, tab_semiologia = st.tabs([
    "🎙️ Transcripción y Edición", 
    "🎴 Taller Anki", 
    "🎯 Simulador Rápido",
    "📊 Tablas Clínicas",
    "📝 Asistente de Semiología"
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
        st.text_area("Apunte estructurado listo para editar:", height=300, value="Aquí aparecerá tu apunte con el formato médico de siempre...")
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
    st.data_editor({"Frente (Pregunta)": ["¿Año del Código de Núremberg?"], "Reverso (Respuesta)": ["1947"], "Aprobar": [True]}, num_rows="dynamic", use_container_width=True)
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

# ------------------------------------------
# PESTAÑA 5: ASISTENTE DE SEMIOLOGÍA
# ------------------------------------------
with tab_semiologia:
    st.subheader("Estructurador de Fichas Clínicas")
    st.write("Ingresa los datos desordenados de tu entrevista con el paciente. La IA los organizará en una Anamnesis profesional.")
    
    datos_brutos = st.text_area("Datos en bruto del paciente:", height=150, 
                 placeholder="Ej: Paciente Juan, 65 años, le duele la guata hace 3 días, su mamá tiene diabetes, lo operaron del apéndice...")
    
    if st.button("✨ Generar Historia Clínica Estructurada", type="primary"):
        if datos_brutos and ia_conectada:
            with st.spinner('Procesando datos clínicos con IA...'):
                instruccion = f"""
                Eres un médico especialista. Ordena los siguientes datos desordenados de un paciente en una historia clínica formal y estructurada. 
                Usa lenguaje técnico médico. Usa los apartados: Motivo de Consulta, Anamnesis Próxima, Anamnesis Remota (Mórbidos, Quirúrgicos, Familiares).
                Datos: {datos_brutos}
                """
                respuesta = modelo_texto.generate_content(instruccion)
                st.session_state['ficha_generada'] = respuesta.text
        elif not ia_conectada:
            st.error("La IA no está conectada correctamente.")
        else:
            st.warning("Por favor, ingresa los datos del paciente primero.")
            
    texto_mostrar = st.session_state.get('ficha_generada', "Aquí aparecerá la ficha clínica ordenada para que la copies, edites o guardes...")
    st.text_area("Historia Clínica Oficial (Editable):", height=300, value=texto_mostrar)
    
    col_sem1, col_sem2 = st.columns(2)
    col_sem1.button("📤 Exportar Ficha a PDF")
    col_sem2.button("📝 Descargar Ficha en formato Word")
