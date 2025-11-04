import os
# Importamos las funciones de almacenamiento
from almacenamiento import (
    guardar_libro, 
    mostrar_libros, 
    modificar_libro, 
    eliminar_libro, 
    estadisticas,
    ordenar_libros
)
# Importamos las funciones de la API
from api_libros import buscar_y_guardar_libro, mostrar_libros_api

# Ruta base donde se guardarán los datos (asumiendo que main.py está en 'src' o 'fuente')
BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
BASE_PATH = os.path.abspath(BASE_PATH)
os.makedirs(BASE_PATH, exist_ok=True)
print("Guardando datos de la Biblioteca en:", BASE_PATH)


def mostrar_menu(modo_api=False):
    print("\n=== MENÚ PRINCIPAL - GESTIÓN DE BIBLIOTECA ===")

    if modo_api:
        print("1. 🌎 Buscar y guardar libro (API Google Books)")
        print("8. 📋 Mostrar libros desde API (sin guardar)")
    else:
        print("1. ✍️ Agregar nuevo libro (Manual/Local)")
    
    print("2. 🔍 Mostrar y Filtrar Libros")
    print("3. ✏️ Modificar Libro")
    print("4. 🗑️ Eliminar Libro")
    print("5. 📊 Estadísticas Globales")
    print("6. ⬆️ Ordenar Lista Global")
    print("7. 🚪 Salir")
    print("-------------------------")


def main():
    print("SISTEMA DE GESTIÓN DE BIBLIOTECA (Jerarquía y Recursividad)\n")

    while True:
        print("Seleccioná modo de trabajo:")
        print("1. Local (usar datos guardados en CSV)")
        print("2. API (consultar Google Books)")
        modo = input("Elegí una opción (1 o 2): ")

        if modo == "1":
            modo_api = False
            print("\nModo seleccionado: LOCAL (CSV manual)")
            break
        elif modo == "2":
            modo_api = True
            print("\nModo seleccionado: API de Google Books")
            break
        else:
            print("Opción inválida. Intentá de nuevo.\n")

    while True:
        mostrar_menu(modo_api)
        opcion = input("Elegí una opción: ")
        
        libro_data_input = {}
        
        match opcion:
            case "1":
                if modo_api:
                    buscar_y_guardar_libro(BASE_PATH)
                else:
                    print("\n--- INGRESO DE NUEVO LIBRO ---")
                    # 3 Niveles de Jerarquía
                    libro_data_input['genero'] = input("Nivel 1 (Género, ej: Ciencia Ficcion): ")
                    libro_data_input['autor'] = input("Nivel 2 (Autor, ej: Isaac Asimov): ")
                    libro_data_input['anio'] = input("Nivel 3 (Año de publicación, ej: 1951): ")
                    
                    # Atributos del Ítem
                    libro_data_input['titulo'] = input("Título del libro: ")
                    libro_data_input['paginas'] = input("Cantidad de páginas (Numérico): ")
                    
                    guardar_libro(BASE_PATH, libro_data_input)

            case "2":
                mostrar_libros(BASE_PATH)
            case "3":
                modificar_libro(BASE_PATH)
            case "4":
                 eliminar_libro(BASE_PATH)
            case "5":
                 estadisticas(BASE_PATH)
            case "6":
                 ordenar_libros(BASE_PATH)
            case "7":
                print("¡Hasta luego!")
                break
            case "8":
                if modo_api:
                    mostrar_libros_api()
                else:
                    print("Esta opción solo está disponible en modo API.")

            case _:
                print("Opción no válida. Probá de nuevo.")

if __name__ == "__main__":
    main()