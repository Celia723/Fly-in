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
    posibol_paths: list[list] = []
    # first_list = []
    # first_list.append(start_hub)
    # posibol_paths.append(first_list)
    posibol_paths = [[start_hub]]

    # key, values = neighbors.items()
    # while end_hub not in values:
    #     neighbors_names  = neighbors[]
    for lst in posibol_paths:
        last_hub = lst[:1]
        neighbors_names = neighbors[last_hub]
        for neighbor in neighbors_names:
            new_list = lst
            new_list.append(neighbor)
            if neighbor == end_hub:
                return new_list
            posibol_paths.append(new_list)
        posibol_paths.remove(lst)

