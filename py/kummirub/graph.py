
from __future__ import annotations

from copy import deepcopy
from enum import Enum, auto
from itertools import combinations
from tempfile import TemporaryFile
from typing import Optional, NamedTuple, Iterable

from networkx import read_adjlist

from kummirub.tiles import Tile


class EdgeType(Enum):

    AFTER_RUN = auto()
    BEFORE_RUN = auto()
    RUN = auto()
    BLOCK = auto()
    UNUSED = auto()

class Edge(NamedTuple):

    type: EdgeType
    adjacencies: Iterable[Tile]


class Graphs:

    def __init__(self, *tiles: Tile, prev: Optional[Graph] = None):
        self.__adjacencies = deepcopy(prev.__adjacencies) if prev else {}
        for tile in tiles:
            self.__add(tile)

    def __add(self, new_tile: Tile):
        self.__adjacencies[new_tile] = []
        blocks = [tile for tile in self.__adjacencies if tile.possible_block(new_tile)]
        self.__add_blocks(new_tile, blocks)
        befores = [tile for tile in self.__adjacencies if tile.possible_before(new_tile)]
        afters = [tile for tile in self.__adjacencies if tile.possible_after(new_tile)]
        self.__add_runs(new_tile, befores, afters)
        self.__add_unused(new_tile)

    def __add_blocks(self, new_tile, blocks):
        all_tiles = set(blocks)
        for tile in all_tiles:
            # drop blocks because we are going to set them all again below
            self.__adjacencies[tile] = [edge for edge in self.__adjacencies[tile] if edge.type != EdgeType.BLOCK]
        all_tiles.add(new_tile)
        for n in 3, 4:  # only valid sized blocks are allowed
            for tiles in combinations(all_tiles, n):
                for tile in tiles:
                    self.__adjacencies[tile].append(Edge(type=EdgeType.BLOCK,
                                                         adjacencies=[other for other in tiles if other != tile]))

    def __add_runs(self, new_tile, befores, afters):
        for before in befores:
            # link from new_tile back towards before (before-new)
            self.__adjacencies[new_tile].append(Edge(type=EdgeType.BEFORE_RUN, adjacencies=[before]))
            # we also need to fill in before to link forwards to new_tile
            self.__adjacencies[before].append(Edge(type=EdgeType.AFTER_RUN, adjacencies=[new_tile]))
            # and include the possible incoming runs to before (before-before-new)
            before_befores = [before_before.adjacencies[0] for before_before in self.__adjacencies[before]
                              if before_before.type == EdgeType.BEFORE_RUN]
            for before_before in before_befores:
                self.__adjacencies[before].append(Edge(type=EdgeType.RUN, adjacencies=[before_before, new_tile]))
            # it's simplest to also do the before-new-after runs here (although new-after is below)
            for after in afters:
                self.__adjacencies[new_tile].append(Edge(type=EdgeType.RUN, adjacencies=[before, after]))
        for after in afters:
            # the new-after edges
            self.__adjacencies[new_tile].append(Edge(type=EdgeType.AFTER_RUN, adjacencies=[after]))
            # and fill in from that node
            self.__adjacencies[after].append(Edge(type=EdgeType.BEFORE_RUN, adjacencies=[new_tile]))
            # and these are the outgoing runs new-after-after
            after_afters = [after_after.adjacencies[0] for after_after in self.__adjacencies[after]
                            if after_after.type == EdgeType.AFTER_RUN]
            for after_after in after_afters:
                self.__adjacencies[after].append(Edge(type=EdgeType.RUN, adjacencies=[after_after, new_tile]))

    def __add_unused(self, new_tile):
        self.__adjacencies[new_tile].append(Edge(type=EdgeType.UNUSED, adjacencies=[]))

    def take(self, n, bag):
        graphs = Graphs(prev=self)
        for _ in range(n):
            tile, bag = bag.draw()
            graphs.__add(tile)
        return graphs, bag

    def to_nx_0(self):
        with TemporaryFile(mode='wb+') as file:
            self._write_adjacencies_0(file)
            file.flush()
            file.seek(0)
            return read_adjlist(file)

    def _write_adjacencies_0(self, file):
        for key, adjacencies in self.__adjacencies.items():
            file.write(str(key).encode('utf'))
            for adjacency in adjacencies[0].adjacencies:
                file.write(' '.encode('utf'))
                file.write(str(adjacency).encode('utf'))
            file.write('\n'.encode('utf'))

