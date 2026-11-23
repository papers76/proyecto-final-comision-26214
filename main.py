from colorama import Fore, init
from database import crear_tabla
from operaciones import registrar, listar, buscar
from operaciones import actualizar, eliminar, bajo_stock

# Inicializar colorama para que los colores se reinicien después de cada print
init(autoreset=True)


def menu():
    """Muestra el menú principal y ejecuta la opción que elige el usuario."""
    while True:
        print(Fore.BLUE + "\n=================================")
        print(Fore.BLUE + " SISTEMA DE GESTIÓN DE INVENTARIO")
        print(Fore.BLUE + "=================================")
        print(Fore.WHITE + "1. Registrar producto")
        print(Fore.WHITE + "2. Listar productos")
        print(Fore.WHITE + "3. Buscar producto")
        print(Fore.WHITE + "4. Actualizar producto")
        print(Fore.WHITE + "5. Eliminar producto")
        print(Fore.WHITE + "6. Reporte de bajo stock")
        print(Fore.WHITE + "7. Salir")

        opcion = input(Fore.CYAN + "Elegí una opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            listar()
        elif opcion == "3":
            buscar()
        elif opcion == "4":
            actualizar()
        elif opcion == "5":
            eliminar()
        elif opcion == "6":
            bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "\n¡Gracias por usar el sistema!")
            break
        else:
            print(Fore.RED + "[ERROR] Opción inválida. Elegí un número del 1 al 7.")


# Crear la tabla (si no existe) y arrancar el programa
crear_tabla()
menu()
