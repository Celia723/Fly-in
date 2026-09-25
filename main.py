from parse import clean_text, parse_syntax
import models
from find_path import total_paths

if __name__ == "__main__":
    file_path = "maps/easy/02_simple_fork.txt"
    #   file_path = "maps/easy/01_linear_path.txt"
    #   file_path = "maps/easy/03_basic_capacity.txt"
    #   file_path = "maps/medium/01_dead_end_trap.txt"
    #   file_path = "maps/medium/02_circular_loop.txt"
    #   file_path = "maps/medium/03_priority_puzzle.txt"

    try:
        lines = clean_text(file_path)
        if lines:
            nb_drones, parsed_data = parse_syntax(lines)
            print(f" Drones detectados: {nb_drones}")
            print(f" Lineas validas procesadas: {len(lines)}")

            grapho = models.Grapho(nb_drones)

            # Leo la lista con los componentes y creo objetos
            for data in parsed_data:
                prefix = data[0]

                if prefix == "start_hub":
                    name, x, y = data[1]
                    element = models.StartHub(name, int(x), int(y), data[2])
                elif prefix == "end_hub":
                    name, x, y = data[1]
                    element = models.EndHub(name, int(x), int(y), data[2])
                elif prefix == "hub":
                    name, x, y = data[1]
                    element = models.Hub(name, int(x), int(y), data[2])
                elif prefix == "connection":
                    zone_a, zone_b = data[1]
                    element = models.Connection(zone_a, zone_b, data[2])
                # Ahora que tengo el objeto creado lo añado al grafo
                if prefix == "connection":
                    grapho.add_connection(element)
                elif prefix in ("start_hub", "end_hub", "hub"):
                    grapho.add_hub(element)
                
 
            # Última validación (start, end y hubs conectados)
            grapho.validate_graph()
            print("Graph validated successfully!\n")

            # Cálculo de rutas
            routes = total_paths(grapho)
            
            # Instancia e inicio de la simulación
            simulation = models.Simulator(grapho, routes, nb_drones)
            simulation.create_drones()
            simulation.run()

            print("La simulación ha finalizado")

    except ValueError as e:
        print(e)

