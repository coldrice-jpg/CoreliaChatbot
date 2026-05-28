import sys
import os
import customtkinter as ctk
from PIL import Image

# Subir un nivel para encontrar la raíz del proyecto
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from chatbot_logic.bot_logic import CoreliaLogic

class CoreliaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.chat_logic = CoreliaLogic()
        
        self.expandido = False
        self.ancho_chat = 400
        self.alto_chat = 550
        self.radio_bolita = 70 

        # Configuración de ventana
        self.title("Corelia")
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        
        # COLOR CLAVE: Usaremos un color extraño para la transparencia que no usemos en el chat
        self.color_transparente = "#abcdef" 
        self.config(background=self.color_transparente)
        self.attributes("-transparentcolor", self.color_transparente)

        # --- Interfaz de la "Bolita" ---
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        
        ruta_normal = os.path.join(directorio_script, "logo_normal.png")
        ruta_hover = os.path.join(directorio_script, "logo_hover.png")

        # Verificación de existencia para depurar
        if not os.path.exists(ruta_normal) or not os.path.exists(ruta_hover):
            print(f"ERROR: No se encuentran las imágenes en: {directorio_script}")
            print(f"¿Existe logo_normal.png?: {os.path.exists(ruta_normal)}")
            print(f"¿Existe logo_hover.png?: {os.path.exists(ruta_hover)}")

        # 1. Cargar ambas imágenes con rutas absolutas
        self.img_normal = ctk.CTkImage(light_image=Image.open(ruta_normal), size=(30, 30))
        self.img_hover = ctk.CTkImage(light_image=Image.open(ruta_hover), size=(30, 30))

        # 2. Crear el botón
        self.btn_flotante = ctk.CTkButton(
            self, 
            image=self.img_normal, # Empezamos con la normal
            text="",               
            width=self.radio_bolita, 
            height=self.radio_bolita, 
            corner_radius=self.radio_bolita // 2,
            fg_color="#617D93",
            hover_color="#4A6071",
            command=self.alternar_chat
        )
        self.btn_flotante.place(x=0, y=0)

        # 3. Vincular eventos de ratón para cambiar el logo
        self.btn_flotante.bind("<Enter>", lambda e: self.btn_flotante.configure(image=self.img_hover))
        self.btn_flotante.bind("<Leave>", lambda e: self.btn_flotante.configure(image=self.img_normal))

        # --- Interfaz del Chat ---
        # El fg_color aquí DEBE ser distinto al color_transparente
        self.frame_chat = ctk.CTkFrame(
            self, 
            fg_color="#F2F2F2", # Fondo gris sólido para el chat
            corner_radius=20, 
            border_width=2, 
            border_color="#617D93"
        )
        
        self.header = ctk.CTkFrame(self.frame_chat, fg_color="#617D93", height= 40, corner_radius=0)
        self.header.pack(fill="x")
        
        self.lbl_titulo = ctk.CTkLabel(self.header, text="Corelia Chat", text_color="white", font=("Arial", 14, "bold"), corner_radius=0)
        self.lbl_titulo.pack(side="left", padx=15, pady=5)

        self.btn_cerrar = ctk.CTkButton(self.header, text="X", width=30, fg_color="transparent", hover_color="#4A6071", command=self.alternar_chat, corner_radius=0)
        self.btn_cerrar.pack(side="right", padx=5, pady=5)

        self.chat_container = ctk.CTkScrollableFrame(self.frame_chat, fg_color="#FFFFFF", corner_radius=20) # Fondo blanco para mensajes
        self.chat_container.pack(padx=10, pady=10, fill="both", expand=True)

        self.input_frame = ctk.CTkFrame(self.frame_chat, fg_color="transparent")
        self.input_frame.pack(padx=10, pady=10, fill="x")

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Escribe...", height=40, corner_radius=20)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.procesar_mensaje)

        self.btn_enviar = ctk.CTkButton(self.input_frame, text="➤", width=40, height=40, fg_color="#617D93", hover_color="#4A6071", corner_radius=20, command=self.procesar_mensaje)
        self.btn_enviar.pack(side="right")

        self.actualizar_geometria()
        self.crear_globo("¡Hola! Soy Corelia. ¿En qué te ayudo?", "bot")

    def actualizar_geometria(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if not self.expandido:
            ancho, alto = self.radio_bolita, self.radio_bolita
            x = screen_width - ancho - -300
            y = screen_height - alto - -100
        else:
            ancho, alto = self.ancho_chat, self.alto_chat
            # Calculamos para que el chat crezca hacia la izquierda de la bolita
            x = screen_width - ancho - -250
            y = screen_height - alto - 15

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def alternar_chat(self):
        if not self.expandido:
            self.btn_flotante.place_forget()
            self.frame_chat.pack(fill="both", expand=True)
            self.expandido = True
        else:
            self.frame_chat.pack_forget()
            self.btn_flotante.place(x=0, y=0)
            self.expandido = False
        
        self.actualizar_geometria()

    def scroll_al_final(self):
        # Forzar la actualización de la interfaz para calcular el nuevo tamaño
        self.update_idletasks()
        # Mover el scroll al final (posiciones van de 0.0 a 1.0)
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def crear_globo(self, texto, emisor):
        if emisor == "user":
            color_fondo = "#617D93" # Color principal adaptado
            color_texto = "white"   # Se mantiene para contraste
            posicion = "e"
            pad_x = (50, 5)
        else:
            # Bot se mantiene igual para contraste
            color_fondo = "#E9E9EB"; color_texto = "black"; posicion = "w"; pad_x = (5, 50)

        globo = ctk.CTkFrame(self.chat_container, fg_color=color_fondo, corner_radius=15)
        globo.pack(anchor=posicion, padx=pad_x, pady=5)
        label = ctk.CTkLabel(globo, text=texto, wraplength=250, justify="left", text_color=color_texto, padx=10, pady=5)
        label.pack()
        # --- AGREGA ESTA LÍNEA AL FINAL ---
        self.after(10, self.scroll_al_final)

    def procesar_mensaje(self, event=None):
        texto_usuario = self.entry.get()
        if texto_usuario.strip():
            self.crear_globo(texto_usuario, "user")
            self.entry.delete(0, "end")
            
            # Actualizamos la pantalla para que el usuario vea su mensaje antes de que la IA procese
            self.update_idletasks() 
            
            respuesta_bot = self.chat_logic.get_response(texto_usuario)
            self.crear_globo(respuesta_bot, "bot")

if __name__ == "__main__":
    app = CoreliaGUI()
    app.mainloop()