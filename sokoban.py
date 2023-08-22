import sys
from typing import Tuple
from enum import Enum
import copy

class Sokoban:
    class Icons(Enum):
        WALL = '#'
        FLOOR = ' '
        GOAL = '.'
        BOX = '$'
        BOX_ON_GOAL = '*'
        PLAYER = '@'
        PLAYER_ON_GOAL = '+'

    class Direction(Enum):
        LEFT = (-1, 0)
        RIGHT = (1, 0)
        UP = (0, -1)
        DOWN = (0, 1)
        NONE = (0, 0)

    def _is_valid_value(self, value):
        return value in [item.value for item in self.Icons]

    def get_valid_directions(self):
        valid_moves = []
        for direction in Sokoban.Direction:
            if (self._can_move(direction) or self._can_push(direction)) and direction != self.Direction.NONE:
                valid_moves.append(direction)
        return valid_moves
    
    def _init_player(self) -> Tuple[int, int, Icons]:
        for y, row in enumerate(self.level_state):
            for x, cell in enumerate(row):
                if cell == self.Icons.PLAYER or cell == self.Icons.PLAYER_ON_GOAL:
                    return (x, y, cell)
        raise RuntimeError("Player not found")

    def __init__(self, level: int, levels_file: str):
        self.level_state = []
        self.boxes = set()
        self.goals = set()
        self.player=(0,0,None)
        x=0
        y=0

        if level < 1:
            print("ERROR: Level " + str(level) + " does not exist")
            sys.exit(1)

        file = open(levels_file, "r")
        level_found = False
        line = file.readline()
        while line:
            if not level_found:
                if "Level " + str(level) == line.strip():
                    level_found = True
            else:
                if line.strip():
                    row = []
                    x = 0
                    for c in line:
                        # If end of line
                        if c == "\n":
                            y += 1
                            x = 0
                            continue
                        # If invalid character
                        if not self._is_valid_value(c): raise RuntimeError(f"ERROR: Level {level} has invalid value {c}")

                        row.append(self.Icons(c))
                        point = (x, y)
                        if c == '$':    # If is a box
                            self.boxes.add(point)
                        elif c == '.':    # If is a goal
                            self.goals.add(point)
                        elif c == '*':    # If is a box on a goal
                            self.boxes.add(point)
                            self.goals.add(point)
                        elif c == '+':    # If is a player on a goal
                            self.goals.add(point)
                        x += 1
                    self.level_state.append(row)
                else:
                    break
            line = file.readline()
        file.close()
        self.player = self._init_player()

    def get_level_state(self):
        return self.level_state
    
    def get_player(self):
        return self.player
    
    def get_boxes(self):
        return self.boxes
    
    def get_goals(self):
        return self.goals

    def _set_player(self, player):
        self.player = player
        
    def set_boxes(self, boxes):
        self.boxes = copy.deepcopy(boxes)
        
    def _set_goals(self, goals):
        self.goals = copy.deepcopy(goals)

    def print_level_state(self):
        for row in self.level_state:
            row_str = "".join([char.value for char in row])
            print(row_str, end="\n")

    def get_cell_content(self, x: int, y: int) -> Icons:
        if (x < 0 or y < 0 or y >= len(self.level_state) or x >= len(self.level_state[y])):
            return self.Icons.WALL
        return self.level_state[y][x]

    def _set_cell_content(self, x: int, y: int, content: Icons):
        if (x < 0 or y < 0 or y >= len(self.level_state) or x >= len(self.level_state[y])):
            raise RuntimeError("Cell is out of bounds")
        self.level_state[y][x] = content

    def level_complete(self) -> bool:
        for row in self.level_state:
            for cell in row:
                if cell == self.Icons.BOX:
                    return False
        return True

    # private
    def _move_box(self, x: int, y: int, x_diff: int, y_diff: int):
        box_cell = self.get_cell_content(x, y)

        if box_cell not in [self.Icons.BOX, self.Icons.BOX_ON_GOAL]:
            raise RuntimeError("Cell is not a box")

        target_cell = self.get_cell_content(x + x_diff, y + y_diff)

        if target_cell not in [self.Icons.FLOOR, self.Icons.GOAL]:
            raise RuntimeError("Cell is not a valid box target")

        new_box_cell = (self.Icons.FLOOR if box_cell == self.Icons.BOX else self.Icons.GOAL)
        new_target_cell = (self.Icons.BOX if target_cell == self.Icons.FLOOR else self.Icons.BOX_ON_GOAL)

        point = (x, y)
        new_point = (x + x_diff, y + y_diff)
        self.boxes.remove(point)
        self.boxes.add(new_point)
        self._set_cell_content(x, y, new_box_cell)
        self._set_cell_content(x + x_diff, y + y_diff, new_target_cell)

    def _can_move(self, direction: Direction) -> bool:
        player_x, player_y, _ = self.get_player()
        x_diff, y_diff = direction.value

        target_cell = self.get_cell_content(player_x + x_diff, player_y + y_diff)

        return target_cell not in [self.Icons.WALL, self.Icons.BOX, self.Icons.BOX_ON_GOAL]

    def _next(self, x: int, y: int) -> Icons:
        player_x, player_y, _ = self.get_player()
        return self.get_cell_content(player_x + x, player_y + y)

    def _can_push(self, dir: Direction) -> bool:
        (x, y) = dir.value

        player_is_adjacent_to_box = self._next(x, y) in [self.Icons.BOX, self.Icons.BOX_ON_GOAL]
        box_can_be_pushed = self._next(2 * x, 2 * y) in [self.Icons.FLOOR, self.Icons.GOAL]

        return player_is_adjacent_to_box and box_can_be_pushed

    def move_player(self, dir: Direction):
        (x, y) = dir.value
        if self._can_move(dir):
            player_x, player_y, player_cell = self.get_player()
            target_cell = self._next(x, y)

            new_player_cell = (self.Icons.FLOOR if player_cell == self.Icons.PLAYER else self.Icons.GOAL)

            new_target_cell = (self.Icons.PLAYER if target_cell == self.Icons.FLOOR else self.Icons.PLAYER_ON_GOAL)
            
            self._set_player((player_x + x, player_y + y, new_target_cell))
            self._set_cell_content(player_x, player_y, new_player_cell)
            self._set_cell_content(player_x + x, player_y + y, new_target_cell)

        elif self._can_push(dir):
            player_x, player_y, player_cell = self.get_player()
            target_cell = self._next(x, y)

            new_player_cell = (self.Icons.FLOOR if player_cell == self.Icons.PLAYER else self.Icons.GOAL)

            new_target_cell = (self.Icons.PLAYER if target_cell == self.Icons.BOX else self.Icons.PLAYER_ON_GOAL)

            self._move_box(player_x + x, player_y + y, x, y)
            self._set_player((player_x + x, player_y + y, new_target_cell))
            self._set_cell_content(player_x, player_y, new_player_cell)
            self._set_cell_content(player_x + x, player_y + y, new_target_cell)

# def game():
#     level = 52
#     levels_file = "levels.txt"
#     sokoban = Sokoban(level, levels_file)

#     while (not sokoban.level_complete()):
#         valid = False
#         dir = Sokoban.Direction.NONE
#         while (not valid):
#             sokoban.print_level_state()
#             key = input("zqsd:")
#             valid = True
#             if key == "z":
#                 dir = Sokoban.Direction.UP
#             elif key == "q":
#                 dir = Sokoban.Direction.LEFT
#             elif key == "s":
#                 dir = Sokoban.Direction.DOWN
#             elif key == "d":
#                 dir = Sokoban.Direction.RIGHT
#             else:
#                 valid = False
#             if (valid and sokoban._can_move(dir) or sokoban._can_push(dir)):
#                 sokoban.move_player(dir)
#     print("Level succeed")
    
# if __name__ == "__main__":
#     game()
