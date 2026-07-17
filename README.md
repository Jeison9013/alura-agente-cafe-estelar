# ☕ Challenge Alura - Agente Inteligente 'Café Estelar'

Este proyecto consiste en un agente de Inteligencia Artificial capaz de responder preguntas en lenguaje natural sobre las políticas, menús y servicios de la cafetería "Café Estelar". Funciona extrayendo información directamente de un documento PDF (Base de Conocimiento) utilizando una arquitectura RAG (Generación Aumentada por Recuperación) para evitar respuestas falsas.

## 🛠️ Arquitectura del Sistema

La solución se diseñó siguiendo un flujo de procesamiento de tres capas:

1. **Base de Conocimiento (PyPDF):** Al arrancar, la aplicación lee de forma automatizada el archivo `informacion_cafeteria.pdf`, extrayendo todo su contenido textual a memoria.
2. **Interfaz de Usuario (Streamlit):** Una aplicación web ligera que gestiona el estado de la sesión (`st.session_state`) para mantener el historial de chat de forma interactiva.
3. **Cerebro de IA (Cohere LLM):** El texto extraído se inyecta como contexto exclusivo (Preamble) en el modelo `command-r-08-2024` de Cohere. Esto asegura que el agente responda únicamente con datos oficiales y decline responder amablemente si la información no está en el documento.

---

## 🚀 Instrucciones de Ejecución Local

Si deseas probar este proyecto en tu entorno local, sigue estos pasos:

### Prerrequisitos
* Tener instalado Python 3.9 o superior.
* Contar con una API Key de Cohere.

### Instalación
1. Clona este repositorio en tu máquina:
   ```bash
   git clone [https://github.com/Jeison9013/alura-agente-cafe-estelar.git](https://github.com/Jeison9013/alura-agente-cafe-estelar.git)
   cd alura-agente-cafe-estelar