import sqlite3

con = sqlite3.connect('users.db')
cur = con.cursor()

# Crear tabla de usuarios
cur.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    clave TEXT NOT NULL
)
''')

# Crear tabla de comentarios
cur.execute('''
CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    mensaje TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

con.commit()
con.close()

print("Base de datos y tablas creadas con éxito.")
