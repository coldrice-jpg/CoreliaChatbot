import sqlite3
import os

# Aseguramos que se cree en la misma carpeta que el script
db_path = os.path.join(os.path.dirname(__file__), "universidad.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Borramos tablas si ya existen para evitar duplicados en las pruebas
cursor.execute("DROP TABLE IF EXISTS eventos")
cursor.execute("DROP TABLE IF EXISTS oferta_academica")

# Crear tablas
cursor.execute("CREATE TABLE eventos (nombre TEXT, fecha TEXT, descripcion TEXT)")
cursor.execute("CREATE TABLE oferta_academica (tipo TEXT, nombre TEXT, duracion TEXT)")

# Datos de prueba para tu presentación
datos_carreras = [
    ('Licenciatura', 'Ingeniería en Sistemas', '9 semestres'),
    ('Licenciatura', 'Administración de Empresas', '8 semestres'),
    ('Doctorado', 'Inteligencia Artificial', '6 semestres')
]

datos_eventos = [
    ('Examen de Admisión', '15 de junio 2026', 'Examen presencial'),
    ('Evento Coparmex', '20 de mayo 2026', 'Presentación de proyectos')
]

cursor.executemany("INSERT INTO oferta_academica VALUES (?,?,?)", datos_carreras)
cursor.executemany("INSERT INTO eventos VALUES (?,?,?)", datos_eventos)

conn.commit() # ¡ESTA LÍNEA ES VITAL!
conn.close()
print("Base de datos creada exitosamente.")