import logging
import random

from typing import List, Any

from src.models import *
from src.helpers import viz_maze

logger = logging.getLogger(__name__)


class MazeGenerator:

    def __init__(self, dimension: int = 5):
        self.dimension = dimension
        self.maze = None
        self.entrance = None
        self.exit = None

    def initialise_maze(self):
        logger.warning("Initialise a maze ...")

        # initialise basic maze
        self.maze = self._init_empty_maze()
        self._init_entrance()
        self._init_exit()

        viz_maze(self.maze)
        self._init_boarder()
        self._init_branches()
        self._init_traps()
        self._init_treasures()
        self._init_wall()

        # visualise maze
        viz_maze(self.maze)

        logger.warning("Maze generated. ")

    # -- init methods --

    def _init_empty_maze(self) -> List[List[BaseTile]]:
        """ initialised a square maze with BaseTiles """
        return [
            [
                BaseTile(i, j) for i in range(self.dimension)
            ]
            for j in range(self.dimension)
        ]

    def _init_entrance(self) -> None:
        """ initialise the entrace at any point on the boarder """
        remains = self._get_remaining_border_tiles()
        chosen_tile = random.choice(remains)
        self.entrance = Entrance(self.dimension, x=chosen_tile.x, y=chosen_tile.y)
        self._replace_title(chosen_tile, self.entrance)

    def _init_exit(self):
        remains = self._get_remaining_border_tiles(excluding_neighbors=[self.entrance])
        chosen_tile = random.choice(remains)
        self.exit = Exit(self.dimension, x=chosen_tile.x, y=chosen_tile.y)
        self._replace_title(chosen_tile, self.exit)

    def _init_branches(self):
        pass

    def _init_traps(self):
        pass

    def _init_treasures(self):
        pass

    def _init_boarder(self):
        for base_tile in self._get_remaining_border_tiles():
            self._replace_title(base_tile, BoarderTile(base_tile.x, base_tile.y, self.dimension))

    def _init_wall(self):
        """
        generate walls after the completion of path
        including the boarders
        :return:
        """
        pass

    # -- helpers --

    def _get_remaining_tiles(self):
        """
        Compute remaining tiles as a list of tuples
        """
        result = []

        for i in range(self.dimension):
            for j in range(self.dimension):
                if isinstance(self.maze[i][j], BaseTile):
                    result.append((i, j))

        return result

    def _get_remaining_border_tiles(self, excluding_neighbors: List = None):
        """
        Compute remaining tiles as a list of tuples
        """
        result = []

        for i in range(self.dimension):
            for j in range(self.dimension):
                if not isinstance(self.maze[i][j], BaseTile):
                    continue

                if 0 not in (i, j) and self.dimension - 1 not in (i, j):
                    continue

                result.append(BaseTile(i, j))

        # excluding neighbors if required
        if excluding_neighbors is not None:
            final_result = []
            for tile in result:
                for exclusion in excluding_neighbors:
                    if not is_neighbor(tile, exclusion):
                        final_result.append(tile)

            result = final_result

        return result

    def _get_walkable_neightbors(self, current_tile: Any) -> List:
        # I am doing this stupid logic again ...
        all_dir = [
            self.maze[current_tile.x + 1][current_tile.y],
            self.maze[current_tile.x - 1][current_tile.y],
            self.maze[current_tile.x][current_tile.y - 1],
            self.maze[current_tile.x][current_tile.y + 1]
        ]
        result = []
        for tile in all_dir:
            if isinstance(tile, BaseTile):
                result.append(tile)

        return result

    def _replace_title(self, this: Any, other: Any):
        self.maze[this.x][this.y] = other


def random_walk(start, walk_before_turn: int):
    """
    Random Walk from a starting point, on all BaseTiles
    """
    pass


def generate_correct_path(start, end):
    """
    generate correct path between tiles, mark path as CorrectPathTile
    """
    pass


def generate_branches_from_coordinates(x, y, length: int):
    pass


def is_reachable(this: Any, other: Any, maze: List[List[Any]]) -> None:
    """
    Test in a give maze, the path is reachable from one place to another
    Note this ignoring any additional effect such as traps
    """
    pass


def is_neighbor(this: Any, other: Any) -> bool:
    if this is other:
        raise Exception("Not allowed to check neighbor for the same object")

    # Too lazy to google or think of algo
    neighbours_tiles_coor = [
        (this.x + 1, this.y),
        (this.x - 1, this.y),
        (this.x, this.y + 1),
        (this.x, this.y - 1)
    ]

    if (other.x, other.y) in neighbours_tiles_coor:
        return True

    return False

