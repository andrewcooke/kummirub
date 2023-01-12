
from __future__ import annotations

from collections import defaultdict
from enum import Enum, auto
from tempfile import TemporaryFile
from typing import Optional

from networkx import read_adjlist

from kummirub.tiles import Tile, JOKER


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

    def neighbouring_tiles(self, tile):
        yield from self.__adjacencies[tile]

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

    def __init__(self, previous: Optional[Patchwork] = None):
        self.__tiles_to_patches = dict(previous.__tiles_to_patches if previous else {})
        self.__patch_to_tiles = defaultdict(set, previous.__patch_to_tiles if previous else {})

    def is_patched(self, tile):
        return tile in self.__tiles_to_patches

    def patch(self, tile):
        return self.__tiles_to_patches[tile]

    def patch_type(self, tile):
        patch = self.patch(tile)
        non_jokers = [tile for tile in patch if tile.value != JOKER]
        if len(non_jokers) < 2 or non_jokers[0].color == non_jokers[1].color:
            yield PatchType.RUN, non_jokers
        if len(non_jokers) < 2 or non_jokers[0].color != non_jokers[1].color:
            yield PatchType.NUMBER, patch, non_jokers

    def part_of_complete_patch(self, tile):
        return len(self.patch(tile)) > 2

    def neighbouring_patches(self, graph, tile):
        known_patches = set()
        for neighbouring_tile in graph.neighbouring_tiles(tile):
            patch = self.patch(neighbouring_tile)
            if patch not in known_patches:
                known_patches.add(patch)
                yield patch

    def add_singleton(self, tile):
        patchwork = Patchwork(self)
        color = len(patchwork.__patch_to_tiles)
        patchwork.__tiles_to_patches[tile] = color
        patchwork.__patch_to_tiles[color].add(tile)
        return patchwork

    def append(self, graph, tile):
        for patch in self.neighbouring_patches(graph, tile):
            for patch_type, patch, non_jokers in self.patch_type(patch):
                match patch_type:
                    case PatchType.NUMBER:
                        if len(patch) < 4 and (len(non_jokers) == 0 or non_jokers[0].value == tile.value) \
                                and all(non_joker.color != tile.color for non_joker in non_jokers):
                            yield self.add_number(patch, tile)
                    case PatchType.RUN:
                        values = sorted(nj.value for nj in non_jokers)
                        n_jokers = len(patch) - len(non_jokers)
                        n_free_jokers = n_jokers - ((values[-1] - values[0] + 1) - len(non_jokers))
                        if n_free_jokers == 0




class Patcher:

    def __init__(self, graph: Graph, patchwork: Patchwork):
        self.__graph = graph
        self.__original_patchwork = patchwork

    def new_patchwork(self):
        for tile in filter(lambda tile: not self.__original_patchwork.is_patched(tile), self.__graph):
            print(f'uncolored: {tile}')
