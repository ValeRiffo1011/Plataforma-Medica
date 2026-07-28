import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 0. CONFIGURACIÓN DE LA IA Y MEMORIA
# ==========================================
tiene_llave = "GEMINI_API_KEY" in st.secrets

ARCHIVO_APUNTES = "mis_apuntes.json"

def cargar_apuntes_guardados():
    """Lee los apuntes guardados desde un archivo JSON en disco."""
    if os.path.exists(ARCHIVO_APUNTES):
        try:
            with open(ARCHIVO_APUNTES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_apuntes_en_disco(lista):
    """Escribe la lista completa de apuntes en el archivo JSON."""
    with open(ARCHIVO_APUNTES, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

if "apunte_generado" not in st.session_state:
    st.session_state.apunte_generado = "Aquí aparecerá el apunte médico ordenado con viñetas y negritas..."

if "lista_apuntes" not in st.session_state:
    st.session_state.lista_apuntes = cargar_apuntes_guardados()

if "apunte_version" not in st.session_state:
    st.session_state.apunte_version = 0

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

    if len(st.session_state.lista_apuntes) == 0:
        st.info("Todavía no has guardado ningún apunte. Genera uno y usa el botón '💾 Guardar en Mis Apuntes'.")
    else:
        # Mostramos los más recientes primero
        for i, apunte in enumerate(reversed(st.session_state.lista_apuntes)):
            indice_real = len(st.session_state.lista_apuntes) - 1 - i
            if st.button(f"📄 {apunte['titulo']}", key=f"abrir_apunte_{indice_real}"):
                st.session_state.apunte_generado = apunte["contenido"]
                st.session_state.apunte_version += 1
                st.rerun()

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

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        ramo_codigo = st.text_input("Ramo y código (Ej: Patología General 2026 — MAP302)")
    with col_meta2:
        profesor_materia = st.text_input("Profesor y materia (Ej: Dr. Navarro — Anatomía Patológica, UFRO)")
    with col_meta3:
        fecha_clase = st.text_input("Fecha de la clase (Ej: 05/06/2025)")

    col_input1, col_input2 = st.columns(2)
    with col_input1:
        texto_crudo = st.text_area("1. Pega aquí el texto bruto de tu clase:", height=150)
    with col_input2:
        archivo_clase = st.file_uploader("2. Sube la presentación (.pdf, .pptx):", type=["pdf", "pptx"])
        
    if st.button("✨ Estructurar Apunte", type="primary"):
        if texto_crudo.strip() == "":
            st.warning("⚠️ Por favor, pega el texto de la clase primero.")
        elif not tiene_llave:
            st.error("⚠️ No se encontró la llave de API en los secretos de Streamlit (Settings > Secrets).")
        else:
            with st.spinner("🧠 Buscando un modelo Gemini disponible y estructurando..."):
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]

                    encabezado = f"{ramo_codigo or '[Ramo y código]'}\n{profesor_materia or '[Profesor y materia]'} | Clase {fecha_clase or '[fecha]'}"

                    prompt = f"""
Eres un asistente experto en crear apuntes de estudio para estudiantes de medicina, a partir de transcripciones brutas de clases grabadas. Debes seguir ESTRICTAMENTE la plantilla de formato que se describe abajo, replicando la misma estructura, mismos tipos de cajas y mismo estilo que un apunte de referencia ya validado. No inventes datos clínicos que no estén en la transcripción; si algo no aparece, simplemente omite esa sección.

# ENCABEZADO (usa exactamente este bloque al inicio, en texto plano, sin viñetas)
{encabezado}
# [Título del tema principal de la clase, como H1]
Un párrafo breve (2-3 líneas) que describe qué contiene el documento y cómo está estructurado (ejes temáticos principales de la clase).

# ESTRUCTURA DEL CUERPO
Divide el contenido en secciones numeradas con headers (## 1. Tema, ## 2. Tema, etc.), siguiendo el orden cronológico real en que el profesor los mencionó en la transcripción. Dentro de cada sección:
- Usa viñetas y sub-viñetas (con sangría) para organizar la información.
- Destaca en **negrita** los conceptos clave, definiciones, cifras importantes, síntomas cardinales, diagnósticos y tratamientos.
- Elimina los titubeos, muletillas y repeticiones del profesor, pero NO elimines información clínica real, incluso si es una anécdota o ejemplo que el profesor dio (va en la caja de "CITA DEL PROFESOR" si es una frase textual relevante, o integrada al texto si es un dato).

# CAJAS ESPECIALES (usa estos formatos EXACTOS cuando corresponda; no las agregues si no hay contenido real que amerite una)

1. Caja de advertencia para conceptos que se prestan a confusión:
⚠️ **TRAMPA DE EXAMEN / NO CONFUNDIR**
[Contenido: contraste explícito entre dos conceptos que el alumno podría confundir, en 1-3 líneas]

2. Caja para una cita textual del profesor (solo si el profesor dijo algo memorable, una anécdota o un ejemplo ilustrativo, usando su fraseo real de la transcripción):
💬 **CITA DEL PROFESOR**
"[cita textual corta]" — [Nombre del profesor, si se conoce, si no usa 'El profesor'] (breve contexto de qué ilustra la cita).

3. Caja para cuando el profesor menciona una diapositiva/imagen/gráfico/mapa (aunque tú no tengas la imagen todavía, describe lo que el profesor cuenta que se ve, y deja un marcador para que se pueda insertar la imagen real después):
🔬 **DESCRIPCIÓN DE IMAGEN**
Tipo: [qué tipo de imagen es: mapa, gráfico de barras, tabla, foto histórica, esquema, etc., y su fuente si se menciona]
Hallazgos: [qué muestra la imagen, según lo que describe el profesor]
Significado: [por qué importa este hallazgo para el tema, si el profesor lo explica]
[IMAGEN PENDIENTE DE INSERTAR — buscar en Banco de Diapositivas]

4. Caja para cuando el profesor da una pista explícita de que algo "va a preguntar en la prueba" o lo enfatiza como importante para evaluación:
📋 **LO QUE PREGUNTA EL PROFESOR**
[Contenido resumido de la pista, en 1-3 líneas]

# CIERRE DEL DOCUMENTO
Al final del apunte, agrega SIEMPRE estas dos secciones:

## Lo que el profesor va a preguntar en la prueba
Lista numerada (10-15 puntos) con los conceptos que, según todo lo dicho en la clase, más probablemente se evalúen (prioriza lo que el profesor remarcó, repitió, o marcó como "trampa" o "pregunta").

## Tabla resumen final
Una tabla en formato Markdown con columnas: Concepto clave | Contenido esencial | Prioridad
Donde Prioridad es uno de: 🔴 Máximo | 🟠 Alto | 🟡 Contextual, según qué tan central fue el tema en la clase.

# FORMATO GENERAL
- Todo el documento en Markdown (headers con #, ##; negritas con **texto**; viñetas con -).
- No agregues comentarios tuyos fuera de la plantilla (nada de "aquí tienes tu apunte" ni explicaciones del proceso).
- Responde ÚNICAMENTE con el apunte ya estructurado, listo para pegar en un editor de texto.

# TRANSCRIPCIÓN BRUTA DE LA CLASE (fuente principal de contenido):
{texto_crudo}
"""

                    # PASO 1: Pedirle el menú de modelos a Google
                    url_menu = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                    respuesta_menu = requests.get(url_menu)

                    modelo_final = None
                    texto_respuesta = None
                    errores = []

                    if respuesta_menu.status_code == 200:
                        modelos = respuesta_menu.json().get("models", [])

                        # Armamos una lista de candidatos ordenada por preferencia:
                        # 1) modelos "flash" recientes (más baratos/rápidos)
                        # 2) modelos "pro" recientes
                        # 3) cualquier otro que soporte generateContent
                        candidatos_flash = []
                        candidatos_pro = []
                        candidatos_otros = []

                        for m in modelos:
                            nombre = m.get("name", "")
                            metodos = m.get("supportedGenerationMethods", [])
                            if "generateContent" not in metodos:
                                continue
                            if "flash" in nombre:
                                candidatos_flash.append(nombre)
                            elif "pro" in nombre:
                                candidatos_pro.append(nombre)
                            else:
                                candidatos_otros.append(nombre)

                        # Preferimos los nombres más "nuevos" primero (orden alfabético inverso
                        # suele poner versiones más altas antes, ej. 3.x antes que 2.x)
                        candidatos = (
                            sorted(candidatos_flash, reverse=True)
                            + sorted(candidatos_pro, reverse=True)
                            + candidatos_otros
                        )

                        # PASO 2: Probar cada candidato HASTA que uno realmente funcione.
                        # Esto es clave porque el listado de /models puede incluir modelos
                        # que ya no están disponibles para tu llave (como pasó con
                        # gemini-2.5-flash), y eso solo se sabe al intentar generar.
                        for candidato in candidatos:
                            url_generar = f"https://generativelanguage.googleapis.com/v1beta/{candidato}:generateContent?key={api_key}"
                            payload = {"contents": [{"parts": [{"text": prompt}]}]}
                            headers = {"Content-Type": "application/json"}

                            respuesta_gen = requests.post(url_generar, json=payload, headers=headers)
                            datos_gen = respuesta_gen.json()

                            if respuesta_gen.status_code == 200:
                                texto_respuesta = datos_gen["candidates"][0]["content"]["parts"][0]["text"]
                                modelo_final = candidato
                                break
                            else:
                                mensaje_error = datos_gen.get("error", {}).get("message", "Error desconocido")
                                errores.append(f"{candidato}: {mensaje_error}")
                                # Si el modelo ya no está disponible, seguimos probando el siguiente.
                                # Si es otro tipo de error (ej. llave inválida), igual seguimos,
                                # pero lo dejamos registrado para mostrarlo si nada funciona.
                                continue

                        if texto_respuesta:
                            st.session_state.apunte_generado = texto_respuesta
                            st.session_state.apunte_version += 1
                            st.success(f"✅ Generado con el modelo: {modelo_final}")
                            st.rerun()
                        else:
                            st.error(
                                "Ningún modelo disponible pudo generar el apunte. Detalle de errores:\n\n"
                                + "\n".join(errores)
                            )
                    else:
                        st.error("No se pudo obtener la lista de modelos de Google.")

                except Exception as e:
                    st.error(f"Ocurrió un error en la conexión: {e}")
        
    st.markdown("---")
    
    col_texto, col_imagenes = st.columns([3, 1])
    with col_texto:
        texto_final = st.text_area(
            "Apunte estructurado listo para editar:",
            height=400,
            value=st.session_state.apunte_generado,
            key=f"editor_apunte_{st.session_state.apunte_version}",
        )

        titulo_apunte = st.text_input(
            "Nombre para guardar este apunte:",
            value=(ramo_codigo.strip() if ramo_codigo.strip() else "Apunte sin título")
        )

        col_btn1, col_btn2, col_btn3 = st.columns(3)
        if col_btn1.button("💾 Guardar en Mis Apuntes"):
            if texto_final.strip() == "":
                st.warning("⚠️ No hay contenido para guardar todavía.")
            else:
                nuevo_apunte = {
                    "titulo": titulo_apunte.strip() or "Apunte sin título",
                    "contenido": texto_final,
                    "fecha_guardado": datetime.now().strftime("%d-%m-%Y %H:%M"),
                }
                st.session_state.lista_apuntes.append(nuevo_apunte)
                guardar_apuntes_en_disco(st.session_state.lista_apuntes)
                st.session_state.apunte_generado = texto_final
                st.session_state.apunte_version += 1
                st.success(f"✅ Apunte '{nuevo_apunte['titulo']}' guardado. Aparecerá en la barra lateral.")
                st.rerun()
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
