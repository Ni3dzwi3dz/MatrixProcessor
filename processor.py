from __future__ import annotations
from typing import Tuple, List, Union


class Matrix:

    def __init__(self, rows: int = 1, columns: int = 1) -> None:
        self.rows = rows
        self.columns = columns
        self.numbers = []

    def fill_with_blanks(self) -> None:
        self.numbers = [[0 for column in range(self.columns)] for row in range(self.rows)]

    def get_dimensions(self) -> Tuple[int, int]:
        return (self.rows, self.columns)

    def fill_row(self, row_number: int, row: List[Union[int, float]]) -> None:
        # need to add some safety switches here
        for c in range(self.columns):
            self.numbers[row_number][c] = row[c]

    def add_row(self, row: List[Union[int, float]]):
        self.numbers.append(row)

    def trace(self) -> float:
        trace = 0

        for i in range(min(self.rows, self.columns)):
            trace += self.numbers[i][i]

        return trace

    def multiply(self, other: Matrix) -> Matrix:

        if self.columns == other.rows:
            result = Matrix(self.rows, other.columns)
            result.fill_with_blanks()

            for i in range(result.rows):
                for j in range(result.columns):
                    for k in range(other.rows):
                        result.numbers[i][j] += self.numbers[i][k] * other.numbers[k][j]

            return result

        else:
            return self

    def diagonal_transpose(self) -> None:

        for r in range(self.rows):
            for c in range(self.columns):
                if r > c:
                    self.numbers[r][c], self.numbers[c][r] = self.numbers[c][r], self.numbers[r][c]

    def side_diagonal_transpose(self) -> None:

        self.horizontal_transpose()
        self.vertical_transpose()
        self.diagonal_transpose()

    def vertical_transpose(self) -> None:

        for r in range(self.rows):
            for c in range(self.columns // 2):
                self.numbers[r][c], self.numbers[r][self.columns - 1 - c] = self.numbers[r][self.columns - 1 - c], \
                                                                            self.numbers[r][c]

    def horizontal_transpose(self) -> None:

        for r in range(self.rows // 2):
            for c in range(self.columns):
                self.numbers[r][c], self.numbers[self.rows - 1 - r][c] = self.numbers[self.rows - 1 - r][c], \
                                                                         self.numbers[r][c]

    def minor(self, row, column) -> Matrix:

        minor = Matrix(self.rows - 1, self.columns - 1)

        # we exclude one row from original matrix
        if row < (len(self.numbers) - 1):
            minor.numbers = self.numbers[:row] + self.numbers[row + 1:]
        else:
            minor.numbers = self.numbers[:row]

        # and now we cut the column from every row
        for i in range(len(minor.numbers)):
            if column < len(minor.numbers[i]):
                minor.numbers[i] = minor.numbers[i][:column] + minor.numbers[i][column + 1:]
            else:
                minor.numbers[i] = minor.numbers[i][:column]

        return minor

    def determinant(self) -> Union[int, float]:

        total: Union[int, float] = 0

        # base options
        if len(self.numbers) == 2 and len(self.numbers[0]) == 2:
            determinant = self.numbers[0][0] * self.numbers[1][1] - self.numbers[1][0] * self.numbers[0][1]
            return determinant

        elif self.get_dimensions() == (1, 1):
            return self.numbers[0][0]

        # recursive slicing
        for c in range(len(self.numbers[0])):
            minor = self.minor(0, c)
            sign = (-1) ** c
            total += sign * minor.determinant() * self.numbers[0][c]
        return total

    def inverted(self) -> Union[Matrix, str]:

        if self.determinant() == 0:
            return "This matrix doesn't have an inverse."

        inverted: Matrix = self.cofactor_matrix()
        inverted.diagonal_transpose()
        inv_det = 1 / self.determinant()

        inverted = inverted * inv_det

        for r in range(self.rows):
            for c in range(self.columns):
                inverted.numbers[r][c] = inverted.numbers[r][c]
        return inverted

    def cofactor_matrix(self) -> Matrix:

        cofactor: Matrix = Matrix(self.rows, self.columns)
        cofactor.fill_with_blanks()

        for r in range(self.rows):
            for c in range(self.columns):
                sub_matrix = self.minor(r, c)
                sign = (-1) ** (r + c)
                cofactor.numbers[r][c] = sub_matrix.determinant() * sign

                if cofactor.numbers[r][c] == 0:
                    cofactor.numbers[r][c] = 0.00

        return cofactor

    # for Matrix + Matrix addition
    def __add__(self, other: Matrix) -> Union[Matrix, str]:
        # in order to add two matrices, they have to have the same dimensions
        if self.get_dimensions() == other.get_dimensions():
            for r in range(self.rows):
                for c in range(self.columns):
                    self.numbers[r][c] += other.numbers[r][c]

            return self

        else:
            return 'ERROR'

    def __mul__(self, other: Union[int, float]) -> Matrix:
        for r in range(self.rows):
            for c in range(self.columns):
                self.numbers[r][c] = self.numbers[r][c] * other

        return self

    __rmul__ = __mul__

    def __repr__(self) -> str:
        repr_string = ''

        for row in self.numbers:
            for element in row:
                repr_string += f' {element:7.4f}'
            repr_string += ' \n'

        return repr_string


class Program:

    def __init__(self) -> None:
        pass

    def main_menu(self) -> None:

        menu = '''1. Add matrices \n 2. Multiply matrix by a constant \n 3. Multiply matrices \n 4. Transpose matrix
0. Exit'''
        choice = ''

        while choice != 0:
            print(menu)
            choice = input('Your choice: ')

            if choice == '1':
                self.add_matrices()
            elif choice == '2':
                self.multiply_constant()
            elif choice == '3':
                self.multiply_matrices()
            elif choice == '4':
                self.transpose_menu()
            elif choice == '5':
                self.calculate_determinant()
            elif choice == '6':
                self.inverse()
            elif choice == '0':
                break
            else:
                print('I`m sorry Dave. I`m afraid I can`t do that')

    def load_matrix(self) -> Matrix:

        rows, columns = map(int, input('Enter matrix size').split())
        print('Enter matrix')

        new_matrix = Matrix(rows, columns)

        for r in range(rows):
            new_matrix.add_row([int(i) if i.isdigit() else float(i) for i in input().split()])

        return new_matrix

    def add_matrices(self) -> None:

        matrix_a = self.load_matrix()
        matrix_b = self.load_matrix()

        if matrix_a.get_dimensions() == matrix_b.get_dimensions():
            print('The result is:')
            print(matrix_a + matrix_b)
        else:
            print('The operation cannot be performed')

    def multiply_constant(self) -> None:

        matrix_a = self.load_matrix()
        constant = float(input())

        print('The result is:')
        print(matrix_a * constant)

    def multiply_matrices(self) -> None:

        matrix_a = self.load_matrix()
        matrix_b = self.load_matrix()

        if matrix_a.columns == matrix_b.rows:
            print('The result is:')
            print(matrix_a.multiply(matrix_b))
        else:
            print('The operation cannot be performed')

    def transpose_menu(self) -> None:
        menu = '1. Main diagonal \n 2. Side diagonal \n 3. Vertical line \n 4. Horizontal line'

        print(menu)
        choice = input()

        matrix_a = self.load_matrix()

        if choice == '1':
            matrix_a.diagonal_transpose()
            print(matrix_a)
        elif choice == '2':
            matrix_a.side_diagonal_transpose()
            print(matrix_a)
        elif choice == '3':
            matrix_a.vertical_transpose()
            print(matrix_a)
        elif choice == '4':
            matrix_a.horizontal_transpose()
            print(matrix_a)
        else:
            print('I`m sorry Dave. I`m afraid I can`t do that')

    def calculate_determinant(self) -> None:
        matrix_a = self.load_matrix()

        print('The result is:')
        print(matrix_a.determinant())

    def inverse(self) -> None:

        matrix_a = self.load_matrix()

        print('The result is:')
        print(matrix_a.inverted())


if __name__ == '__main__':
    program = Program()
    program.main_menu()
