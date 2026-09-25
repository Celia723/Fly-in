
def calculate_route_cost(route: list[str], graph: "Grapho", active_drones: list) -> float:
    cost = 0.0

    # 1. TIEMPO BASE (velocidad por tipo de zona)
    for hub in route[1:]:
        object_hub = graph.hubs[hub]

        if object_hub.zone == "blocked":
            return None  # Si hay un bloqueo, la ruta no sirve
        elif object_hub.zone == "normal":
            cost += 1.0
        elif object_hub.zone == "restricted":
            cost += 2.0
        elif object_hub.zone == "priority":
            cost += 0.5

    # 2. TRÁFICO Y ATASCOS (Hub a Hub)
    for hub in route[1:-1]:
        object_hub = graph.hubs[hub]
        
        # Contamos cuántos drones hay en este hub
        drones_in_hub = sum(1 for d in active_drones if d.current_position == object_hub.name)
        
        # ¿Hay atasco en este hub concreto?
        if drones_in_hub == object_hub.max_drones:
            return None
    
    # TRAFICO EN CONEXIONES
    for i in range(1, len(route)):
        current_hub = route[i]
        previous_hub = route[i - 1]
        
        # Buscas la conexión entre previous_hub y current_hub
        connection = graph.get_connection_object(previous_hub, current_hub)
        
        # Contamos cuántos drones están transitando esa conexión
        drones_in_connection = sum(
            1 for d in active_drones 
            if d.current_position == previous_hub and d.time_in_conexion == 1
        )
        
        if connection and drones_in_connection >= connection.max_link_capacity:
            return None  # Conexión colapsada


    return cost
        

#   con las rutas del path_finder  vamos a calcular su peso y decidir cual es el mejor  para cada situacion

def choose_route(routes: list[list], grapho: "Grapho", active_drones: list) -> list[str]:
    valid_routes = []

    for r in routes:
        cost = calculate_route_cost(r, grapho, active_drones)
        if cost == None:
            continue  #si el coust da NONE es pq tenia un prohibido. Saltamos a la siguiente sin añadirla
        valid_routes.append((cost, r))
    
    if not valid_routes:
        return None

    #vemos el numero mas pequeño
    costs_in_order = sorted(valid_routes)
    choosen_route = costs_in_order[[0][1]]

    return choose_route

    


    

    