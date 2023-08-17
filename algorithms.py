import copy
import time

class SokobanSolver:
    class TreeNode:
        def __init__(self, state, parent=None, action=None, depth=0):  # Add depth parameter with default value
            self.state = state
            self.parent = parent
            self.action = action
            self.depth = depth  # Store the depth of the node

    def __init__(self, initial_sokoban):
        self.initial_node = self.TreeNode(initial_sokoban)

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

    def _dls(self, max_depth, node_counter):
        def recursive_dls(node, depth, node_counter):
            if depth > max_depth:
                return None, node_counter
            if self._goal_test(node.state):
                return node, node_counter
            if depth == 0:
                return 'cutoff', node_counter
            for action in self._actions_fn(node.state):
                new_state = self._apply_action(node.state, action)
                child, node_counter = recursive_dls(self.TreeNode(new_state, node, action), depth - 1, node_counter)
                if child == 'cutoff':
                    return 'cutoff', node_counter
                elif child is not None:
                    return child, node_counter
            return None, node_counter
        return recursive_dls(self.initial_node, max_depth, node_counter)

    def _iddfs(self, max_depth):
        node_counter = 0
        for depth in range(max_depth + 1):
            result, node_counter = self._dls(depth, node_counter)
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

    def _goal_test(self, state):
        return state.level_complete()

    def _actions_fn(self, state):
        return state.get_valid_directions()

    def _apply_action(self, state, action):
        new_state = copy.deepcopy(state)
        new_state.move_player(action)
        return new_state

    def _manhattan_distance(self, box, goal):
        (x, y) = box
        (a, b) = goal
        return abs(a - x) + abs(b - y)

    def _heuristic_manhattan(self, state):
        total_distance = 0
        for box in state.get_boxes():
            min_distance = min([self._manhattan_distance(box, goal) for goal in state.get_goals()])
            total_distance += min_distance
        return total_distance

    def play_sokoban_with_algorithm(self, algorithm_name, heuristic_name, max_depth):
        start_time = time.time()
        result = None
        node_counter = 0
        # Choose the algorithm to use
        if (algorithm_name in ["bfs", "dfs", "iddfs", "a_star"] and heuristic_name in ["manhattan"]):
            raise ValueError("Invalid algorithm or heuristic name")
        elif algorithm_name == "bfs":
            result, node_counter = self._bfs()
        elif algorithm_name == "dfs":
            result = self._dfs()
        elif algorithm_name == "iddfs":
            result, node_counter = self._iddfs(max_depth)
        elif algorithm_name == "a_star":
            heuristic_func = self._heuristic_manhattan
            result, node_counter = self._a_star(heuristic_func)

        end_time = time.time()
        execution_time = end_time - start_time

        # Process the result
        if result:
            print("Solution found:")
            print(f"Nodes visited: {node_counter}")
        else:
            print("No solution found")
        print(f"In {execution_time}s")
