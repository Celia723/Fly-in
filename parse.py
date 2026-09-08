def clean_text(file_path: str) -> list[tuple[int, str]]:
    """Read a map file and extract valid content lines with line numbers."""
    clean_lines: list[tuple[int, str]] = []
    try:
        with open(file_path, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                clean_lines.append((line_num, line))
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file {file_path}: {e}")

    return clean_lines


def get_nb_drones(first_line: tuple[int, str]) -> int:
    """Extract and validate the number of drones from the first active line."""
    line_num, line_text = first_line

    if ":" not in line_text:
        raise ValueError(
            f"Line {line_num}: invalid format for nb_drones, missing ':'"
        )

    prefix, _, value = line_text.partition(":")

    if prefix.strip() != "nb_drones":
        raise ValueError(
            f"Line {line_num}: first active line must be 'nb_drones'"
        )

    value_clean = value.strip()
    if not value_clean.isdigit():
        raise ValueError(
            f"Line {line_num}: 'nb_drones' must be a positive integer"
        )

    nb_drones = int(value_clean)
    if nb_drones <= 0:
        raise ValueError(
            f"Line {line_num}: number of drones must be greater than 0"
        )

    return nb_drones


def is_prefix_valid(line: str) -> bool:
    """Check if the line prefix exists and is allowed for elements."""
    if ":" not in line:
        return False

    prefix = line.split(":", 1)[0].strip()
    return prefix in {"start_hub", "end_hub", "hub", "connection"}


def parse_middle_part(line: str) -> list[str]:
    """Validate and clean the middle component between ':' and '['."""
    prefix, _, after = line.partition(":")

    if "[" not in after:
        middle_part = after
    else:
        middle_part, _, _ = after.partition("[")

    components = middle_part.split()

    if prefix.strip() != "connection":
        if len(components) != 3:
            raise ValueError(
                "Middle part must contain 3 elements (name x y)"
            )

        name = components[0]
        if " " in name or "-" in name:
            raise ValueError("Hub name cannot contain spaces or dashes")

        for coord in components[1:]:
            if not coord.isdigit():
                if coord.startswith("-") and coord[1:].isdigit():
                    continue
                raise ValueError("Coordinates must be valid integers")

        return components
    else:
        if "-" not in middle_part:
            raise ValueError("Connection must contain '-' between hubs")

        conn_a, _, conn_b = middle_part.partition("-")
        hub_a = conn_a.strip()
        hub_b = conn_b.strip()

        if not hub_a or not hub_b:
            raise ValueError("Invalid connected hubs in connection definition")

        return [hub_a, hub_b]


def assign_values(prefix: str, key: str, value: str) -> bool:
    """Check if the metadata key and value are allowed for the given prefix."""
    ALLOWED_KEYS = {
        "start_hub": {"color"},
        "end_hub": {"color"},
        "hub": {"color", "max_drones", "zone"},
        "connection": {"max_link_capacity"},
    }
    VALID_ZONES = {"restricted", "normal", "priority", "blocked"}

    if prefix not in ALLOWED_KEYS or key not in ALLOWED_KEYS[prefix]:
        raise ValueError(f"Metadata '{key}' is not allowed for '{prefix}'")

    if key == "zone" and value not in VALID_ZONES:
        raise ValueError(f"Invalid zone value: {value}")
    elif key in {"max_drones", "max_link_capacity"} and not value.isdigit():
        raise ValueError(f"Value for '{key}' must be a positive integer")
    elif key == "color" and not value.isalpha():
        raise ValueError(f"Invalid color value: {value}")

    return True


def parse_metadata(line: str, prefix: str) -> dict[str, str]:
    """Parse metadata key-value pairs between '[' and ']'."""
    if "[" not in line or "]" not in line:
        return {}

    _, _, meta_part = line.partition("[")
    meta_part = meta_part.rstrip("]").strip()

    metadata_dict = {}
    seen_keys = set()
    rest = meta_part

    while rest:
        if "=" not in rest:
            raise ValueError("Missing '=' in metadata declaration")

        key, _, rest_after_equal = rest.partition("=")
        key = key.strip()
        parts = rest_after_equal.split()

        if not parts:
            raise ValueError(f"Missing value for metadata key '{key}'")

        value = parts[0]

        if key in seen_keys:
            raise ValueError(f"Duplicate metadata key: {key}")
        seen_keys.add(key)

        assign_values(prefix, key, value)
        metadata_dict[key] = value

        rest = " ".join(parts[1:])

    return metadata_dict


def parse_syntax(lines: list[tuple[int, str]]) -> tuple[int, list[tuple]]:
    """Validate map syntax. Returns (nb_drones, parsed_elements)."""
    if not lines:
        raise ValueError("Map file is empty")

    nb_drones = get_nb_drones(lines[0])
    parsed_elements = []

    for line_num, line_text in lines[1:]:
        if not is_prefix_valid(line_text):
            raise ValueError(f"Line {line_num}: invalid line prefix")

        prefix = line_text.split(":", 1)[0].strip()

        try:
            middle = parse_middle_part(line_text)
            metadata = parse_metadata(line_text, prefix)
            parsed_elements.append((prefix, middle, metadata))
        except ValueError as e:
            raise ValueError(f"Syntax error at line {line_num}: {e}")

    return nb_drones, parsed_elements


if __name__ == "__main__":
    file_path = "maps/easy/02_simple_fork.txt"

    clean_lines = clean_text(file_path)
    if clean_lines:
        try:
            nb_drones, parsed_data = parse_syntax(clean_lines)
            print(f"Drones detected: {nb_drones}")
            print(f"Processed valid lines: {len(parsed_data)}")
        except ValueError as e:
            print(e)