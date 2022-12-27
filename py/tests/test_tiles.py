from random import seed
from unittest import TestCase

from kummirub.tiles import Tile, Color, Bag


class TilesTest(TestCase):

    def test_tiles(self):
        r1a = Tile(Color.RED, 1, 1)
        r1b = Tile(Color.RED, 1, 1)
        r2 = Tile(Color.RED, 2, 1)
        self.assertTrue(r1a == r1b)
        self.assertFalse(r1a == r2)
        self.assertTrue(Color.random() in set(Color))
        self.assertTrue(Tile.random().color in set(Color))
        self.assertTrue(1 <= Tile.random().value <= 13)

    def test_bag(self):
        seed(1)
        bag = Bag()
        self.assertEqual(len(bag), 106)
        tile, bag = bag.draw()
        self.assertEqual(len(bag), 105)
        self.assertEqual(tile, Tile(Color.BLACK, 3, 1))
        tile, bag = bag.draw()
        self.assertEqual(len(bag), 104)
        self.assertEqual(tile, Tile(Color.BLACK, 6, 2))
