from algorithms import SokobanSolver
from sokoban import Sokoban


def main():
    # Create an instance of the Sokoban class with the desired level and levels file
    level = 53
    levels_file = "levels.txt"
    algorithms = ["bfs", "global_greedy", "a_star"]
    heuristics = ["manhattan_boxes", "manhattan_player", "combined", "grid"]
    initial_sokoban = Sokoban(level, levels_file)

    # Specify the algorithm name and maximum depth (for IDDFS)
    algorithm_name = "a_star"  # Choose the algorithm: "bfs", "dfs", "greedy", "a_star", "iddfs"
    heuristic_name = "grid"  # Choose the algorithm: "manhattan_boxes", "manhattan_player", "freedom_degrees", "combined", "grid"
    max_depth = 4000  # Set the maximum depth for IDDFS (ignored for other algorithms)

    sokobanSolver = SokobanSolver(initial_sokoban)

    #sokobanSolver.play_sokoban_with_algorithm(algorithm_name, heuristic_name, max_depth)

    for algorithm in algorithms:
        if algorithm != "bfs":
            for heuristic in heuristics:
                sokobanSolver.play_sokoban_with_algorithm(algorithm, heuristic, max_depth)
        else:
            sokobanSolver.play_sokoban_with_algorithm(algorithm, heuristic_name, max_depth)

    # Use the specified algorithm to play Sokoban



# Main entry point
if __name__ == "__main__":
    main()
