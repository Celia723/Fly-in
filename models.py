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


class Drone():
    def __init__(self, id: int, route: list[str]):
        self.id = id
        self.route = route
        self.current_step = 0
        self.wait_time = 0

    @property
    def current_position(self):
        return self.route[self.current_step]
    
    @property
    def has_finished(self) -> bool:
        return self.current_step == len(self.route) - 1

    @property
    def next_position(self) -> str:
        if self.has_finished:
            return None
        return self.route[self.current_step + 1]

    def move(self):
        if self.has_finished:
            return None
        self.current_step += 1


class Simulator():
    def __init__(self, grapho: Grapho, routes: list[list], num_drones: int):
        self.grapho: Grapho = grapho
        self.drones: list[Drone] = []
        self.num_drones: int = num_drones
        self.routes: list[list] = routes
        self.turn: int = 0

    def create_drones(self):
        for i in range(self.num_drones):
            self.drones.append(Drone(i))
        
    def run(self):
        #   hago una lista de todos los drones acivos y las ordeno de mayor a menor
        active_drones: list[(int, Drone)] = []
        for d in self.drones:
            if d.current_step > 0:
                active_drones.append((d.current_step, d))
        #   ordenamos
        active_drones_sort = sorted(active_drones)[::-1]
        
        #   cojo los activos y ahora hago q avancen en su ruta
        #   para eso veo si estan esperando o no, veo si el siguiente tiene espacio y si es asi vemos de q tipo es
                
        for da in active_drones_sort:
            active_drone: Drone = da[1]
            if active_drone.wait_time > 0:
                active_drone.wait_time -= 1
                continue
            else:
                nxt_hub = self.grapho.hubs[active_drone.next_position]
                #ahora q sabes cua es el grapho siguiente tienes q ver si tienes suficente  espacio para entrar y si
                # restricted o no, para q este dntro y le pongas tiempo de espera

