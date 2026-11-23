import sqlite3
from colorama import Fore
from database import conectar


def pedir_cantidad_y_precio():
    """
    Pide la cantidad y el precio al usuario y los valida.
    Devuelve (cantidad, precio) si son correctos, o None si hay un error.
    """
    try:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
    except ValueError:
        print(Fore.RED + "[ERROR] La cantidad debe ser un número entero y el precio un número.")
        return None

    if cantidad < 0:
        print(Fore.RED + "[ERROR] La cantidad no puede ser negativa.")
        return None

    if precio <= 0:
        print(Fore.RED + "[ERROR] El precio debe ser mayor a 0.")
        return None

    return cantidad, precio


def mostrar_producto(producto):
    """Muestra en pantalla los datos de un producto (id, nombre, descripción, cantidad, precio, categoría)."""
    print(Fore.WHITE + f"ID: {producto[0]} | {producto[1]:<20} | Cant: {producto[3]:<5} | "
          f"Precio: ${producto[4]:.2f} | Categoría: {producto[5]} | Descripción: {producto[2]}")


def registrar():
    """Pide los datos de un producto nuevo, los valida y los guarda en la base de datos."""
    print(Fore.CYAN + "\n=== Registrar Producto ===")

    nombre = input("Nombre: ").strip().capitalize()
    if not nombre:
        print(Fore.RED + "[ERROR] El nombre no puede estar vacío.")
        return

    datos = pedir_cantidad_y_precio()
    if not datos:
        return
    cantidad = datos[0]
    precio = datos[1]

    descripcion = input("Descripción: ").strip()
    categoria = input("Categoría: ").strip().capitalize()

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        conexion.execute("BEGIN TRANSACTION")
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        print(Fore.GREEN + f"[ÉXITO] '{nombre}' registrado correctamente.")

    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED + f"[ERROR] No se pudo registrar el producto: {e}")

    finally:
        conexion.close()


def listar():
    """Muestra todos los productos guardados en la base de datos."""
    print(Fore.CYAN + "\n=== Lista de Productos ===")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        if not productos:
            print(Fore.YELLOW + "[INFO] El inventario está vacío.")
            return

        for producto in productos:
            mostrar_producto(producto)

    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo consultar el inventario: {e}")

    finally:
        conexion.close()


def buscar():
    """Busca un producto por su ID (si se ingresa un número) o por su nombre."""
    print(Fore.CYAN + "\n=== Buscar Producto ===")

    criterio = input("Ingresá el ID o el nombre del producto: ").strip()
    if not criterio:
        print(Fore.RED + "[ERROR] Tenés que ingresar un ID o un nombre.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        if criterio.isdigit():
            cursor.execute("SELECT * FROM productos WHERE id = ?", (int(criterio),))
        else:
            cursor.execute("SELECT * FROM productos WHERE nombre = ?", (criterio.capitalize(),))
        productos = cursor.fetchall()

        if not productos:
            print(Fore.YELLOW + "[INFO] No se encontraron productos.")
            return

        for producto in productos:
            mostrar_producto(producto)

    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo realizar la búsqueda: {e}")

    finally:
        conexion.close()


def actualizar():
    """Actualiza la cantidad y el precio de un producto, buscándolo por su ID."""
    print(Fore.CYAN + "\n=== Actualizar Producto ===")

    id_producto = input("ID del producto: ").strip()
    if not id_producto.isdigit():
        print(Fore.RED + "[ERROR] El ID debe ser un número entero.")
        return
    id_producto = int(id_producto)

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Primero se verifica que el producto exista
        cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.YELLOW + "[INFO] No existe un producto con ese ID.")
            return

        print(Fore.WHITE + f"Producto: {producto[0]}")
        datos = pedir_cantidad_y_precio()
        if not datos:
            return
        cantidad = datos[0]
        precio = datos[1]

        conexion.execute("BEGIN TRANSACTION")
        cursor.execute(
            "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
            (cantidad, precio, id_producto)
        )
        conexion.commit()
        print(Fore.GREEN + f"[ÉXITO] '{producto[0]}' actualizado correctamente.")

    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED + f"[ERROR] No se pudo actualizar el producto: {e}")

    finally:
        conexion.close()


def eliminar():
    """Elimina un producto por su ID, pidiendo confirmación antes."""
    print(Fore.CYAN + "\n=== Eliminar Producto ===")

    id_producto = input("ID del producto a eliminar: ").strip()
    if not id_producto.isdigit():
        print(Fore.RED + "[ERROR] El ID debe ser un número entero.")
        return
    id_producto = int(id_producto)

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Primero se verifica que el producto exista
        cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.YELLOW + "[INFO] No existe un producto con ese ID.")
            return

        confirmacion = input(Fore.YELLOW + f"¿Seguro que querés eliminar '{producto[0]}'? (S/N): ").strip().lower()
        if confirmacion != "s":
            print(Fore.GREEN + "[CANCELADO] No se eliminó el producto.")
            return

        conexion.execute("BEGIN TRANSACTION")
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        print(Fore.GREEN + f"[ÉXITO] '{producto[0]}' eliminado correctamente.")

    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED + f"[ERROR] No se pudo eliminar el producto: {e}")

    finally:
        conexion.close()


def bajo_stock():
    """Muestra los productos cuya cantidad es menor o igual al límite que ingresa el usuario."""
    print(Fore.CYAN + "\n=== Reporte de Bajo Stock ===")

    limite = input("Límite de stock: ").strip()
    if not limite.isdigit():
        print(Fore.RED + "[ERROR] El límite debe ser un número entero mayor o igual a 0.")
        return
    limite = int(limite)

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT id, nombre, cantidad FROM productos WHERE cantidad <= ? ORDER BY cantidad",
            (limite,)
        )
        productos = cursor.fetchall()

        if not productos:
            print(Fore.GREEN + "[INFO] No hay productos con bajo stock.")
            return

        for producto in productos:
            print(Fore.RED + f"ID: {producto[0]} | {producto[1]:<20} | Quedan: {producto[2]}")

    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo generar el reporte: {e}")

    finally:
        conexion.close()
