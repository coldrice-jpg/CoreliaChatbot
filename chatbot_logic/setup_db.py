import sqlite3
import os

class UniversityDB:
    def __init__(self):
        # Localiza la base de datos en la misma carpeta que este script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "universidad.db")
        self._crear_tablas()

    def _crear_tablas(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Aseguramos que las tablas existan
            cursor.execute('''CREATE TABLE IF NOT EXISTS eventos 
                             (nombre TEXT, fecha TEXT, descripcion TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS oferta_academica 
                             (tipo TEXT, nombre TEXT, duracion TEXT)''')
            
            # Insertar la fecha de renovación de becas solo si no existe
            cursor.execute("SELECT * FROM eventos WHERE nombre = ?", ("Renovación de Becas",))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO eventos (nombre, fecha, descripcion) VALUES (?, ?, ?)", 
                               ("Renovación de Becas", "agosto 9 a agosto 22", "Periodo oficial de renovación"))
            
            conn.commit()

    def obtener_toda_la_oferta(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tipo, nombre FROM oferta_academica")
            resultados = cursor.fetchall()
            if resultados:
                lista = "\n".join([f"- {r[0]} en {r[1]}" for r in resultados])
                return f"Nuestra oferta académica completa incluye:\n{lista}"
            return "No hay oferta académica registrada actualmente."

    def buscar_dato(self, pregunta_usuario):
        pregunta = pregunta_usuario.lower()
        
        # 1. Filtro para preguntas generales
        if any(p in pregunta for p in ["oferta", "carreras", "licenciaturas", "doctorados", "tienen", "ofrecen"]):
            return self.obtener_toda_la_oferta()
            
        # 2. Búsqueda específica
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            palabras = pregunta.split()
            
            for palabra in palabras:
                if len(palabra) < 4: continue 
                query = f"%{palabra}%"
                
                # Buscar en Oferta Académica
                cursor.execute("""SELECT tipo, nombre, duracion FROM oferta_academica 
                                WHERE nombre LIKE ? OR tipo LIKE ?""", (query, query))
                carrera = cursor.fetchone()
                if carrera:
                    return f"Contamos con el {carrera[0]} en {carrera[1]} ({carrera[2]})."

                # Buscar en Eventos (incluye la nueva Beca)
                cursor.execute("SELECT nombre, fecha FROM eventos WHERE nombre LIKE ?", (query,))
                evento = cursor.fetchone()
                if evento:
                    return f"El evento '{evento[0]}' se realizará del {evento[1]}."
        
        return "Lo siento, no encontré información sobre eso en nuestra base de datos."