
from __future__ import annotations

from tempfile import TemporaryFile
from typing import Optional

from networkx import read_adjlist

from kummirub.tiles import Tile


class Graph:

    def __init__(self, *tiles: Tile, prev: Optional[Graph] = None):
        self.__adjacencies = dict(prev.__adjacencies) if prev else {}
        for tile in tiles:
            self.__add(tile)

    def __add(self, new_tile: Tile):
        new_neighbours = set()
        for old_tile in self.__adjacencies:
            if new_tile.possible_run(old_tile) or new_tile.possible_block(old_tile):
                old_neighbours = set(self.__adjacencies[old_tile]) if self.__adjacencies[old_tile] else set()
                old_neighbours.add(new_tile)
                self.__adjacencies[old_tile] = frozenset(old_neighbours)
                new_neighbours.add(old_tile)
        self.__adjacencies[new_tile] = frozenset(new_neighbours)

    def take(self, n, bag):
        graph = Graph(prev=self)
        for _ in range(n):
            tile, bag = bag.draw()
            graph.__add(tile)
        return graph, bag

    def to_nx(self):
        with TemporaryFile(mode='wb+') as file:
            self.write_adjacencies(file)
            file.flush()
            file.seek(0)
            return read_adjlist(file)

    def write_adjacencies(self, file):
        for key, adjacencies in self.__adjacencies.items():
            file.write(str(key).encode('utf'))
            for adjacency in adjacencies:
                file.write(' '.encode('utf'))
                file.write(str(adjacency).encode('utf'))
            file.write('\n'.encode('utf'))
