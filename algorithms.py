import copy
import time
import sys

class SokobanSolver:
    class TreeNode:
        def __init__(self, state, parent=None, action=None, depth=0):  # Add depth parameter with default value
            self.state = state
            self.parent = parent
            self.action = action
            self.depth = depth  # Store the depth of the node

    def _grid_notation(self, state):
        matrix = []
        for j, row in enumerate(state.get_level_state()):
            new_row = []
            for i, elem in enumerate(row):
                if elem == state.Icons.WALL or (
                        (state.get_cell_content(i,j-1)==state.Icons.WALL and state.get_cell_content(i-1,j)==state.Icons.WALL) or
                        (state.get_cell_content(i,j-1)==state.Icons.WALL and state.get_cell_content(i+1,j)==state.Icons.WALL) or
                        (state.get_cell_content(i,j+1)==state.Icons.WALL and state.get_cell_content(i-1,j)==state.Icons.WALL) or
                        (state.get_cell_content(i,j+1)==state.Icons.WALL and state.get_cell_content(i+1,j)==state.Icons.WALL)
                    ):
                        new_row.append(sys.maxsize)
                else:
                    value = min([self._manhattan_distance((i,j), goal) for goal in state.get_goals()])
                    new_row.append(value)
            matrix.append(new_row)
        return matrix
    
    def __init__(self, initial_sokoban):
        self.initial_node = self.TreeNode(initial_sokoban)
        self.grid = self._grid_notation(self.initial_node.state)

    def _bfs(self):
        frontier = [self.initial_node]
        node_counter = 0

        while frontier:
            node = frontier.pop(0)
            node_counter += 1

            if self._goal_test(node.state):
                return node, node_counter

            for action in self._actions_fn(node.state):
                new_state = self._apply_action(node.state, action)
                frontier.append(self.TreeNode(new_state, node, action))

        return None, node_counter

    def _dfs(self):
        frontier = [self.initial_node]
        node_counter = 0  # Initialize the counter

        while frontier:
            node = frontier.pop()
            node_counter += 1  # Increment the counter for each explored node

            if self._goal_test(node.state):
                return node, node_counter

            for action in self._actions_fn(node.state):
                new_state = self._apply_action(node.state, action)
                frontier.append(self.TreeNode(new_state, node, action))
        return None , node_counter# If goal not found

    def _dls(self, node, depth, max_depth, node_counter):
        if depth > max_depth:
            return None, node_counter
        if self._goal_test(node.state):
            return node, node_counter
        if depth == 0:
            return 'cutoff', node_counter
        for action in self._actions_fn(node.state):
            new_state = self._apply_action(node.state, action)
            child, node_counter = self._dls(self.TreeNode(new_state, node, action), depth - 1, max_depth, node_counter)
            if child == 'cutoff':
                return 'cutoff', node_counter
            elif child is not None:
                return child, node_counter
        return None, node_counter

    def _iddfs(self, max_depth):
        node_counter = 0
        for depth in range(max_depth + 1):
            result, node_counter = self._dls(self.initial_node, depth, max_depth, node_counter)
            if result != 'cutoff':
                return result, node_counter
        return None, node_counter

    def _a_star(self, heuristic_fn):
        def f(node):
            return node.depth + heuristic_fn(node.state)
        frontier = [self.initial_node]
        node_counter = 0

        while frontier:
            node = min(frontier, key=f)
            frontier.remove(node)
            node_counter += 1

            if self._goal_test(node.state):
                return node, node_counter

            for action in self._actions_fn(node.state):
                new_state = self._apply_action(node.state, action)
                new_node = self.TreeNode(new_state, node, action)
                new_node.depth = node.depth + 1
                frontier.append(new_node)

        return None, node_counter
    
    def _greedy(self, heuristic_func):
        def f(node):
            return heuristic_func(node.state)

        frontier = [self.initial_node]
        node_counter = 0  # Initialize node counter

        while frontier:
            node = min(frontier, key=f)
            frontier.remove(node)
            node_counter += 1  # Increment node counter

            if self._goal_test(node.state):
                return node, node_counter  # Return the node object and node counter

            for action in self._actions_fn(node.state):
                new_state = self._apply_action(node.state, action)
                new_node = self.TreeNode(new_state, node, action)
                frontier.append(new_node)

        return None, node_counter  # Return None and node counter if no solution is found

    def _goal_test(self, state):
        return state.level_complete()

    def _actions_fn(self, state):
        return state.get_valid_directions()

    def _apply_action(self, state, action):
        new_state = copy.deepcopy(state)
        new_state.move_player(action)
        return new_state

    def _manhattan_distance(self, elem, goal):
        (x, y) = elem
        (a, b) = goal
        return abs(a - x) + abs(b - y)

    def _heuristic_manhattan_boxes(self, state):
        total_distance = 0
        for box in state.get_boxes():
            min_distance = min([self._manhattan_distance(box, goal) for goal in state.get_goals()])
            total_distance += min_distance
        return total_distance
    
    def _heuristic_manhattan_player(self, state):
        x,y, _ = state.get_player()
        min_distance = min([self._manhattan_distance((x,y), box) for box in state.get_boxes()])
        return min_distance
    
    def _heuristic_freedom_degrees(self, state):
        nb_freedom_degrees = 0
        for box in state.get_boxes():
            nb_freedom_degrees += 4
            x,y = box
            if state.get_cell_content(x+1,y) not in [state.Icons.BOX, state.Icons.WALL]: nb_freedom_degrees -= 1
            if state.get_cell_content(x,y+1) not in [state.Icons.BOX, state.Icons.WALL]: nb_freedom_degrees -= 1
            if state.get_cell_content(x-1,y) not in [state.Icons.BOX, state.Icons.WALL]: nb_freedom_degrees -= 1
            if state.get_cell_content(x,y-1) not in [state.Icons.BOX, state.Icons.WALL]: nb_freedom_degrees -= 1
        return (nb_freedom_degrees/len(state.get_boxes()))/4
    
    def _combined_heuristics(self, state):
        manhattan_boxes = self._heuristic_manhattan_boxes(state)
        manhattan_player = self._heuristic_manhattan_player(state)
        freedom_degrees = self._heuristic_freedom_degrees(state)
        return manhattan_boxes + manhattan_player + freedom_degrees
    
    def _grid_heuristic(self, state):
        val = 0
        for j,i in state.get_boxes():
            val += self.grid[i][j]
        return val
             
    def play_sokoban_with_algorithm(self, algorithm_name, heuristic_name, max_depth):
        start_time = time.time()
        result = None
        node_counter = 0

        # Choose the heuristic to use
        if (heuristic_name not in ["manhattan_boxes", "manhattan_player", "freedom_degrees", "combined", "grid"]):
            raise ValueError("Invalid heuristic name")
        elif heuristic_name == "manhattan_boxes":
            heuristic_func = self._heuristic_manhattan_boxes
        elif heuristic_name == "manhattan_player":
            heuristic_func = self._heuristic_manhattan_player
        elif heuristic_name == "freedom_degrees":
            heuristic_func = self._heuristic_freedom_degrees
        elif heuristic_name == "combined":
            heuristic_func = self._combined_heuristics
        elif heuristic_name == "grid":
            heuristic_func = self._grid_heuristic

        # Choose the algorithm to use
        if (algorithm_name not in ["bfs", "dfs", "iddfs", "greedy", "a_star"]):
            raise ValueError("Invalid algorithm name")
        elif algorithm_name == "bfs":
            result, node_counter = self._bfs()
        elif algorithm_name == "dfs":
            result = self._dfs()
        elif algorithm_name == "iddfs":
            result, node_counter = self._iddfs(max_depth)
        elif algorithm_name == "greedy":
            heuristic_func = self._combined_heuristics
            result, node_counter = self._greedy(heuristic_func)
        elif algorithm_name == "a_star":
            heuristic_func = self._combined_heuristics
            result, node_counter = self._a_star(heuristic_func)
        print(f"Algorithm : {algorithm_name}")
        print(f"with heuristic : {heuristic_name}")
        end_time = time.time()
        execution_time = end_time - start_time

        # Process the result
        if result:
            print("Solution found:")
            print(f"Nodes visited: {node_counter}")
        else:
            print("No solution found")
        print(f"In {execution_time}s")
