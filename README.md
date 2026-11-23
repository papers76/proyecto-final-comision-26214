# Sistema de Gestión de Inventario

Proyecto Final Integrador de Python - Talento Tech.

Aplicación de consola para administrar el inventario de una pequeña tienda.
Los datos se guardan en una base de datos SQLite, así que no se pierden al cerrar el programa.

## Funcionalidades

1. **Registrar producto**: nombre, descripción, cantidad, precio y categoría.
2. **Listar productos**: muestra todo el inventario.
3. **Buscar producto**: por ID (si se ingresa un número) o por nombre.
4. **Actualizar producto**: cambia la cantidad y el precio de un producto por su ID.
5. **Eliminar producto**: por ID, pidiendo confirmación antes de borrar.
6. **Reporte de bajo stock**: lista los productos con cantidad menor o igual a un límite.
7. **Salir**.

## Validaciones y seguridad

- El nombre no puede quedar vacío.
- La cantidad debe ser un número entero mayor o igual a 0.
- El precio debe ser un número mayor a 0.
- Los ID deben ser números enteros, y se verifica que el producto exista antes de modificarlo o eliminarlo.
- La tabla tiene restricciones `NOT NULL` y `CHECK`, así que la base de datos también rechaza datos inválidos.
- Todas las consultas SQL usan parámetros (`?`) para evitar inyecciones SQL.
- Las operaciones que modifican datos usan transacciones (`BEGIN TRANSACTION`, `commit()` y `rollback()`).
- Los errores se manejan con `try-except`, y la conexión se cierra siempre en `finally`.
- Los mensajes usan colores con Colorama: verde para éxito, rojo para errores, amarillo para avisos.

## Requisitos

- Python 3
- Colorama
- SQLite3 (ya viene incluido con Python)

## Instalación

```bash
git clone https://github.com/papers76/proyecto-final-comision-26214.git
cd proyecto-final-comision-26214
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

Ejecutalo desde la carpeta del proyecto. La base de datos `inventario.db` se crea automáticamente en esa carpeta la primera vez que se ejecuta el programa, y no se sube al repositorio (está en el `.gitignore`).

## Estructura

```text
proyecto-final-comision-26214/
├── database.py      # Conexión y creación de la tabla
├── operaciones.py   # Funciones del CRUD y reporte de bajo stock
├── main.py          # Menú principal (punto de entrada)
├── requirements.txt # Dependencias (colorama)
├── .gitignore       # Archivos que no se suben (base de datos, caché)
└── README.md
```

## Ejemplos de uso

Registrar un producto:

```text
=== Registrar Producto ===
Nombre: yerba mate
Cantidad: 3
Precio: 2500
Descripción: Paquete 1kg
Categoría: almacen
[ÉXITO] 'Yerba mate' registrado correctamente.
```

Listar productos:

```text
=== Lista de Productos ===
ID: 1 | Yerba mate           | Cant: 3     | Precio: $2500.00 | Categoría: Almacen | Descripción: Paquete 1kg
ID: 2 | Aceite               | Cant: 20    | Precio: $3200.00 | Categoría: Almacen | Descripción: 1.5 litros
```

Buscar por nombre:

```text
=== Buscar Producto ===
Ingresá el ID o el nombre del producto: aceite
ID: 2 | Aceite               | Cant: 20    | Precio: $3200.00 | Categoría: Almacen | Descripción: 1.5 litros
```

Reporte de bajo stock:

```text
=== Reporte de Bajo Stock ===
Límite de stock: 10
ID: 1 | Yerba mate           | Quedan: 3
```

Validación de datos:

```text
=== Registrar Producto ===
Nombre: Arroz
Cantidad: 5
Precio: 0
[ERROR] El precio debe ser mayor a 0.
```

## Autor

Ariel Basabe · Talento Tech · Python · Comisión 26214
