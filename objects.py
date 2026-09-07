class Hub:

    def __init__(self, name: str, x: int, y: int, metadata: dict):
        self.name: str = name
        self.x: int = x
        self.y: int = y

        self.color: str | None = metadata.get("color", None)
        self.zone: str = metadata.get("zone", "normal")
        self.max_drones: int = int(metadata.get("max_drones", 1))


class StartHub(Hub):

    def __init__(self, name: str, x: int, y: int, metadata: dict):
        super().__init__(name, x, y, metadata)
        self.max_drones: float = float("inf")  # Capacidad infinita


class EndHub(Hub):

    def __init__(self, name: str, x: int, y: int, metadata: dict):
        super().__init__(name, x, y, metadata)
        self.max_drones: float = float("inf")  # Capacidad infinita

class Connection:
    def __init__(self, name: str, conecction_a: str, conecction_b: str, metadata: dict):
        self.name: str = name
        self.conecction_a: str = conecction_a
        self.conecction_b: str = conecction_b

    self.max_link_capacity: int = int(metadata.get("max_link_capacity", 1))


class Grapho:
    def __init__(hub_list: tuple[str, Hub], coordenates: set(tuple), conexion_list: list, start_hub: StartHub, end_hub: EndHub):
        self.hub_list = hub_list
        self.coordenates = coordenates
        self.conexion_list = conexion_list
        self.start_hub = start_hub
        self.end_hub = end_hub

        