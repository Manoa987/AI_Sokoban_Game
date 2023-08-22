## Sokoban Game
This repository contains a program that allows solving the Sokoban game using various search methods and heuristics.
# Content
The algorithms used in this repository are:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Greedy search
- A* search
- (Iterative Deepening Depth-First Search) - iddfs
For the greedy and A* algorithms, different heuristics are implemented. 
Some are admissible:
- Manhattan Boxes: The distances of the boxes to the nearest targets are summed, and the state with the lowest value is chosen.
- Manhattan Player: The distance between the player and the boxes is calculated, and the closest box is chosen.
- Grid: An attempt to enhance the efficiency of the Manhattan Boxes heuristic.
Some are not admissible:
- Freedom Degrees: For each box, the number of walls (or boxes) it will be touching (losing the ability to move) is considered, and the option with more freedom of movement is chosen.

# How to use
```bash
./python3 main.py
```