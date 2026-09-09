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

