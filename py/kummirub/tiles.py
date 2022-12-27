
from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from functools import reduce
from random import choice, randint, shuffle
from typing import NamedTuple

# both count from 1
MAX_NUMBER = 13
MAX_GENERATION = 2
# number of jokers fixed at 2

# the 'value' for the jokers
JOKER = 'J'


class Color(Enum):

    RED = 'R'
    BLACK = 'K'
    YELLOW = 'Y'
    BLUE = 'B'

    @classmethod
    def random(cls):
        return choice(list(cls))

    def __str__(self):
        return self.value


class Tile(NamedTuple):

    color: Color
    value: int | str  # either the numerical value or 'J'
    generation: int

    @classmethod
    def random(cls):
        return Tile(Color.random(), randint(1, MAX_NUMBER), randint(1, MAX_GENERATION))

    def __str__(self):
        base = str(self.color) + str(self.value)
        if self.generation == 1:
            return base.upper()
        elif self.generation == 2:
            return base.lower()
        else:  # generally only support 2
            return base + '/' + str(self.generation)

    @classmethod
    def all(cls):
        yield Tile(Color.RED, JOKER, 1)
        yield Tile(Color.BLACK, JOKER, 1)
        for generation in range(1, MAX_GENERATION+1):
            for color in Color:
                for number in range(1, MAX_NUMBER + 1):
                    yield Tile(color, number, generation)

    def possible_run(self, tile):
        return self.value == JOKER or tile.value == JOKER or \
               (tile.color == self.color and abs(tile.value - self.value) == 1)

    def possible_block(self, tile):
        return self.value == JOKER or tile.value == JOKER or \
               (tile.color != self.color and tile.value == self.value)


class BagInterface:

    @abstractmethod
    def draw(self) -> (Tile, BagInterface):
        pass

    @abstractmethod
    def __len__(self):
        pass


class Bag(BagInterface):

    def __init__(self):
        nodes = list(Tile.all())
        shuffle(nodes)
        self.__node = reduce(BagNode, nodes, None)

    def draw(self) -> (Tile, BagInterface):
        return self.__node._tile, self.__node._bag

    def __len__(self):
        return len(self.__node)


class BagNode(BagInterface):

    def __init__(self, bag, tile):
        self._tile = tile
        self._bag = bag

    def draw(self) -> (Tile, BagInterface):
        return self._tile, self._bag

    def __len__(self):
        if self._bag is None:
            return 1
        else:
            return 1 + len(self._bag)


