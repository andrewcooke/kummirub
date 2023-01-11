from random import seed
from unittest import TestCase

from networkx import draw_spring

from kummirub.graph import Graph, Patcher, Patchwork
from kummirub.tiles import Bag


class GraphTest(TestCase):

    def test_nx_display(self):
        seed(1)
        bag = Bag()
        graph = Graph()
        # bag = graph.take(len(bag), bag)
        graph, bag = graph.take(30, bag)
        nx = graph.to_nx()
        draw_spring(nx, with_labels=True)
        # uncomment for manual verification
        # plt.show()

    def test_painter(self):
        seed(1)
        bag = Bag()
        graph = Graph()
        graph, bag = graph.take(14, bag)
        patcher = Patcher(graph, Patchwork())
        patcher.new_patchwork()
