*This project has been created as part of the 42 curriculum by ceboyero.*
 
# Fly-in
 
## Description
 
**Fly-in** is a drone routing simulator written in Python 3.10+. Given a map describing a network of zones (hubs) linked by connections, the program moves a fleet of drones from the start zone to the end zone in as few simulation turns as possible, while respecting:
 
- Zone types: `normal` (1 turn), `restricted` (2 turns), `priority` (1 turn, preferred) and `blocked` (forbidden).
- Zone capacity (`max_drones`) and connection capacity (`max_link_capacity`).
- Simultaneous movement, strategic waiting, and conflict/deadlock avoidance.
Constraints of the project: fully object-oriented, fully type-safe (`flake8` + `mypy`), and **no graph library** (no `networkx`, `graphlib`, etc.).
 
## Instructions
 
### Requirements
 
- Python 3.10 or later
- `flake8` and `mypy` (for linting)
### Makefile rules
 
| Rule          | Description                                                   |
|---------------|---------------------------------------------------------------|
| `make install`| Installs the project dependencies                             |
| `make run`    | Runs the main script                                          |
| `make debug`  | Runs the main script with `pdb`                               |
| `make clean`  | Removes `__pycache__`, `.mypy_cache`, etc.                    |
| `make lint`   | Runs `flake8 .` and `mypy .` with the mandatory flags         |
| `make lint-strict` | Runs `flake8 .` and `mypy . --strict`                    |
 
### Execution
 
```bash
make install
make run
```
 
The map is currently selected in `main.py` through the `file_path` variable. Uncomment the map you want to run:
 
```python
file_path = "maps/easy/02_simple_fork.txt"
# file_path = "maps/medium/01_dead_end_trap.txt"
# file_path = "maps/hard/01_maze_nightmare.txt"
```
 
### Project structure
 
```
.
├── main.py             # Entry point: parsing -> graph -> routes -> simulation
├── parse.py            # Text cleaning and syntax parsing
├── models.py           # Hub, Connection, Grapho, Drone, Simulator
├── find_path.py        # Neighbour search and path enumeration
├── route_algorithm.py  # Route cost evaluation and route selection
├── maps/               # easy / medium / hard / challenger maps
├── Makefile
└── README.md
```
 
## Map format
 
```
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: corridorA-goal [max_link_capacity=2]
```
 
Comments start with `#`. Zone names cannot contain dashes or spaces. Invalid maps stop the program with an error message indicating the line and the cause.
 
## Algorithm and implementation strategy
 
### 1. Parsing (`parse.py`)
 
`clean_text` reads the file (using a context manager), removes comments and empty lines. `parse_syntax` validates every line (prefixes, integer coordinates, metadata syntax, valid zone types, positive capacities, unique names, no duplicated connections...) and returns the number of drones plus a list of parsed entries, one per line. Any error raises a `ValueError` with the line number and the reason.
 
### 2. Object model (`models.py`)
 
The parsed data is converted into objects:
 
- `Hub` (and its subclasses `StartHub` and `EndHub`): name, coordinates, zone type, color and capacity. Capacity is ignored in start and end hubs.
- `Connection`: the two zones it links and its `max_link_capacity`.
- `Grapho`: the whole map (hubs, coordinates, neighbours, connections, start and end). `validate_graph()` performs the last validation: start and end exist and every hub is connected.
- `Drone`: its ID, assigned route and current progress.
- `Simulator`: runs the simulation turn by turn.
### 3. Path enumeration (`find_path.py`)
 
`total_paths(grapho)` explores the neighbours of each hub (skipping `blocked` zones) and builds **all the possible routes** from the start hub to the end hub. These routes are computed **once**, before the simulation starts, and cached for the whole run.
 
### 4. Route selection (`route_algorithm.py`)
 
Every time a new drone is about to leave, `choose_route` evaluates the cost of every available route:
 
- The base cost is the route weight (movement costs by zone type; `priority` zones are favoured).
- A traffic penalty is added depending on the drones already using the hubs and connections of that route.
- If a hub or a connection on the route is saturated, the cost of that route is `None`: it is discarded, because it is impossible to know how many turns it will take to clear up.
The route with the lowest cost is assigned to the drone. If every route is discarded, the drone simply waits and the simulator tries again next turn.
 
### 5. Simulation (`Simulator.run`)
 
Each turn:
 
1. Drones that are already on the map advance along their route, as long as zone and connection capacities allow it (drones leaving a zone free its capacity during the same turn). Movements towards `restricted` zones take 2 turns and the drone cannot wait on the connection.
2. The simulator then tries to release new drones from the start hub, assigning each one a route with `choose_route`.
3. The turn is printed as one line with every movement (`D<ID>-<zone>` or `D<ID>-<connection>` for drones in flight). Drones that don't move are omitted.
The simulation ends when all drones have reached the end hub.
 
### Complexity and performance
 
- **Path enumeration**: Finding all paths can be complex in dense graphs, but it is computed once at startup to optimize execution.
- **Route choice**: Efficiently evaluates available paths based on current traffic and capacity constraints.
- **Simulation turn**: Iterates dynamically through the active drones ($D$) at each discrete turn until all are delivered.
- **Caching**: Paths are calculated once; traffic costs and zone occupancies are updated turn-by-turn.
### Benchmarks
 
> TODO: fill in with the turns obtained on each map.
 
| Map                      | Drones | Target | Obtained |
|--------------------------|--------|--------|----------|
| Linear path              | 2      | ≤ 6    |          |
| Simple fork              | 4      | ≤ 8    |          |
| Basic capacity           | 4      | ≤ 6    |          |
| Dead end trap            | 5      | ≤ 12   |          |
| Circular loop            | 6      | ≤ 15   |          |
| Priority puzzle          | 5      | ≤ 12   |          |
| Maze nightmare           | 8      | ≤ 30   |          |
| Capacity hell            | 12     | ≤ 35   |          |
| Ultimate challenge       | 15     | ≤ 45   |          |
| The Impossible Dream (*) | 25     | 45     |          |
 
(*) Optional challenger map.
 
## Visual representation

Our implementation supports both **dynamic colored terminal output** and **web-based visualization** to make the simulation intuitive and easy to follow:

- **ANSI Color Mapping**: Zone colors defined in the map configuration (such as `[color=red]`, `[color=blue]`, `[color=yellow]`, etc.) are automatically parsed and translated into terminal ANSI colors.
- **Turn-by-Turn Tracking**: Each simulation step prints active movements clearly (e.g., `D1-roof1 D2-junction`), letting you track drone flows and routes at a glance.
- **Default Fallback**: Zones without an explicit color (or set to `none`) default to standard terminal text without breaking output formatting.
- **Web Visualizer Integration**: The simulator can also interface with a web-based visualizer to provide a graphical, real-time view of the map, nodes, and traffic constraints.
- **Debugging & Analysis**: This dual visual approach helps quickly identify bottlenecks, traffic jams, and drone distribution during each turn.
## Example
 
### Input
 
```
nb_drones: 2
start_hub: start 0 0 [color=green]
end_hub: goal 2 0 [color=yellow]
hub: a 1 0 [color=blue]
connection: start-a
connection: a-goal
```
 
### Expected output
 
```
D1-a
D1-goal D2-a
D2-goal
```
 
The simulation ends in 3 turns: zone `a` has capacity 1, so the second drone has to wait one turn before leaving.
 
## Resources
 
### References
 
- Python documentation: https://docs.python.org/3/
- PEP 8, PEP 257 (style and docstrings): https://peps.python.org/
- mypy documentation: https://mypy.readthedocs.io/
- flake8 documentation: https://flake8.pycqa.org/
- Graph search (BFS / DFS / Dijkstra) and flow-based routing: articles and lecture notes of your choice.

    **Web Visualizer**: The graphical web viewer used for advanced simulation tracking is based on external community visualization tools / open-source resources: https://davidgarciasolis.github.io/visualizador-fly-in/
### Use of AI
 
AI was used for:

- Resolve coding and syntax doubts, serving as technical support during development.
- Help structure and organize the project's codebase.
- Draft and structure this README file.

All AI-generated content was reviewed, tested, and understood by the authors.
All AI-generated content was reviewed, tested and understood by the authors.
 