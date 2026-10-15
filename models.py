from route_algorithm import choose_route


class Hub:
    def __init__(self, name: str, x: int, y: int, metadata: dict):
        self.name: str = name
        self.x: int = x
        self.y: int = y

        self.color: str | None = metadata.get("color", None)
        self.zone: str = metadata.get("zone", "normal")
        self.max_drones: int | float = int(metadata.get("max_drones", 1))


class StartHub(Hub):
    def __init__(self, name: str, x: int, y: int, metadata: dict):
        super().__init__(name, x, y, metadata)
        self.max_drones: float = float("inf")  # infinity capacity


class EndHub(Hub):
    def __init__(self, name: str, x: int, y: int, metadata: dict):
        super().__init__(name, x, y, metadata)
        self.max_drones: float = float("inf")  # inifinity cap


class Connection:
    def __init__(self, zone_a: str, zone_b: str, metadata: dict):
        self.zone_a: str = zone_a
        self.zone_b: str = zone_b
        self.max_link_capacity: int = int(metadata.get("max_link_capacity", 1))


class Grapho:
    def __init__(self, nb_drones: int):
        self.nb_drones = nb_drones

        self.hubs: dict[str, Hub] = {}
        self.coordinates: set[tuple[int, int]] = set()

        self.connections: list[Connection] = []
        self.connection_pairs: set[tuple[str, str]] = set()

        self.start_hub: StartHub | None = None
        self.end_hub: EndHub | None = None

        self.neighbors: dict[str, list[str]] = {}

    def add_connection(self, connection: Connection) -> None:

        if connection.zone_a == connection.zone_b:
            raise ValueError("A connection cannot link a hub to itself")

        if (
            connection.zone_a not in self.hubs
            or connection.zone_b not in self.hubs
        ):
            raise ValueError("Connection requires hubs that do not exist")

        if connection.zone_a > connection.zone_b:
            connection.zone_a, connection.zone_b = (
                connection.zone_b,
                connection.zone_a,
            )

        pair = (connection.zone_a, connection.zone_b)
        if pair in self.connection_pairs:
            raise ValueError("The connection already exists")

        self.connection_pairs.add(pair)
        self.connections.append(connection)

    def add_hub(self, hub: Hub) -> None:
        if hub.name in self.hubs.keys():
            raise ValueError(f"The hub: {hub.name} already exists")
        elif (hub.x, hub.y) in self.coordinates:
            raise ValueError("The coordinates already exist")
        elif isinstance(hub, StartHub):
            if self.start_hub is None:
                self.start_hub = hub
            else:
                raise ValueError("A start_hub already exists")
        elif isinstance(hub, EndHub):
            if self.end_hub is None:
                self.end_hub = hub
            else:
                raise ValueError("An end_hub already exists")

        self.hubs[hub.name] = hub
        self.coordinates.add((hub.x, hub.y))

    def validate_graph(self) -> None:
        if self.start_hub is None:
            raise ValueError("Graph validation failed: Missing StartHub.")
        if self.end_hub is None:
            raise ValueError("Graph validation failed: Missing EndHub.")
        if len(self.connection_pairs) == 0:
            raise ValueError("Graph validation failed: Missing connections.")
        connected_hubs = set()
        for pair in self.connection_pairs:
            a, b = pair
            connected_hubs.add(a)
            connected_hubs.add(b)

        for _, hub in self.hubs.items():
            if hub.name not in connected_hubs:
                raise ValueError(
                    f"Graph validation failed: Hub '{hub.name}'"
                      "has no connections.")

    def get_connection_object(self, h1: str, h2: str) -> Connection | None:
        """Devuelve el objeto Connection entre dos hubs."""
        for c in self.connections:
            if (
                (c.zone_a == h1 and c.zone_b == h2)
                or
                (c.zone_a == h2 and c.zone_b == h1)
            ):
                return c
        return None

    def get_connection_name(self, h1: str, h2: str) -> str:
        """Devuelve el nombre de la conexión (edge) entre dos hubs."""
        c = self.get_connection_object(h1, h2)
        if not c:
            return None
        return f"{c.zone_a}-{c.zone_b}" if c else ""


class Drone:
    def __init__(self, id: int, route: list[str] | None = None):
        self.id = id
        self.route = route
        self.current_step = 0
        self.wait_time = 0
        self.time_in_conexion = 0

    @property
    def current_position(self) -> str | None:
        if not self.route or self.current_step >= len(self.route):
            return None
        return self.route[self.current_step]

    @property
    def has_finished(self) -> bool:
        if not self.route:
            return False
        return self.current_step == len(self.route) - 1

    @property
    def next_position(self) -> str | None:
        if not self.route or self.has_finished:
            return None
        return self.route[self.current_step + 1]

    def move(self) -> None:
        if self.has_finished:
            return
        self.current_step += 1


class Simulator:
    def __init__(self, grapho: Grapho, routes: list[list], num_drones: int, capacity_info_enabled: bool):
        self.grapho: Grapho = grapho
        self.drones: list[Drone] = []
        self.num_drones: int = num_drones
        self.routes: list[list] = routes
        self.turn: int = 0
        self.capacity_info_enabled: bool = capacity_info_enabled

    def create_drones(self) -> None:
        for i in range(self.num_drones):
            self.drones.append(Drone(i + 1))

    def move_active_drones(self, turn_movements: list[str]) -> None:

        active_drones: list[tuple[int, Drone]] = []
        for d in self.drones:
            if d.current_step > 0 and not d.has_finished:
                active_drones.append((d.current_step, d))

        active_drones_sort = sorted(
            active_drones, key=lambda x: x[0], reverse=True)

        for da in active_drones_sort:

            active_drone: Drone = da[1]

            if active_drone.wait_time > 0:
                active_drone.wait_time -= 1
                continue

            current_position = active_drone.current_position
            next_position = active_drone.next_position
            if current_position is None or next_position is None:
                continue

            nxt_hub = self.grapho.hubs[next_position]
            drones_active_in_hub = sum(
                1 for _, d in active_drones_sort
                if d.current_position == nxt_hub.name
            )

            if nxt_hub.zone == "restricted":
                if active_drone.time_in_conexion == 1:
                    active_drone.time_in_conexion = 0
                    active_drone.move()
                    turn_movements.append(f"D{active_drone.id}-{nxt_hub.name}")
                    continue

                conn_obj = self.grapho.get_connection_object(
                    current_position, nxt_hub.name
                )
                if conn_obj is None:
                    continue
                conn_name = self.grapho.get_connection_name(
                    current_position, nxt_hub.name
                )
                drones_using_link = sum(
                    1 for m in turn_movements if conn_name in m)

                if (
                    drones_active_in_hub < nxt_hub.max_drones
                    and drones_using_link < conn_obj.max_link_capacity
                ):
                    active_drone.time_in_conexion = 1
                    active_drone.wait_time = 1
                    turn_movements.append(f"D{active_drone.id}-{conn_name}")

            else:
                if drones_active_in_hub < nxt_hub.max_drones:
                    turn_movements.append(f"D{active_drone.id}-{nxt_hub.name}")
                    active_drone.move()

    def spawn_new_drones(self, turn_movements: list[str]) -> None:
        desactive_drones: list[Drone] = [
            d for d in self.drones if d.current_step == 0
        ]

        while len(desactive_drones) > 0:
            drone = desactive_drones[0]
            active_drones = [
                        (d.current_step, d) for d in self.drones
                        if d.current_step > 0 and not d.has_finished
                    ]
            active_drones_sort = sorted(
                active_drones, key=lambda x: x[0], reverse=True)
            active_objects_drones_sort = [d for step, d in active_drones_sort]
            chosen_route = choose_route(
                self.routes, self.grapho, active_objects_drones_sort)

            if chosen_route is None:
                break
            drone = desactive_drones.pop(0)
            drone.route = chosen_route
            next_position = drone.next_position
            if next_position is None:
                continue
            nxt_hub = self.grapho.hubs[next_position]

            if nxt_hub.zone == "restricted":
                if drone.time_in_conexion == 0:
                    drone.time_in_conexion = 1
                    drone.wait_time = 1
                    conn_name = f"{drone.current_position}-{nxt_hub.name}"
                    turn_movements.append(f"D{drone.id}-{conn_name}")

                elif drone.time_in_conexion == 1:
                    drone.time_in_conexion = 0
                    drone.move()
                    turn_movements.append(f"D{drone.id}-{nxt_hub.name}")

            else:
                drone.move()
                turn_movements.append(f"D{drone.id}-{nxt_hub.name}")

    def run(self) -> None:
        while any(not d.has_finished for d in self.drones):
            self.turn += 1
            turn_movements: list[str] = []
            self.move_active_drones(turn_movements)
            self.spawn_new_drones(turn_movements)

            COLOR_MAP = {
                "red": "\033[91m",
                "green": "\033[92m",
                "blue": "\033[94m",
                "yellow": "\033[93m",
                "gray": "\033[90m",
                "cyan": "\033[36m",
                "magenta": "\033[35m",
                "purple": "\033[35m",
                "black": "\033[30m",
                "brown": "\033[38;5;130m",
                "orange": "\033[38;5;208m",
                "maroon": "\033[38;5;88m",
                "gold": "\033[38;5;220m",
                "darkred": "\033[38;5;52m",
                "crimson": "\033[38;5;161m",
                "rainbow": "\033[95m"
            }
            RESET_COLOR = "\033[0m"

            if turn_movements:
                colored_movements = []
                hubs_turno = []
                for m in turn_movements:
                    #   "D1-roof1" o "D2-tunnelB"
                    parts = m.split("-")
                    destination = parts[1] if len(parts) > 1 else ""
                    zone_color: str = "none"
                    if destination in self.grapho.hubs:
                        hub = self.grapho.hubs[destination]
                        hubs_turno.append(hub)
                        zone_color = hub.color or "none"
                    ansi_code = COLOR_MAP.get(zone_color.lower(), "")

                    if ansi_code:
                        colored_movements.append(
                            f"{ansi_code}{m}{RESET_COLOR}")
                    else:
                        colored_movements.append(m)

                  # 1. Imprimimos los movimientos del turno juntos
                print(" ".join(colored_movements))

                # 2. Si el flag --capacity-info está activo, imprimimos la extra
                if self.capacity_info_enabled:
                    extra_text = imprimir_extra(hubs_turno, self.grapho, self)
                    print(extra_text)


def imprimir_extra(hubs: list[Hub], graph: Grapho, simulator: Simulator) -> str:
    active_drones = [
        d for d in simulator.drones 
        if d.current_step > 0 and not d.has_finished
    ]
    
    parts = []
    for hub in hubs:
        drones_in_hub = sum(
            1 for d in active_drones if d.current_position == hub.name
        )
        max_cap = hub.max_drones
        parts.append(f"Zone {hub.name}: {drones_in_hub}/{max_cap} drones")

    return ", ".join(parts)


