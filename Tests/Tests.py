import unittest
from src.SokobanGame import *


class MyTestCase(unittest.TestCase):
    def test_new_game(self):
        _game = SokobanGame()
        _game.new_game('../resources/levels/level1.txt')

        expected_width = 7
        expected_height = 6

        _width = _game.get_width()
        _height = _game.get_height()

        self.assertEqual(expected_height, _height)
        self.assertEqual(expected_width, _width)

    def test_move_x(self):
        _game = SokobanGame()
        _game.new_game('../resources/levels/level1.txt')

        dx = -1
        dy = 0
        _game.move(dx, dy)

        expected_x = 3

        self.assertEqual(expected_x, _game.now_point.get_x())

    def test_move_y(self):
        _game = SokobanGame()
        _game.new_game('../resources/levels/level1.txt')

        dx = 0
        dy = 1
        _game.move(dx, dy)

        expected_y = 2

        self.assertEqual(expected_y, _game.now_point.get_y())

    def test_move_box(self):
        _game = SokobanGame()
        _game.new_game('../resources/levels/level1.txt')

        _game.move(0, 1)
        _game.move(-1, 0)
        _game.move(-1, 0)
        _game.move(0, 1)

        self.assertEqual(True, _game.was_moved_box)

    def test_win(self):
        _game = SokobanGame()
        _game.new_game('../resources/levels/level1.txt')

        _game.move(0, 1)
        _game.move(-1, 0)
        _game.move(-1, 0)
        _game.move(-1, 0)
        _game.move(0, 1)
        _game.move(0, -1)
        _game.move(1, 0)
        _game.move(0, 1)
        _game.move(0, 1)

        self.assertEqual(True, _game.is_win())


if __name__ == '__main__':
    unittest.main()
