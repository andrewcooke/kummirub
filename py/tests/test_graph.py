from random import seed
from unittest import TestCase

from matplotlib import pyplot as plt
from networkx import draw_spring

from kummirub.graph import Graph
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
        plt.show()
