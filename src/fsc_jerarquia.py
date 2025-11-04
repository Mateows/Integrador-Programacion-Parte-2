import os
from typing import Dict


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
    try:
        os.makedirs(ruta_dir, exist_ok=True)
        print(f"📁 Carpeta verificada o creada: {ruta_dir}")
    except OSError as e:
        print(f"❌ Error al crear la estructura de carpetas {ruta_dir}: {e}")
        return None

    return os.path.join(ruta_dir, "items.csv")
