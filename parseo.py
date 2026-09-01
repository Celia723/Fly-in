
def clean_tex(file: str) -> list[tuple[int, str]]:
    """Lee un fichero de mapa y extrae las líneas de contenido válidas.

    Args:
        file_path: Ruta al archivo de texto del mapa.

    Returns:
        Una lista de tuplas donde cada elemento contiene el número de línea
        original (empezando en 1) y el texto procesado sin espacios.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta dada.
        PermissionError: Si no hay permisos para leer el archivo.
    """

    lines_clean: list[tuple[int, str]] = []
    try:
        with open(file, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                if line.startswith("#"):
                    continue
                elif not line:
                    continue
                else:
                    lines_clean.append((line_num, line))
    #   captura error de lectura
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file{file}: {e}")

    return lines_clean

#   comprobamos su sintaxis
#   y si va bien  y no salta ningun errror (con el numero de linea)  la converitimos en objeto
def okey_sintax(lines: list) -> None:
    """
        comprobamos si es valida la sintxis de las lineas

        Args:
            lines: lineas sin comentarios ni lineas blancas. LIMPIAS para el parseo
        
        Returns:
            true si está todo con 

        Raise:

    """


