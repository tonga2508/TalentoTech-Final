import mysql.connector
from mysql.connector import Error
from colorama import init, Fore
import os

# Inicializar colorama
init()

def limpiar_pantalla():
    """Limpia la pantalla para mejorar la visualización en la terminal."""
    os.system("cls" if os.name == "nt" else "clear")

def crear_conexion():
    """Crear y devolver una conexión a la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='tonga',
            password='cicsparg',
            database='inventario'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(Fore.RED + f"Error al conectar con MySQL: {e}" + Fore.RESET)
        return None

def registrar_producto():
    """Registrar un nuevo producto en la base de datos."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nRegistrar Producto" + Fore.RESET)
        print("1. Ingresar un nuevo producto")
        print("2. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del producto: ")
            descripcion = input("Ingrese la descripción del producto: ")
            cantidad = int(input("Ingrese la cantidad disponible: "))
            precio = float(input("Ingrese el precio del producto: "))
            categoria = input("Ingrese la categoría del producto: ").strip().upper()

            if cantidad <= 0 or precio <= 0:
                print(Fore.RED + "La cantidad y el precio deben ser mayores a 0." + Fore.RESET)
                continue

            conexion = crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, descripcion, cantidad, precio, categoria))
                conexion.commit()
                conexion.close()
                print(Fore.GREEN + "Producto registrado exitosamente." + Fore.RESET)
                input("Presione Enter para continuar...")
        elif opcion == "2":
            break
        else:
            print(Fore.RED + "Opción no válida." + Fore.RESET)
            input("Presione Enter para continuar...")

def eliminar_producto():
    """Eliminar un producto del inventario."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nEliminar Producto" + Fore.RESET)
        print("1. Ingresar ID de producto para eliminar")
        print("2. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "2":
            break

        if opcion == "1":
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            conexion = crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("""
                    DELETE FROM productos
                    WHERE id = %s
                """, (id_producto,))
                conexion.commit()
                conexion.close()
                print(Fore.RED + "Producto eliminado exitosamente." + Fore.RESET)
                input("Presione Enter para continuar...")
        else:
            print(Fore.RED + "Opción no válida." + Fore.RESET)
            input("Presione Enter para continuar...")

def buscar_producto():
    """Buscar un producto por ID, nombre o categoría."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nBuscar Producto" + Fore.RESET)
        print("1. Buscar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por categoría")
        print("4. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "4":
            break

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            if opcion == "1":
                valor = input("Ingrese el ID del producto: ").strip()
                cursor.execute("SELECT * FROM productos WHERE id = %s", (valor,))
            elif opcion == "2":
                valor = input("Ingrese el nombre del producto: ").strip()
                cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", (f"%{valor}%",))
            elif opcion == "3":
                valor = input("Ingrese la categoría del producto: ").strip().upper()
                cursor.execute("SELECT * FROM productos WHERE categoria = %s", (valor,))
            else:
                print(Fore.RED + "Opción no válida." + Fore.RESET)
                input("Presione Enter para continuar...")
                continue

            resultados = cursor.fetchall()
            conexion.close()

            if resultados:
                print(Fore.YELLOW + "\nResultados de la búsqueda:" + Fore.RESET)
                for producto in resultados:
                    print(f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | {producto[4]} | {producto[5]}")
            else:
                print(Fore.RED + "No se encontraron productos." + Fore.RESET)

            input("Presione Enter para continuar...")


def mostrar_productos():
    """Mostrar productos del inventario por categoría o todos."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nOpciones para mostrar productos:" + Fore.RESET)
        print("1. Mostrar todos los productos")
        print("2. Mostrar productos por categoría")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            if opcion == "1":
                cursor.execute("SELECT * FROM productos")
                productos = cursor.fetchall()
                print(Fore.YELLOW + "\nTodos los productos:" + Fore.RESET)
            elif opcion == "2":
                categoria = input("Ingrese la categoría (A, B, C, etc.): ").strip().upper()
                cursor.execute("SELECT * FROM productos WHERE categoria = %s", (categoria,))
                productos = cursor.fetchall()
                print(Fore.YELLOW + f"\nProductos en la categoría '{categoria}':" + Fore.RESET)
            elif opcion == "3":
                conexion.close()
                break
            else:
                print(Fore.RED + "Opción no válida." + Fore.RESET)
                input("Presione Enter para continuar...")
                continue
            if productos:
                print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
                print("-" * 50)
                for producto in productos:
                    print(f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | {producto[4]} | {producto[5]}")
            else:
                print(Fore.RED + "No se encontraron productos." + Fore.RESET)

            conexion.close()
            input("Presione Enter para continuar...")

def actualizar_producto():
    """Actualizar la cantidad o el precio de un producto específico."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nActualizar Producto" + Fore.RESET)
        print("1. Actualizar cantidad")
        print("2. Actualizar precio")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "3":
            break

        id_producto = int(input("Ingrese el ID del producto a actualizar: "))
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            if opcion == "1":
                nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                if nueva_cantidad <= 0:
                    print(Fore.RED + "La cantidad debe ser mayor a 0." + Fore.RESET)
                    continue
                cursor.execute("""
                    UPDATE productos
                    SET cantidad = %s
                    WHERE id = %s
                """, (nueva_cantidad, id_producto))
                print(Fore.GREEN + "Cantidad actualizada exitosamente." + Fore.RESET)
            elif opcion == "2":
                nuevo_precio = float(input("Ingrese el nuevo precio: "))
                if nuevo_precio <= 0:
                    print(Fore.RED + "El precio debe ser mayor a 0." + Fore.RESET)
                    continue
                cursor.execute("""
                    UPDATE productos
                    SET precio = %s
                    WHERE id = %s
                """, (nuevo_precio, id_producto))
                print(Fore.GREEN + "Precio actualizado exitosamente." + Fore.RESET)
            else:
                print(Fore.RED + "Opción no válida." + Fore.RESET)
                input("Presione Enter para continuar...")
                continue

            conexion.commit()
            conexion.close()
            input("Presione Enter para continuar...")

def reporte_bajo_stock():
    """Generar un reporte de productos con bajo stock."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nReporte de Bajo Stock" + Fore.RESET)
        print("1. Ingresar límite de stock para generar reporte")
        print("2. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "2":
            break

        if opcion == "1":
            limite = int(input("Ingrese el límite de stock: "))
            conexion = crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM productos WHERE cantidad <= %s", (limite,))
                productos = cursor.fetchall()
                conexion.close()

                print(Fore.YELLOW + "\nProductos con bajo stock:" + Fore.RESET)
                if productos:
                    for producto in productos:
                        print(f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | {producto[4]} | {producto[5]}")
                else:
                    print(Fore.RED + "No se encontraron productos con bajo stock." + Fore.RESET)

                input("Presione Enter para continuar...")

def menu():
    """Mostrar el menú principal e interactuar con el usuario."""
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\nMenú Principal" + Fore.RESET)
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Reporte de bajo stock")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "Saliendo del programa..." + Fore.RESET)
            break
        else:
            print(Fore.RED + "Opción no válida." + Fore.RESET)
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu()