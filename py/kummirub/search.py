
from typing import NamedTuple

from kummirub.graph import Patchwork, Graph
from kummirub.tiles import Tile
from kummirub.utils import ImmutableSet

"""
we start from the current patchwork and do a breadth-first search of possible modifications.
in this way we can cut the search short at a given depth if we are time limited.
"""


class SearchState(NamedTuple):

    patchwork: Patchwork
    unused_tiles: tuple[Tile]
    active_tiles = ImmutableSet[Tile]


def next_levels(graph: Graph, state: SearchState):
    if not state.unused_tiles: return
    tile, *rest = state.unused_tiles
    for patchwork in state.patchwork.append(graph, tile):
        yield SearchState(patchwork, tuple(rest), state.active_tiles.add(tile))
    # try number and sequence, with separations into feasible and non-feasible subgroups
    # finally, add single
