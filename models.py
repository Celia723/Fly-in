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
    def __init__(self, zone_a: str, zone_b: str, metadata: dict):
        self.zone_a: str = zone_a
        self.zone_b: str = zone_b
        self.max_link_capacity: int = int(metadata.get("max_link_capacity", 1))


class Grapho:
    def __init__(self, nb_drones: int):
        self.nb_drones = nb_drones

        self.hubs: dict[str, Hub] = {}
        self.coordenates: set[tuple[int, int]] = set()

        self.connections: list[Connection] = []

        self.connection_pairs: set[tuple[str, str]] = set()

        self.start_hub: StartHub | None = None
        self.end_hub: EndHub | None = None

        self.neighbors = {}
    
    def add_connection(self, connection: Connection) -> None:
        # 1. Comprobar autociclo
        if connection.zone_a == connection.zone_b:
            raise ValueError("A connection cannot link a hub to itself")

        # 2. Comprobar que ambos hubs existen en el grafo
        if connection.zone_a not in self.hubs or connection.zone_b not in self.hubs:
            raise ValueError("Connection requires hubs that do not exist")

        # 3. Ordenar los nombres alfabéticamente para normalizar la dirección
        if connection.zone_a > connection.zone_b:
            connection.zone_a, connection.zone_b = (
                connection.zone_b,
                connection.zone_a,
            )

        # 4. Comprobar si ya existe la tupla ordenada en nuestro set de control
        pair = (connection.zone_a, connection.zone_b)
        if pair in self.connection_pairs:
            raise ValueError("The connection already exists")

        # 5. Guardar en ambas estructuras
        self.connection_pairs.add(pair)
        self.connections.append(connection)

    def add_hub(self, hub: Hub) -> None:
        # primero vemos si el hub o su nombre por lo menos esta repetido

        if hub.name in self.hubs:
            raise ValueError("The hub is already exists")
        elif (hub.x, hub.y) in self.coordenates:
            raise ValueError("The coordenates already exist")
        elif isinstance(hub, StartHub):
            if self.start_hub is None:
                self.start_hub = hub
            else:
                raise ValueError("A start_hub already exists")     
        elif isinstance(hub, EndHub):
            if self.end_hub is None:
                self.end_hub = hub
            else:
                raise ValueError("A end_hub already exists")

        self.hubs[hub.name] = hub
        self.coordenates.add((hub.x, hub.y))

    def validate_graph(self) -> None:
        if self.start_hub is None:
            raise ValueError("Graph validation failed: Missing StartHub.")
        if self.end_hub is None:
            raise ValueError("Graph validation failed: Missing EndHub.")
        if len(self.connection_pairs) == 0:
            raise ValueError("Graph validation falied. Missing connections")