import sqlite3
from colorama import Fore

# Nombre del archivo de la base de datos
DB_NAME = "inventario.db"


def conectar():
    """Abre y devuelve una conexión con la base de datos."""
    return sqlite3.connect(DB_NAME)


def crear_tabla():
    """
    Crea la tabla productos si todavía no existe.
    Las restricciones CHECK impiden guardar cantidades negativas
    o precios menores o iguales a cero.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
                precio REAL NOT NULL CHECK (precio > 0),
                categoria TEXT
            )
        ''')
        conexion.commit()
        print(Fore.GREEN + "[ÉXITO] Base de datos inicializada.")

    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo crear la tabla: {e}")

    finally:
        conexion.close()
