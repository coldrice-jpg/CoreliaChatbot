# Corelia: Asistente Virtual Universitario 💬
Corelia es un chatbot inteligente diseñado para proporcionar información centralizada a docentes, alumnos y aspirantes de la universidad. El proyecto utiliza modelos de lenguaje de gran escala (LLM) ejecutados de forma local para garantizar la privacidad y eficiencia en la consulta de datos académicos.

## 🚀 Características principales
* Interfaz Flotante: Widget tipo pop-up que se ubica en la esquina inferior derecha de la pantalla.

* IA Local: Integración con Ollama para procesar lenguaje natural sin depender de la nube.

* Diseño Modular: Separación clara entre la lógica del bot y la interfaz gráfica (GUI).

* Identidad Institucional: Estética personalizada con los colores de la universidad.

## 🛠️ Requisitos previos
Antes de comenzar, asegúrate de tener instalado lo siguiente:

  1. Python 3.10+

  2. Ollama.

  3. Modelo Llama3: Ejecuta ollama pull llama3 en tu terminal.

## 📦 Instalación
1. Clona este repositorio:

 
        git clone https://github.com/coldrice-jpg/CoreliaChatbot.git

2. Crea y activa un entorno virtual:


       python -m venv .venv
       
       # Windows:
       .venv\Scripts\activate
       
       # Linux/Mac:
       source .venv/bin/activate
       
3. Instala las dependencias:

        pip install customtkinter ollama
   
## 📂 Estructura del Proyecto
El código está organizado en módulos para facilitar el trabajo colaborativo:

Plaintext

    CoreliaChatbot/
    ├── gui_folder/ 
    │   ├── __init__.py
    │   └── gui_app.py       # Interfaz gráfica (CustomTkinter)
    └── chatbot_logic/
        ├── __init__.py
        └── bot_logic.py     # Conexión con Ollama y manejo de historial
    
## 🖥️ Uso
Para iniciar el chatbot, ejecuta el archivo principal de la interfaz desde la raíz del proyecto:

    python gui_folder/gui_app.py

* Bolita Flotante: Haz clic en el icono del globo de texto (💬) en la esquina inferior derecha para abrir el chat.

* Minimizar: Usa la "X" en el encabezado rojo para volver al modo bolita sin perder el historial de la conversación.

## 📝 Notas para colaboradores
 * Lógica: Cualquier cambio en el comportamiento de la IA debe hacerse en chatbot_logic/bot_logic.py.

 * Interfaz: Los ajustes de colores, posiciones o tamaños se gestionan en gui_folder/gui_app.py.

 * Transparencia: Se utiliza el color clave #abcdef para manejar la transparencia del widget en Windows.
