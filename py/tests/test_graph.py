from random import seed
from unittest import TestCase

from networkx import draw_spring
import matplotlib.pyplot as plt

from kummirub.graph import Graphs
from kummirub.tiles import Bag


class GraphTest(TestCase):

    def test_nx_display(self):
        seed(1)
        bag = Bag()
        graph = Graphs()
        # bag = graph.take(len(bag), bag)
        graph, bag = graph.take(30, bag)
        nx = graph.to_nx_0()
        draw_spring(nx, with_labels=True)
        # uncomment for manual verification
        plt.show()
