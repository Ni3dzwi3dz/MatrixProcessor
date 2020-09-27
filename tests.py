from processor import  Matrix
import unittest

class test_Matrix(unittest.TestCase):
    
    def setUp(self) -> None:
        self.sample_matrix = Matrix(3,3)

        self.sample_matrix.add_row([13, 25, 39])
        self.sample_matrix.add_row([ 3, 12, 0])
        self.sample_matrix.add_row([12, 22, 11])

    def test_determinant(self) -> None:
        # checks determinant counting

        self.assertEqual(self.sample_matrix.determinant(), -2151)

    def test_dimensions(self) -> None:

        self.assertEqual(self.sample_matrix.get_dimensions(), (3, 3))

    def test_trace(self) -> None:

        self.assertEqual(self.sample_matrix.trace(), 36)

    def test_minor(self) -> None:

        minor12 = Matrix(2,2)
        minor12.add_row([13,25])
        minor12.add_row([12,22])
        self.assertEqual(self.sample_matrix.minor(1,2).numbers, minor12.numbers)


unittest.main()
