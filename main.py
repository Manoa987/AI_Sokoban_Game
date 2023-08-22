from algorithms import SokobanSolver
from sokoban import Sokoban

def main():
    
    # Create an instance of the Sokoban class with the desired level and levels file
    level = 55
    levels_file = "levels.txt"
    initial_sokoban = Sokoban(level, levels_file)

    # Specify the algorithm name and maximum depth (for IDDFS)
    algorithm_name = "a_star"  # Choose the algorithm: "bfs", "dfs", "greedy", "a_star", "iddfs"
    heuristic_name = "combined" # Choose the algorithm: "manhattan_boxes", "manhattan_player", "freedom_degrees", "combined", "grid"
    max_depth = 4000  # Set the maximum depth for IDDFS (ignored for other algorithms)

    sokobanSolver = SokobanSolver(initial_sokoban)
    # Use the specified algorithm to play Sokoban
    sokobanSolver.play_sokoban_with_algorithm(algorithm_name, heuristic_name, max_depth)
    
# Main entry point
if __name__ == "__main__":
    main()