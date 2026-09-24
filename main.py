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
            print(f" Líneas válidas procesadas: {len(parsed_data)}")

            grapho = models.Grapho(nb_drones)

            #   leo la lista con los componentes y creo objetos
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

                #   Ahora q tengo el elemento objeto creado lo tengo q meter en grafo, me dara error si algo sale mal
                if prefix == "connection":
                    grapho.add_connection(element)
                elif prefix == "start_hub":
                    grafo.add_star_hub(element)
                elif prefix == "end_hub":
                    grafo.add_end_hub(element)
                else:
                    grapho.add_hub(element)
            #   ultima validacion (q haya start hub, end y q ningun hub quede suelto)
            grapho.validate_graph()
            print("Graph validated successfully!\n")

            #   ahora que tengo el mapa , tengo q tener las rutas
            routes = total_paths(grafo)
            
            #   ya lo tengo para crear la simulacion
            simulation = Simulator(grafo, routes, nb_drones)
            
            #   creo todos los drones
            simulation.create_drones()

            #   los voy lanzando (empiezo la simulacion)
            simulation.run()

            print("La simulacion ha finalizado")

    except ValueError as e:
        print(e)

