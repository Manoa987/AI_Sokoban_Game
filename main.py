from algorithms import SokobanSolver
from sokoban import Sokoban

def main():
    
    # Create an instance of the Sokoban class with the desired level and levels file
    level = 2
    levels_file = "levels.txt"
    initial_sokoban = Sokoban(level, levels_file)

    # Specify the algorithm name and maximum depth (for IDDFS)
    algorithm_name = "a_star"  # Choose the algorithm: "bfs", "dfs", "iddfs", "a_star"
    max_depth = 20  # Set the maximum depth for IDDFS (ignored for other algorithms)

    sokobanSolver = SokobanSolver(initial_sokoban)
    # Use the specified algorithm to play Sokoban
    sokobanSolver.play_sokoban_with_algorithm(algorithm_name, "", max_depth)
    
# Main entry point
if __name__ == "__main__":
    main()