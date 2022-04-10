import unittest
from src.Utils import count_lines_in_file, count_words_in_line


class MyTestCase(unittest.TestCase):
    def test_foo(self):
        lines = 0
        letters = 0
        words = 0

        fname = open("resources/levels/level1.txt", 'r')

        for line in fname:
            lines += 1
            letters += len(line)
            words = 0

            pos = 'out'
            for letter in line:
                if letter != ' ' and pos == 'out':
                    words += 1
                    pos = 'in'
                elif letter == ' ':
                    pos = 'out'

        print("Lines:", lines)
        print("Words:", words)
        print("Letters:", letters)

        expected_lines = 6
        expected_words = 7
        expected_letters = 13

        fname.close()

        self.assertEqual(expected_lines, lines)

    def test_count_lines(self):
        lines = 0
        expected_lines = 6

        fname = open("resources/levels/level1.txt", 'r')
        lines = count_lines_in_file(fname)
        fname.close()

        self.assertEqual(expected_lines, lines)

    def test_count_words(self):
        fname = open("resources/levels/level1.txt", 'r')
        words = count_words_in_line(fname)
        expected_words = 7
        fname.close()

        self.assertEqual(expected_words, words)

    def test_make_list(self):
        field = [[0] * 3 for i in range(3)]

        field[1][2] = 5

        print(len(field))
        print(len(field[1]))
        print(field[1][2])

    def test_read(self):
        fname = open("resources/levels/level1.txt", 'r')
        print(fname.read(2))
        print(fname.read(2))
        print(fname.read(2))
        print(fname.read(2))
        print(fname.read(2))
        print(fname.read(2))
        print(fname.read(2))
        print(fname.read(2))


if __name__ == '__main__':
    unittest.main()
