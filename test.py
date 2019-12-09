from intcode import Intcode
import unittest


class TestIntcode(unittest.TestCase):

    def test_output(self):
        input_codes = [
            [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],  # 0
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],  # 1
            [3, 3, 1108, -1, 8, 3, 4, 3, 99],  # 2
            [3, 3, 1107, -1, 8, 3, 4, 3, 99],  # 3
            [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9, ],  # 4
            [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],  # 5
            [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125,
             20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]  # 6
        ]
        output_pairs = [
            [[8, 1], [0, 0]],  # 0
            [[7, 1], [8, 0]],  # 1
            [[8, 1], [0, 0]],  # 2
            [[7, 1], [8, 0]],  # 3
            [[0, 0], [9, 1]],  # 4
            [[5, 1], [0, 0]],  # 5
            [[7, 999], [8, 1000], [15, 1001]]  # 6
        ]

        for i in range(len(input_codes)):
            for j in range(len(output_pairs[i])):
                computer = Intcode(input_codes[i], output_pairs[i][j][0])
                while not computer.ready:
                    computer.step()
                self.assertEqual(output_pairs[i][j][1], computer.return_code, "i:{}, j:{}, return:{}, status:{}"
                                 .format(i, j, computer.return_code, computer.ready))
                del computer

    def test_relative(self):
        input_codes = [
            [104, 1125899906842624, 99],
            [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        ]

        expected_results = [
            1125899906842624,
            1219070632396864
        ]

        quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

        for i in range(len(input_codes)):
            computer = Intcode(input_codes[i])
            while not computer.ready:
                computer.step()
            self.assertEqual(expected_results[i], computer.return_code)
            del computer

        computer = Intcode(quine)
        while not computer.ready:
            computer.step()
        self.assertEqual(quine, quine)
        del computer

    def test_simple(self):
        input_codes = [
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [1, 0, 0, 0, 99],
            [2, 3, 0, 3, 99],
            [2, 4, 4, 5, 99, 0],
            [1, 1, 1, 4, 99, 5, 6, 0, 99]
        ]
        output_codes = [
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            [2, 0, 0, 0, 99],
            [2, 3, 0, 6, 99],
            [2, 4, 4, 5, 99, 9801],
            [30, 1, 1, 4, 2, 5, 6, 0, 99]
        ]

        for i in range(len(input_codes)):
            computer = Intcode(input_codes[i])
            while not computer.ready:
                computer.step()
            self.assertEqual(output_codes[i], computer.int_codes)
            del computer


if __name__ == '__main__':
    unittest.main()
