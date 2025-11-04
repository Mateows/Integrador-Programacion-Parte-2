import os
import csv
from typing import List, Dict, Tuple, Any, Optional

# --- CONFIGURACIÓN DE LA JERARQUÍA (BIBLIOTECA) ---
# Estructura: base_path/genero/autor/anio/
JERARQUIA_NIVELES = ['genero', 'autor', 'anio']
CSV_HEADERS = ["Título", "Páginas"] # Atributos del ítem final

# --- FUNCIONES DE MANIPULACIÓN DE RUTAS Y CREACIÓN JERÁRQUICA (os) ---

def ensure_path_for_book(base_path: str, niveles: Dict[str, str]) -> str:
    """
    Crea la estructura de carpetas jerárquica (genero/autor/anio/) 
    si no existe y devuelve la ruta completa del archivo CSV final.
    """
    ruta_dir = os.path.join(
        base_path, 
        niveles['genero'], 
        niveles['autor'], 
        str(niveles['anio']) # Aseguramos que el año sea string para la ruta
    )
    
    # Crear la estructura de carpetas de forma dinámica (os.makedirs)
    os.makedirs(ruta_dir, exist_ok=True)
    
    return os.path.join(ruta_dir, "items.csv")


# --- FUNCIONES DE VALIDACIÓN ESTRICTA (Fase 3, Punto 1) ---

def validar_entrada_libro(data: Dict[str, str]) -> Tuple[bool, str | Dict[str, Any]]:
    """
    Aplica validaciones estrictas al nuevo ítem Libro.
    """
    
    # 1. Validar que no estén vacíos
    required_fields = ['genero', 'autor', 'anio', 'titulo', 'paginas']
    if not all(data.get(field, '').strip() for field in required_fields):
        return False, "Todos los campos (Género, Autor, Año, Título, Páginas) son obligatorios."

    # 2. Validar tipo de dato numérico
    try:
        anio_int = int(data['anio'].strip())
        paginas_int = int(data['paginas'].strip())
    except ValueError:
        return False, "Año y Páginas deben ser valores numéricos enteros."

    # 3. Validar lógica de negocio (Valores positivos)
    if anio_int <= 0 or paginas_int <= 0:
        return False, "El Año de publicación y la Cantidad de Páginas deben ser positivos y mayores a cero."

    # Si pasa todas las validaciones, retorna True con el diccionario limpio
    libro_data = {
        "genero": data['genero'].strip(),
        "autor": data['autor'].strip(),
        "anio": anio_int,
        "titulo": data['titulo'].strip(),
        "paginas": paginas_int,
    }
    return True, libro_data


# --- LECTURA RECURSIVA OBLIGATORIA (Fase 2, Punto 2) ---

def leer_csv_a_diccionarios(ruta_csv: str, niveles_jerarquia: Dict[str, str]) -> List[Dict]:
    """Lee un CSV y lo convierte en lista de diccionarios, incluyendo la jerarquía."""
    libros_list = []
    
    try:
        with open(ruta_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None) # Saltar encabezado (Título, Páginas)
            
            if not headers or len(headers) < 2:
                return libros_list

            for fila in reader:
                if len(fila) >= 2:
                    try:
                        paginas_int = int(fila[1])
                    except ValueError:
                        continue # Ignorar fila si las páginas no son un número
                        
                    # Crear el diccionario (el patrón de datos exigido)
                    libros_list.append({
                        "genero": niveles_jerarquia['genero'], 
                        "autor": niveles_jerarquia['autor'], 
                        "anio": niveles_jerarquia['anio'],
                        "titulo": fila[0],
                        "paginas": paginas_int,
                        # ID simple para identificación en CRUD
                        "id": f"{niveles_jerarquia['genero']}/{niveles_jerarquia['autor']}/{fila[0]}", 
                        "ruta_csv": ruta_csv # Para saber dónde sobrescribir
                    })
                        
    except FileNotFoundError:
        pass 
    except OSError:
        pass 
        
    return libros_list


def consolidar_libros_recursivamente(ruta_actual: str, lista_global: List[Dict]) -> List[Dict]:
    """
    Función recursiva OBLIGATORIA (Fase 2) para recorrer la jerarquía y consolidar los datos.
    """
    
    # 1. Caso Base 1: Encontrar el archivo CSV
    if os.path.basename(ruta_actual) == "items.csv":
        partes = ruta_actual.split(os.sep)
        # Tomamos los 3 niveles (Genero/Autor/Anio) antes de items.csv
        if len(partes) >= 4:
            niveles_jerarquia = {
                'genero': partes[-4],
                'autor': partes[-3],
                'anio': partes[-2],
            }
            libros_csv = leer_csv_a_diccionarios(ruta_actual, niveles_jerarquia)
            lista_global.extend(libros_csv)
        return

    # Caso Base 2: Si es un archivo que no es items.csv
    if os.path.isfile(ruta_actual):
        return

    # 2. Paso Recursivo: Si es un directorio
    try:
        elementos = os.listdir(ruta_actual)
    except Exception:
        return
        
    for elemento in elementos:
        ruta_hijo = os.path.join(ruta_actual, elemento)
        consolidar_libros_recursivamente(ruta_hijo, lista_global)

    return lista_global


# --- FUNCIONES DE PERSISTENCIA (CSV) Y MANEJO DE EXCEPCIONES ---

def guardar_datos_csv(ruta_csv: str, libros_en_memoria: List[Dict]):
    """Sobrescribe un archivo CSV específico (modo 'w') con la lista de diccionarios actualizada."""
    if not libros_en_memoria:
        try:
            if os.path.exists(ruta_csv):
                os.remove(ruta_csv)
            return
        except OSError as e:
            print(f"❌ Error al intentar eliminar el archivo vacío {ruta_csv}: {e}")
            return
    
    try:
        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for libro in libros_en_memoria:
                writer.writerow({'Título': libro['titulo'], 'Páginas': libro['paginas']})

    except OSError as e:
        print(f"❌ Error al escribir en el archivo {ruta_csv}: {e}")


def guardar_libro(base_path: str, data_input: Dict[str, str]):
    """
    Alta de Nuevo Ítem (Creación Jerárquica) - Única que puede crear nuevas carpetas.
    """
    es_valido, resultado = validar_entrada_libro(data_input)
    
    if not es_valido:
        print(f"\n❌ Error de validación: {resultado}")
        return

    libro_data: Dict[str, Any] = resultado
    
    niveles_jerarquia = {
        'genero': libro_data['genero'], 
        'autor': libro_data['autor'], 
        'anio': libro_data['anio']
    }
    
    try:
        ruta_csv = ensure_path_for_book(base_path, niveles_jerarquia)
        existe = os.path.exists(ruta_csv)

        with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(CSV_HEADERS) 
            
            writer.writerow([libro_data['titulo'], libro_data['paginas']])

        print(f"\n✅ Libro '{libro_data['titulo']}' guardado jerárquicamente en {ruta_csv}")
        
    except OSError as e:
        print(f"❌ Error del sistema de archivos al guardar el libro: {e}")


# --- FUNCIONALIDADES (CRUD y Consultas) ---

def mostrar_libros(base_path: str):
    """
    Muestra ítems totales y permite filtrado, usando la lectura recursiva.
    """
    lista_libros = consolidar_libros_recursivamente(base_path, []) 
    
    if not lista_libros:
        print("\nNo hay ítems registrados en la estructura de archivos.")
        return

    print("\n📚 LISTADO GLOBAL DE LIBROS\n")
    
    atributo_filtro = input("¿Desea filtrar la lista? (titulo/autor/genero/no): ").lower().strip()
    
    libros_a_mostrar = lista_libros
    
    if atributo_filtro in ["titulo", "autor", "genero"]:
        valor_filtro = input(f"Ingrese el valor a filtrar por {atributo_filtro}: ").strip()
        if valor_filtro:
            libros_a_mostrar = [
                libro for libro in libros_a_mostrar 
                if valor_filtro.lower() in str(libro.get(atributo_filtro, "")).lower()
            ]
            print(f"\nMostrando {len(libros_a_mostrar)} libros filtrados.")

    if not libros_a_mostrar:
        print("No se encontraron libros con ese criterio de filtrado.")
        return

    print("---")
    for i, libro in enumerate(libros_a_mostrar, start=1):
        print(f"[{i}] ID: {libro['id']}")
        print(f"    Título: {libro['titulo']} ({libro['paginas']} pgs)")
        print(f"    Ubicación: {libro['genero']} / {libro['autor']} / {libro['anio']}")
        print("---")


def _seleccionar_item_por_id(base_path: str, operacion: str) -> Tuple[List[Dict], int]:
    """Función auxiliar para buscar un ítem por ID."""
    
    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("No hay libros registrados para esta operación.")
        return [], -1

    print(f"\n{operacion.upper()} LIBRO\n")
    print("Libros disponibles (ID: Genero/Autor/Titulo):")
    
    for i, libro in enumerate(lista_libros, start=1):
        print(f"[{i}] {libro.get('id', libro['titulo'])}") # Usamos .get() por seguridad
        
    try:
        indice = int(input(f"\nElegí el número del libro a {operacion}: "))
        if indice < 1 or indice > len(lista_libros):
            print("Número inválido.")
            return [], -1
    except ValueError:
        print("Debes ingresar un número.")
        return [], -1
        
    return lista_libros, indice - 1


def modificar_libro(base_path: str):
    """
    Modificación de Item (Actualización/Update)
    """
    
    lista_libros, indice_global = _seleccionar_item_por_id(base_path, "modificar")
    
    if indice_global == -1:
        return

    libro_a_modificar = lista_libros[indice_global]
    ruta_csv_original = libro_a_modificar['ruta_csv']
    
    print(f"\nModificando: {libro_a_modificar['id']}")

    nuevo_titulo = input(f"Nuevo título (actual: {libro_a_modificar['titulo']}, dejar vacío para no cambiar): ").strip()
    nuevas_paginas_str = input(f"Nuevas páginas (actual: {libro_a_modificar['paginas']}, dejar vacío para no cambiar): ").strip()

    if nuevo_titulo:
        libro_a_modificar['titulo'] = nuevo_titulo
        # Actualizar ID
        libro_a_modificar['id'] = f"{libro_a_modificar['genero']}/{libro_a_modificar['autor']}/{nuevo_titulo}"

    if nuevas_paginas_str:
        try:
            paginas_int = int(nuevas_paginas_str)
            if paginas_int <= 0:
                print("❌ Validación fallida: Las páginas deben ser positivas. Modificación cancelada.")
                return
            libro_a_modificar['paginas'] = paginas_int
        except ValueError:
            print("❌ Validación fallida: Las páginas deben ser un número entero. Modificación cancelada.")
            return
    
    libros_mismo_csv = [lib for lib in lista_libros if lib['ruta_csv'] == ruta_csv_original]
    
    guardar_datos_csv(ruta_csv_original, libros_mismo_csv)

    print(f"\n✅ Libro modificado correctamente. Archivo actualizado: {ruta_csv_original}")


def eliminar_libro(base_path: str):
    """
    Eliminación de Ítem (Baja/Delete)
    """
    
    lista_libros, indice_global = _seleccionar_item_por_id(base_path, "eliminar")
    
    if indice_global == -1:
        return

    libro_a_eliminar = lista_libros[indice_global]
    ruta_csv_original = libro_a_eliminar['ruta_csv']

    confirm = input(f"¿Seguro que querés eliminar '{libro_a_eliminar['titulo']}'? (s/n): ").lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    libros_mismo_csv_actualizado = [
        lib for i, lib in enumerate(lista_libros)
        if lib['ruta_csv'] == ruta_csv_original and i != indice_global
    ]
    
    try:
        guardar_datos_csv(ruta_csv_original, libros_mismo_csv_actualizado)
        print(f"\n✅ Libro '{libro_a_eliminar['titulo']}' eliminado correctamente.")
    except Exception as e:
        print(f"\n❌ Falló la eliminación. Problemas de escritura en {ruta_csv_original}: {e}")


def ordenar_libros(base_path: str):
    """
    Permite ordenar la lista completa de ítems por al menos dos atributos.
    """
    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("No hay libros para ordenar.")
        return

    print("\n⬆️ ORDENAR LIBROS\n")
    print("Atributos disponibles: 1. Título, 2. Páginas, 3. Género, 4. Autor")
    
    clave1_str = input("Elegí el atributo principal para ordenar (titulo/paginas/genero/autor): ").lower().strip()
    clave2_str = input("Elegí el atributo secundario (opcional, dejar vacío): ").lower().strip()
    
    if clave1_str not in ["titulo", "paginas", "genero", "autor"]:
        print("Opción de ordenamiento principal inválida.")
        return

    orden_asc = input("Orden ascendente (asc) o descendente (desc)? ").lower().startswith('a')
    
    if clave2_str in ["titulo", "paginas", "genero", "autor"]:
        lista_libros.sort(key=lambda x: (x.get(clave1_str, ""), x.get(clave2_str, "")), reverse=not orden_asc)
        criterio = f"{clave1_str.capitalize()} y {clave2_str.capitalize()}"
    else:
            # Ordenamiento por una sola clave
            lista_libros.sort(key=lambda x: x.get(clave1_str, ""), reverse=not orden_asc) # <-- Corregido
            criterio = clave1_str.capitalize()
    print(f"\nLista ordenada por {criterio} ({'Ascendente' if orden_asc else 'Descendente'}):")
    
    print("---")
    for i, libro in enumerate(lista_libros[:15], start=1): 
        print(f"[{i}] {libro['titulo']} | Páginas: {libro['paginas']} | {criterio}: {libro[clave1_str]}")
    print("---")


def estadisticas(base_path: str):
    """
    Calcula y muestra estadísticas básicas globales.
    """

    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("\nNo hay libros registrados para calcular estadísticas.")
        return

    print("\n📊 ESTADÍSTICAS GLOBALES DE LIBROS\n")

    total_libros = len(lista_libros)
    total_paginas = 0
    libros_por_genero: Dict[str, int] = {}

    for libro in lista_libros:
        genero = libro['genero']
        libros_por_genero[genero] = libros_por_genero.get(genero, 0) + 1
        
        try:
            paginas = int(libro['paginas'])
            total_paginas += paginas
        except (ValueError, TypeError):
            pass

    promedio_paginas = (total_paginas / total_libros) if total_libros > 0 else 0

    print(f"Total de libros registrados: {total_libros}")
    print(f"Promedio de páginas por libro: {promedio_paginas:.2f}")
    print("\nRecuento por Género (Categoría de Primer Nivel):")
    for genero, count in sorted(libros_por_genero.items(), key=lambda item: item[1], reverse=True):
        print(f"  - {genero}: {count} libros")

