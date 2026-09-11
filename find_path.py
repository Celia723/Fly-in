from models import Grapho, Hub


def calculate_neighbors(grapho: Grapho) -> dict[str, list]:
    hubs_and_neighbors: dict[str, list] = {}
    conecctions = grapho.connection_pairs

    for hub in grapho.hubs.values():
        neighbors = []
        for conn in conecctions:
            if hub.name in conn:
                x, y = conn
                if x == hub.name:
                    neighbors.append(y)
                else:
                    neighbors.append(x)

        hubs_and_neighbors[hub.name] = neighbors

    return hubs_and_neighbors


def path_finder(neighbors: dict[str, list], start_hub: str, end_hub: str) -> list [str]:
    """
    empezamos con start y vamso creando rutas : creamos listas nuevas con cada vecino, y cuando un hub tenga de vecino end, lo metemos en la lista
    y lo devolvemos
    """
    #   Caminos FINALES
    sorted_final_paths : list[list] = []
    #   1 generacion
    first_paths: list[list] = []
    #   2 generacion
    second_paths : list[list] = []
    # para q empiece empezamos con la lista de un solo hub (START)
    first_paths = [[start_hub]]
    

    while len(first_paths) != 0:
        #limpiamos la segunda ronda anterior
        second_paths : list[list] = []
        for lst in first_paths:
            last_hub = lst[-1]
            neighbors_names: list = neighbors[last_hub]
            for neighbor in neighbors_names:
                if neighbor in lst:
                    continue
                new_list = []
                new_list = lst.copy()
                new_list.append(neighbor)
                if neighbor == end_hub:
                    sorted_final_paths.append(new_list)
                    continue
                second_paths.append(new_list)
        
        first_paths = second_paths
        
    return sorted_final_paths

