import os
import sys

# Esto permite que el archivo encuentre a sus vecinos en la misma carpeta
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import ollama
from database_manager import UniversityDB

class CoreliaLogic:
    def __init__(self, model_name="llama3"):
        # ESTA ES LA LÍNEA QUE FALTA:
        self.model_name = model_name 
        
        # El resto de tu configuración
        self.db = UniversityDB()
        self.history = [
    {
        "role": "system", 
        "content": (
            "Eres Corelia, la asistente oficial de una universidad. REGLA DE ORO: Si el mensaje del usuario "
            "viene con un 'CONTEXTO UNIVERSITARIO', DEBES usar esa información para responder. "
            "No inventes fechas ni carreras si el contexto dice algo distinto."
            "Si el usuario pregunta algo que no está en el contexto, responde que no tienes esa información en lugar de inventar una respuesta."
            "Y si el usuario pregunta sobre datos que sí están en el contexto, asegúrate de usarlos para responder de forma precisa." 
            "También recuerda usar la base de datos local para responder preguntas sobre eventos y oferta académica, y si encuentras algo relevante ahí, úsalo como parte de tu respuesta."
            "Da respuestas certeras, no des información que no te pidan, como hablar sobre el contexto o la base de datos a menos que el usuario lo pregunte explícitamente."
            "Y no te presentes solo da la información que el usuario pide, sin saludos ni despedidas."
        )
    }
]

    def get_response(self, user_input):
        # 1. Buscar en la base de datos
        dato_local = self.db.buscar_dato(user_input)
        # Añade esto justo después de buscar el dato_local
        print(f"--- DEBUG: Dato encontrado en DB: {dato_local} ---")
        # 2. Formatear el mensaje según si hay o no datos en la DB
        if dato_local:
            # Inyectamos el dato de la DB como una instrucción prioritaria
            prompt_final = (
                f"Instrucción: Usa los siguientes datos reales para responder.\n"
                f"Datos: {dato_local}\n"
                f"Pregunta del usuario: {user_input}"
            )
        else:
            prompt_final = user_input

        # 3. Añadir al historial (solo el prompt final, no duplicar el input)
        self.history.append({"role": "user", "content": prompt_final})

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)
            bot_message = response['message']['content']
            
            # Guardamos la respuesta para el hilo de la charla
            self.history.append({"role": "assistant", "content": bot_message})
            return bot_message
        except Exception as e:
            return f"Error: {str(e)}"