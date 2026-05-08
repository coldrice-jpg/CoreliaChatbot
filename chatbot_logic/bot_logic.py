import ollama

class CoreliaLogic:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        # Historial interno para que Corelia recuerde lo que se dijo
        self.history = [
            {"role": "system", "content": "Eres Corelia, la asistente oficial de la universidad. Responde de forma amable y profesional."}
        ]
 
    def get_response(self, user_input):
        # Añadimos lo que dijo el usuario al historial
        self.history.append({"role": "user", "content": user_input})
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.history
            )
            bot_message = response['message']['content']
            
            # Guardamos la respuesta del bot para mantener el contexto
            self.history.append({"role": "assistant", "content": bot_message})
            return bot_message
            
        except Exception as e:
            return f"Error de conexión con Ollama: {str(e)}"