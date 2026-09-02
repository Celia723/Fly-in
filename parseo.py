
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


    def prefix_ok(line: str) -> bool:
        """
        comprueba el prefijo (lo de antes de los dos puntos esta bien).
        tmb compruebo q haya dos puntos

        Args:
        La linea tal cual

        Returns:
        true --> esta bien,  false -> esta mal
        
        """

        prefix = ""

        if ":" not in line:
            return false
        
        prefix = line.split(":", 1)
        prefix_clean = prefix[0].strip()

        if prefix_clean not "start_hub" or prefix_clean not "end_hub" or prefix_clean not "hub" or prefix_clean not "connection":
            return False
        
        else:
            return True


def inter_ok(line: str)-> list[]:
    """
    coge la parte intermedia de la linea (la de despues de los dos puntos y antes de los corchetes).
    Comprueba su sintaxis dependiendo tmb si es connection u otra cosa (son distintos criterios)
    

    Args:
    la linea del texto entera

    Returns:
    una lista de los  componentes del medio bien limpitos

    Raised:
    error si la sintaxis va mal 
    """
    components_mild_part = []
    components_mild_part_conecction = []


    prefix, sep, after = linea.partition(":")
    

    if "[" not in after:
        mild_part = after
    else:
        mild_part, bracket , metadata = after.partition("[")

    components_mild_part = mild_part.split()

    if prefix.strip() not "connection":
        for c in range(3):
            if c == 0:
                if " " in components_mild_part[c] or "-" in components_mild_part[c]:
                    raise ValueError
            else:
                if not components_mild_part[c].isdigit():
                    raise ValueError
        
        return components_mild_part
    else:
        if "-" not in mild_part:
            raise ValueError
        connection1, dash, connection2 = mild_part.partition("-")

        zone_a = connection1.strip()
        zone_b =  connection2.strip()


        if not zone_a or not zone_b:
            raise ValueError
        else:
            components_mild_part_conecction.append(zone_a, zone_b)
            return components_mild_part_conecction



def asignar_values(metadates: dict, prefix: str, key: str, value: str) -> dict:
    """
    coge el valor de la key y mira a ver si es una key valida (compara tmb con el prefix).
    Tmb mira 
    """



            
def metadata_ok(line: str, prefix: str) -> list[]:
    """
    si hay metadata analiza cada una de sus partes para ver la sintaxis

    Args:
    linea limpia entera y el prefijo para ver q tipo de metadata puede tener

    Returns:
    si hay metadata una lista con los metados, si no, una lista vacia

    Raised:
    una excepticion si la sintaxis esta mal
    """
    metadates = []
    meta_part = ""

    if not "[" in line or not "]" :
        return []
    
    x, y, meta_part = line.partition["["].[2]

    #ahora con la mparte de los metadatos , vamos a hacer un bulce
    while rest:
        if rest == "]":
            break
        key, equal, rest = meta_part.partition("=")
        parts_rest = rest.split()
        value = parts_rest[0]

        asignar_values(prefix)
        rest = join.parts_rest[1:]

    
    


        




def okey_sintax(lines: list[tuple[int, str]]) -> list[list]:
    """
        comprobamos si es valida la sintxis de las lineas y obtenemso los datos para crear los objetos

        Args:
            lines: lineas sin comentarios ni lineas blancas. LIMPIAS para el parseo
        
        Returns:
           una lista con listas de todos los datos de las lineas
        
    """

    result = []
    for line in lines:
        prefix = ""
        midel = []
        metadata = []

        try:
            prefix = prefix_ok(line[1]):7
        except ValueError:
           print(f"Error de sintaxis en la linea : {line[0]}")
        
        try:
            midel = inter_ok(line[1])
        except ValueError:
            print(f"Error de sintaxis en la linea : {line[0]}")
        
        try:
            metadata = metadata_ok(line[1])
        except ValueError:
            print(f"Error de sintaxis en la linea : {line[0]}")
        
        

    

