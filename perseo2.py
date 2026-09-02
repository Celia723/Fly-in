
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




def tratar_metadates(prefix: str, metadata: str)-> dict:

    rest = metadata
    metadata_dict = {}

    while rest:
        clave = ""
        valor = ""

        if not "=" in rest :
        raise ValueError("Error de sintaxis en los metadatos, falta el igual")

        clave, _, rest= rest.partition("=")
        valor = rest.split[0]

        #primero tratar mejor si el metadato es valido para el tipo de prefix 

        if clave is in metadata_dict:  #q se repita el metadato
            raise ValueError ("Metadato repetido")
        elif clave is "zone" and valor not in {"restricted", "normal", "priority", "blocked"}: #si la clave es zona y el valor no corresponde
            raise ValueError ("El valor de la zona no existe")
        elif prefix in {"start_hub", "end_hub"} and valor not "color":  #restricciones por prefijo
            raise ValueError ("Hub con metadata no correspondiente")
        elif prefix is "hub" and 

        
        metadata_dict[clave] = valor
        rest = rest.split[1:]
    



def trate_mild_part(prefix: str, mild_part:str)-> list:
    
    clear_tokens = []

    if prefix == "conecction":
        if "-" not in mild_part:
            raise ValueError("Las zonas no están separadas por un guion")
        else:
            zona_a, _, zona_b = mild_part.partition()
            return (zona_a.strip(), zona_b.strip())
    
    else:
        tokens = mild_part.split()
        if tokens.len() not 3:
            raise ValueError ("La sintaxis de la zona esta mal")
        
        else:
            name, x, y = tokens

            if "-" in name:
                raise ValueError ("El nombre de la zona no debe tener guiones")
            
            if is not x.isdigit() or is not y.isdigit():
                raise ValueError ("Las coordenadas deben de ser numeros")

            for t in tokens:
                clear_tokens.append(t.strip())
        
        return clear_tokens
            
        
def parse_line(lines: list[int, str])-> list[str, ]:

    for line in lines:
        prefix = ""
        metadata_dict= {}
        tokens_mild_part = []

        if ":" not in line:
            raise ValueError ("Faltael separador de los dos puntos")
        
        prefix, _, rest = line.partition(":")

        if prefix not in {"start_hub", "end_hub", "hub", "connection"}:
            raise ValueError (f"Prefijo desconocido: {prefix}")
        
        #comprobamos q tengo corchetes para los metadatos
       
        if "[" in rest:
            if "]" in rest:
                mild_part, _, metadates  = rest.partition("[")
                clean_metadates = metadates.rstrip("]").split()
                #TODO crear tratar_metadates
                metadata_dict = tratar_metadates( clean_metadates, prefix)
            
            else:
                raise ValueError("Un [ sin  cerrar")
        else:
            mild_part = rest
        
        tokens_mild_part = trate_mild_part(prefix, mild_part)
 

        









