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
    def __init__(self, conecction_a: str, conecction_b: str, metadata: dict):
        self.conecction_a: str = conecction_a
        self.conecction_b: str = conecction_b

    self.max_link_capacity: int = int(metadata.get("max_link_capacity", 1))


class Grapho:
    def __init__(self, nb_drones:int):
        self.nb_drones = nb_drones

        self.hubs: dict[str, Hub] = {}
        self.coordenates: set[tuple[int, int]]= set()

        self.conecctions: list[Connection]= []

        self.start_hub: StartHub | None = None
        self.end_hub: EndHub | None = None
    
        def add_conecction(self, connection: Connection) -> None:
            #comprobamos q no sea una conexion con el mismo
            if connection.conecction_a == connection.conecction_b:
                    raise ValueError("One conecction can't be with a same hub")
            #primero veo si existen los hubs
            elif connection.conecction_a not in self.hubs or connection.conecction_b not in connected.conecction_b:
                raise ValueError("The connection requiers a hub that doesn't exist")
            else:
                #deues voy a hacer q siempre esten ordenados alfabeticamente de mayor  a menor 
                # para q siempre enten ordenados igual y ver mas facil si hay duplicados
                if connection.zone_a > connection.zone_b:
                connection.zone_a, connection.zone_b = (connection.zone_b, connection.zone_a)
                
                if (connection.conecction_a, connection.conecction_b) in self.conecctions:
                    raise ValueError("The conecction is repeat")
                
                self.append(connection)


        def add_hub(self, hub: Hub)-> None:
            #primero vemos si el hub o su nombre por lo menos esta repetido

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
                    sel.end_hub = hub
                    return
                else:
                    raise ValueError("A end_hub already exists")
            
            self.hubs.append[hub.name] = hub
            self.coordenates.add((hub.x, hub.y))


        