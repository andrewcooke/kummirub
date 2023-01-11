
from __future__ import annotations

from collections import defaultdict
from enum import Enum, auto
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
            self._write_adjacencies(file)
            file.flush()
            file.seek(0)
            return read_adjlist(file)

    def _write_adjacencies(self, file):
        for key, adjacencies in self.__adjacencies.items():
            file.write(str(key).encode('utf'))
            for adjacency in adjacencies:
                file.write(' '.encode('utf'))
                file.write(str(adjacency).encode('utf'))
            file.write('\n'.encode('utf'))

    def __iter__(self):
        """iterate over all tiles"""
        yield from self.__adjacencies


class PatchType(Enum):

    RUN = auto()
    NUMBER = auto()


class Patchwork:

    def __init__(self):
        self.__tiles_to_patches = {}
        self.__patch_to_tiles = defaultdict(set)

    def new_patch(self, tile):
        self.add_tile(len(self.__patch_to_tiles), tile)
        return self.__tiles_to_patches[tile]

    def add_tile(self, color, tile):
        self.__tiles_to_patches[tile] = color
        self.__patch_to_tiles[color].add(tile)

    def is_patched(self, tile):
        return tile in self.__tiles_to_patches

    def patch_type(self, tile):
        patch = list(self.__tiles_to_patches[tile])
        if len(patch) < 2:
            raise Exception('ambiguous patch (too small)')
        if patch[0].color == patch[1].color:
            return PatchType.RUN
        else:
            return PatchType.NUMBER


class Patcher:

    def __init__(self, graph: Graph, patchwork: Patchwork):
        self.__graph = graph
        self.__original_patchwork = patchwork

    def new_patchwork(self):
        for tile in filter(lambda tile: not self.__original_patchwork.is_patched(tile), self.__graph):
            print(f'uncolored: {tile}')
