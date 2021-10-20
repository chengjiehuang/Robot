#!/usr/bin/env python3

from typing import Optional, Tuple
from abc import abstractmethod


class Robot:

    def __init__(self, table_size: Tuple[int, int]):
        self._table_width, self._table_height = table_size

    @abstractmethod
    def place(self, x, y, dir_str):
        ...

    @abstractmethod
    def left(self):
        ...

    @abstractmethod
    def right(self):
        ...

    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def report(self):
        ...


class RobotImpl(Robot):

    _directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    _directions_strs = ('NORTH', 'EAST', 'SOUTH', 'WEST')

    def __init__(self, table_size):
        super().__init__(table_size)

        self._pos: Optional[Tuple[int, int]] = None
        self._dir: Optional[int] = None

    def place(self, x, y, dir_str):
        try:
            next_pos = int(x), int(y)
            if not self._valid_position(next_pos):
                # Ignore the command. 
                #print(f'Error: Position {next_pos} is not on the table. Stop placing.')
                return

            next_dir = RobotImpl._directions_strs.index(dir_str)
        except ValueError:
            # Ignore the command. 
            #print(f'Error: Position: {x, y} or Direction: {dir_str} is not valid. Stop Placing.')
            return

        # No problems found. Place!
        self._pos = next_pos
        self._dir = next_dir

    def left(self):
        if self._dir is None:
            return
        self._dir -= 1
        self._dir %= 4

    def right(self):
        if self._dir is None:
            return
        self._dir += 1
        self._dir %= 4

    def move(self):
        if self._dir is None or self._pos is None:
            # Ignore the command. 
            #print('Error: Robot is not on the table. Stop.')
            return

        next_pos = self._next_position()
        if self._valid_position(next_pos):
            self._pos = next_pos
        else:
            # Ignore the command. 
            #print('Error: Invalid Move! Stop.')
            pass

    def report(self):
        if self._pos is not None and self._dir is not None:
            print(f'{self._pos[0]},{self._pos[1]},{RobotImpl._directions_strs[self._dir]}')
        else:
            # Ignore the command. 
            #print('Warn: Robot is not on the table.')
            pass

    def _next_position(self) -> Optional[Tuple[int, int]]:
        if self._dir is not None and self._pos is not None:
            return RobotImpl._directions[self._dir][0] + self._pos[0], \
                   RobotImpl._directions[self._dir][1] + self._pos[1]
        return None

    def _valid_position(self, pos) -> bool:
        return pos is not None and (0 <= pos[0] <= self._table_width - 1) and\
               (0 <= pos[1] <= self._table_height - 1)


class RobotFactory:

    @staticmethod
    def create_robot(table_size: Tuple[int, int]) -> Robot:
        return RobotImpl(table_size)


def run_robot(input_file):
    cmds = [line.strip() for line in open(input_file, 'r').readlines()]

    robot = RobotFactory.create_robot(table_size=(5, 5))
    for cmd in cmds:
        tokens = cmd.split(' ', 2)

        method_name = tokens[0].lower()
        method_params = [] if len(tokens) == 1 else [p.strip() for p in tokens[1].split(',')]

        getattr(robot, method_name)(*method_params)


if __name__ == '__main__':
    import sys
    import pathlib
    run_robot(pathlib.Path(sys.argv[1]))
