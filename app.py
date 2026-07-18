import streamlit as st
import cohere
from pypdf import PdfReader

# Configuración de la página web
st.set_page_config(page_title="Agente Café Estelar", page_icon="☕", layout="centered")

st.title("☕ Agente Inteligente - Café Estelar")
st.write("¡Bienvenido! Pregúntame lo que quieras sobre el menú, horarios o políticas de la cafetería.")

# 1. Configurar la API Key de Cohere desde los Secrets de Streamlit
try:
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
except Exception:
    st.error("❌ Falta configurar la COHERE_API_KEY en los Secrets de Streamlit Cloud.")
    st.stop()

cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# 2. Cargar y extraer texto del PDF (Base de Conocimiento)
@st.cache_data
def cargar_base_conocimiento(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() + "\n"
        return texto
    except Exception as e:
        return None

texto_pdf = cargar_base_conocimiento("informacion_cafeteria.pdf")

if not texto_pdf:
    st.error("❌ No se encontró el archivo 'informacion_cafeteria.pdf' en el repositorio.")
    st.stop()

# 3. Inicializar el historial de chat en la sesión web
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes anteriores del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Caja de entrada de texto para el usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    
    # Mostrar el mensaje del usuario en la pantalla
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar la respuesta del agente con Cohere
    with st.chat_message("assistant"):
        with st.spinner("Buscando en la base de conocimiento..."):
            
            # Definir el contexto y reglas estrictas para el modelo (RAG)
            preamble = (
                "Eres un asistente de servicio al cliente exclusivo para la cafetería 'Café Estelar'. "
                "Tu objetivo es responder las preguntas de los usuarios basándote ÚNICAMENTE en la siguiente información oficial:\n\n"
                f"{texto_pdf}\n\n"
                "Reglas críticas:\n"
                "1. Si la respuesta a la pregunta del usuario NO se encuentra explícitamente en el texto provisto, responde exactamente: "
                "'No cuento con esa información en los registros oficiales de Café Estelar.'\n"
                "2. No inventes datos bajo ninguna circunstancia.\n"
                "3. Mantén un tono sumamente amable y profesional."
            )
            
            try:
                # Llamada al modelo de lenguaje
                response = cohere_client.chat(
                    message=prompt,
                    model="command-r-08-2024",
                    preamble=preamble
                )
                respuesta_texto = response.text
                
                # Mostrar la respuesta en la interfaz
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                
            except Exception as e:
                st.error(f"Error al procesar la respuesta con Cohere: {e}")
