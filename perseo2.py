
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

    ALLOWED_KEYS = {
    "start_hub": {"color"},
    "end_hub": {"color"},
    "hub": {"color", "max_drones", "zone"},
    "connection": {"max_link_capacity"},
    }

    VALID_ZONES = {"restricted", "normal", "priority", "blocked"}

    rest = metadata
    metadata_dict = {}
    comprobation_repes = []

    while rest:
        clave = ""
        valor = ""


        if not "=" in rest :
            raise ValueError("Error de sintaxis en los metadatos, falta el igual")

        clave, _, rest_despues_igual = rest.partition("=")
        valor = rest_despues_igual.split()[0]

        if not valor:
            raise ValueError("Falta el metadato despues del tipo")

        comprobation_repes.append(clave)

        

        #primero tratar mejor si el metadato es valido para el tipo de prefix 

        if clave in ALLOWED_KEYS[prefix]:
            if clave == "zone":
                if valor not in VALID_ZONES:
                    raise ValueError("Error de zona valida")
            elif clave in {"max_drones", "max_link_capacity"}:
                if not valor.isdigit():
                    raise ValueError("El tipo de metadato debe de ser un numero")
            elif clave == "color":
                if not valor.isalpha():
                    raise ValueError("El color no es valido")
        else: 
            raise ValueError("Metadato invalido para el tipo de hub o conexion")

        if len(comprobation_repes) != len(set(comprobation_repes)):
            raise ValueError("Metadato repetido")
        
        metadata_dict[clave] = valor
        rest_partitionated = rest_despues_igual.split()[1:]
        rest = " ".join(rest_partitionated)

    return metadata_dict
    

def trate_mild_part(prefix: str, mild_part:str)-> list:
    
    clear_tokens = []

    if prefix == "conecction":
        if "-" not in mild_part:
            raise ValueError("Las zonas no están separadas por un guion")
        else:
            zona_a, _, zona_b = mild_part.partition("-")
            return (zona_a.strip(), zona_b.strip())
    
    else:
        tokens = mild_part.split()
        if len(tokens) != 3:
            raise ValueError ("La sintaxis de la zona esta mal")
        
        else:
            name, x, y = tokens

            if "-" in name:
                raise ValueError ("El nombre de la zona no debe tener guiones")
            
            if not x.isdigit() or not y.isdigit():
                raise ValueError ("Las coordenadas deben de ser numeros")

            for t in tokens:
                clear_tokens.append(t.strip())
        
        return clear_tokens
            
        

def get_nb_drones(data_line: tuple[int, str]):
    
    num_line, line = data_line

    if not ":" in line:
        raise ValueError(f"no : in line: {num_line}")

    nb_drones, _, num_drones = line.partition(":")

    if nb_drones.strip() != "nb_drones":
        raise ValueError("It must be there a nb_drones")
    elif not num_drones.strip().isdigit():
        raise ValueError("nb_drones must be a number")

    else:
        return num_drones


def parse_lines(lines: list[tuple[int, str]])-> tuple[str, list[tuple] ]:

    clean_data_lines: list[tuple] = []
    final_result : tuple[str, list[tuple] ] = []

    nb_drones = get_nb_drones(lines[0])

    for num_line, texto_line in lines[1:]:
        prefix = ""
        metadata_dict= {}
        tokens_mild_part = []

        if ":" not in texto_line:
            raise ValueError ("Faltael separador de los dos puntos")
        
        prefix, _, rest = texto_line.partition(":")

        if prefix not in {"start_hub", "end_hub", "hub", "connection"}:
            raise ValueError (f"Prefijo desconocido: {prefix}")
        
        #comprobamos q tengo corchetes para los metadatos
       
        try:
            if "[" in rest:
                if "]" in rest:
                    mild_part, _, metadates  = rest.partition("[")
                    clean_metadates = metadates.rstrip("]")
                    metadata_dict = tratar_metadates( clean_metadates, prefix)
                
                else:
                    raise ValueError("Un [ sin  cerrar")
            else:
                mild_part = rest
        
            tokens_mild_part = trate_mild_part(prefix, mild_part)
        except ValueError as e:
            print(f"Sintax error in line {num_line}: {e}")

        clean_data_lines.append((prefix,tokens_mild_part, metadata_dict))
    
    final_result = [nb_drones, clean_data_lines]

    return final_result


        
if __name__ == "__main__":
    
    file = "C:\\Cursus 42 Madrid\\fly-in\\maps\\easy\\01_linear_path.txt"

    #obtenemos las lineas limpias del texto con su numero
    lines: list[tuple[int, str]] = clean_tex(file)

    
    clean_data: tuple[str, list[tuple[str, str, list[str], dict]]] = parse_lines(lines)



    


    









