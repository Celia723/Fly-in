def clean_tex(file: str) -> list[tuple[int, str]]:
    """Lee un fichero de mapa y extrae las líneas de contenido válidas."""
    lines_clean: list[tuple[int, str]] = []
    try:
        with open(file, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                if line.startswith("#") or not line:
                    continue
                else:
                    lines_clean.append((line_num, line))
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file {file}: {e}")

    return lines_clean


def get_nb_drones(first_line: tuple[int, str]) -> int:
    """Extrae y valida el número de drones de la primera línea útil del mapa."""
    line_num, line_text = first_line

    if ":" not in line_text:
        raise ValueError(f"Línea {line_num}: formato incorrecto en nb_drones, falta ':'")

    prefix, _, value = line_text.partition(":")

    if prefix.strip() != "nb_drones":
        raise ValueError(f"Línea {line_num}: la primera línea debe ser 'nb_drones'")

    value_clean = value.strip()
    if not value_clean.isdigit():
        raise ValueError(f"Línea {line_num}: 'nb_drones' debe ser un entero positivo")

    nb_drones = int(value_clean)
    if nb_drones <= 0:
        raise ValueError(f"Línea {line_num}: el número de drones debe ser mayor que 0")

    return nb_drones


def prefix_ok(line: str) -> bool:
    """Comprueba que el prefijo existe y es uno de los permitidos para elementos."""
    if ":" not in line:
        return False
            
    prefix_parts = line.split(":", 1)
    prefix_clean = prefix_parts[0].strip()

    if prefix_clean not in {"start_hub", "end_hub", "hub", "connection"}:
        return False
    else:
        return True


def inter_ok(line: str) -> list[str]:
    """Valida y limpia la parte intermedia (entre ':' y '[')."""
    prefix, sep, after = line.partition(":")
    
    if "[" not in after:
        mild_part = after
    else:
        mild_part, bracket, metadata = after.partition("[")

    components_mild_part = mild_part.split()

    if prefix.strip() != "connection":
        if len(components_mild_part) != 3:
            raise ValueError("La parte intermedia debe tener 3 elementos (nombre x y)")

        for c in range(3):
            if c == 0:
                if " " in components_mild_part[c] or "-" in components_mild_part[c]:
                    raise ValueError("El nombre no puede tener espacios ni guiones")
            else:
                if not components_mild_part[c].isdigit():
                    if components_mild_part[c][0] == "-" and  components_mild_part[c][1:].isdigit():
                        continue
                    else:
                        raise ValueError("Las coordenadas deben ser números")
        
        return components_mild_part
    else:
        if "-" not in mild_part:
            raise ValueError("Las conexiones deben llevar '-'")
            
        connection1, dash, connection2 = mild_part.partition("-")
        zone_a = connection1.strip()
        zone_b = connection2.strip()

        if not zone_a or not zone_b:
            raise ValueError("Zonas de conexión inválidas")
        else:
            return [zone_a, zone_b]


def asignar_values(prefix: str, key: str, value: str) -> bool:
    """Comprueba si la clave de metadato y su valor son válidos para el prefijo."""
    ALLOWED_KEYS = {
        "start_hub": {"color"},
        "end_hub": {"color"},
        "hub": {"color", "max_drones", "zone"},
        "connection": {"max_link_capacity"},
    }
    VALID_ZONES = {"restricted", "normal", "priority", "blocked"}

    if prefix not in ALLOWED_KEYS or key not in ALLOWED_KEYS[prefix]:
        raise ValueError(f"Metadato '{key}' no permitido para '{prefix}'")

    if key == "zone" and value not in VALID_ZONES:
        raise ValueError(f"Zona no válida: {value}")
    elif key in {"max_drones", "max_link_capacity"} and not value.isdigit():
        raise ValueError(f"El valor de {key} debe ser un número")
    elif key == "color" and not value.isalpha():
        raise ValueError(f"Color no válido: {value}")

    return True


def metadata_ok(line: str, prefix: str) -> dict:
    """Analiza la metadatos entre '[' y ']' si existen."""
    if "[" not in line or "]" not in line:
        return {}

    _, _, meta_part = line.partition("[")
    meta_part = meta_part.rstrip("]").strip()
    
    metadata_dict = {}
    comprobation_repes = []
    rest = meta_part

    while rest:
        if "=" not in rest:
            raise ValueError("Falta el '=' en los metadatos")

        key, _, rest_after_equal = rest.partition("=")
        key = key.strip()
        parts = rest_after_equal.split()

        if not parts:
            raise ValueError(f"Falta valor para la clave {key}")

        value = parts[0]

        if key in comprobation_repes:
            raise ValueError(f"Metadato repetido: {key}")
        comprobation_repes.append(key)

        asignar_values(prefix, key, value)
        metadata_dict[key] = value

        rest = " ".join(parts[1:])

    return metadata_dict


def okey_sintax(lines: list[tuple[int, str]]) -> tuple[int, list[tuple]]:
    """Comprueba la sintaxis del mapa. Devuelve (nb_drones, elementos_parsed)."""
    if not lines:
        raise ValueError("El mapa está vacío")

    # 1. Extraemos el número de drones obligatoriamente de la 1ª línea
    nb_drones = get_nb_drones(lines[0])

    result = []
    # 2. Procesamos desde la 2ª línea en adelante el resto del mapa
    for num_line, line_text in lines[1:]:
        if not prefix_ok(line_text):
            print(f"Error de prefijo en línea: {num_line}")
            continue

        prefix = line_text.split(":", 1)[0].strip()

        try:
            midel = inter_ok(line_text)
            metadata = metadata_ok(line_text, prefix)
            result.append((prefix, midel, metadata))
        except ValueError as e:
            raise ValueError(f"Error de sintaxis en línea {num_line}: {e}")

    return nb_drones, result


if __name__ == "__main__":
    file_path = "maps/easy/02_simple_fork.txt"
    #file_path = "maps/easy/01_linear_path.txt"
    #file_path = "maps/easy/03_basic_capacity.txt"
    #file_path = "maps/medium/01_dead_end_trap.txt"
    #file_path = "maps/medium/02_circular_loop.txt"
    #file_path = "maps/medium/03_priority_puzzle.txt"

    lines = clean_tex(file_path)
    if lines:
        try:
            nb_drones, parsed_data = okey_sintax(lines)
            print(f" Drones detectados: {nb_drones}")
            print(f" Líneas válidas procesadas: {len(parsed_data)}")
            
        except ValueError as e:
            print(e)
