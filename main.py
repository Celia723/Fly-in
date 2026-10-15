from parse import clean_text, parse_syntax
import models
from find_path import total_paths
import sys

"""import colorama
colorama.init()  # Esto activa los colores mágicamente en Windows
"""
if __name__ == "__main__":
    #   file_path = "maps/easy/01_linear_path.txt"
    file_path = "maps/easy/02_simple_fork.txt"
    #   file_path = "maps/easy/03_basic_capacity.txt"
    #   file_path = "maps/medium/01_dead_end_trap.txt"
    #   file_path = "maps/medium/02_circular_loop.txt"
    #   file_path = "maps/medium/03_priority_puzzle.txt"
    #   file_path = "maps/hard/01_maze_nightmare.txt"
    #   file_path = "maps/hard/02_capacity_hell.txt"
    #   file_path = "maps/hard/03_ultimate_challenge.txt"
    #   file_path = "maps/challenger/01_the_impossible_dream.txt"
    try:
        lines = clean_text(file_path)
        if lines:
            nb_drones, parsed_data = parse_syntax(lines)
            print(f" Drones detectados: {nb_drones}")
            print(f" Lineas validas procesadas: {len(lines)}")

            grapho = models.Grapho(nb_drones)

            for data in parsed_data:
                prefix = data[0]

                if prefix == "start_hub":
                    name, x, y = data[1]
                    grapho.add_hub(
                        models.StartHub(name, int(x), int(y), data[2])
                    )
                elif prefix == "end_hub":
                    name, x, y = data[1]
                    grapho.add_hub(
                        models.EndHub(name, int(x), int(y), data[2])
                    )
                elif prefix == "hub":
                    name, x, y = data[1]
                    grapho.add_hub(
                        models.Hub(name, int(x), int(y), data[2])
                    )
                elif prefix == "connection":
                    zone_a, zone_b = data[1]
                    grapho.add_connection(
                        models.Connection(zone_a, zone_b, data[2])
                    )

            grapho.validate_graph()
            print("Graph validated successfully!\n")

            routes = total_paths(grapho)

            # Comprobamos directamente si el flag está en los argumentos de la terminal
            capacity_info_enabled = "--capacity-info" in sys.argv

            simulation = models.Simulator(grapho, routes, nb_drones, capacity_info_enabled)
            simulation.create_drones()
            simulation.run()

            print("La simulación ha finalizado")

    except ValueError as e:
        print(e)
