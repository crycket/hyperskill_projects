from functools import wraps

EXIT = '0'
MAIN = ADD = '1'
SIDE = SCALAR = '2'
VERTICAL = PRODUCT = '3'
HORIZONTAL = TRANSPOSE = '4'
DETERMINANT = '5'
INVERSE = '6'


def result_is(func):
    @wraps(func)
    def decorate(*args, **kargs):
        print("The result is:")
        return_val = func(*args, **kargs)
        print()
        return return_val
    return decorate


def menu():
    print('1. Add matrices\n'
          '2. Multiply matrix by a constant\n'
          '3. Multiply matrices\n'
          '4. Transpose matrix\n'
          '5. Calculate a determinant\n'
          '6. Inverse matrix\n'
          '0. Exit')
    return input("Your choice: ")


def transpose_menu():
    print('1. Main diagonal\n'
          '2. Side diagonal\n'
          '3. Vertical line\n'
          '4. Horizontal line')
    return input("Your choice: ")


def get_matrix_size(string=''):
    row, column = input(f"Enter size of {string} matrix: ").split()
    return int(row), int(column)


def get_matrix(row, string=''):
    print("Enter", string, "matrix:")
    return [list(map(float, input().split())) for _ in range(row)]


class Matrix:
    def __init__(self, name='', row=None, column=None, data=None):
        if row is None or column is None:
            self.row, self.column = get_matrix_size(name)
        else:
            self.row, self.column = row, column
        if data is None:
            self.data = get_matrix(self.row, name)
        else:
            self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return self.data.__iter__()

    def minor(self, i, j):
        minor_ij = [[self.data[ii][jj] for jj in range(self.column) if jj != j] for ii in range(self.row) if ii != i]
        # print(f"minor_{i}{j}\n", minor_ij)
        return Matrix('', self.row - 1, self.column - 1, minor_ij)

    def cofactor(self, i, j):
        return (-1) ** (i+j) * det(self.minor(i, j))

    def adjoint(self):
        data = [[self.cofactor(i, j) for j in range(self.column)] for i in range(self.row)]
        # print("cofactors:\n", data)
        data = [[data[r][c] for r in range(self.row)] for c in range(self.column)]
        # print("transpose cofactors:\n", data)
        return Matrix('', self.row, self.column, data)


@result_is
def add(matrix1, matrix2):
    for row_matrix1, row_matrix2 in zip(matrix1, matrix2):
        print(*(round(sum(n), 2) for n in zip(row_matrix1, row_matrix2)))


@result_is
def multiply_by_scalar(matrix, constant):
    for row in matrix:
        print(*[element * constant for element in row])


@result_is
def multiply(matrix1, matrix2):
    for row in matrix1:
        print(*[sum(row[j] * matrix2[j][i] for j in range(matrix2.row)) for i in range(matrix2.column)])


def add_matrices():
    m1 = Matrix('first')
    m2 = Matrix('second')
    if m1.row == m2.row and m1.column == m2.column:
        add(m1, m2)
    else:
        print("The operation cannot be performed.")


def scalar_product():
    m = Matrix()
    const_value = float(input("Enter constant: "))
    multiply_by_scalar(m, const_value)


def product():
    m1 = Matrix('first')
    m2 = Matrix('second')
    if m1.column == m2.row:
        multiply(m1, m2)
    else:
        print("The operation cannot be performed.")


@result_is
def main_diagonal(matrix):
    for c in range(matrix.column):
        print(*[matrix[r][c] for r in range(matrix.row)])


@result_is
def side_diagonal(matrix):
    for c in reversed(range(matrix.column)):
        print(*[matrix[r][c] for r in reversed(range(matrix.row))])


@result_is
def vertical_line(matrix):
    for r in range(matrix.row):
        print(*[matrix[r][c] for c in reversed(range(matrix.column))])


@result_is
def horizontal_line(matrix):
    for r in reversed(range(matrix.row)):
        print(*[matrix[r][c] for c in range(matrix.column)])


def transpose():
    choice_t = transpose_menu()
    m = Matrix()
    if choice_t == MAIN:
        main_diagonal(m)
    elif choice_t == SIDE:
        side_diagonal(m)
    elif choice_t == VERTICAL:
        vertical_line(m)
    elif choice_t == HORIZONTAL:
        horizontal_line(m)


def det(m):
    if m.column == 1:
        return m[0][0]
    if m.column == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return sum(m[0][j] * m.cofactor(0, j) for j in range(m.column))


def calculate_determinant():
    m = Matrix()
    if m.column == m.row:
        print(det(m))


def inverse_matrix(m):
    d = det(m)
    if d == 0:
        print("This matrix doesn't have an inverse.")
    else:
        multiply_by_scalar(m.adjoint(), 1/d)


def calculate_inverse():
    m = Matrix()
    if m.column == m.row:
        inverse_matrix(m)


while True:
    choice = menu()
    if choice == EXIT:
        break
    elif choice == ADD:
        add_matrices()
    elif choice == SCALAR:
        scalar_product()
    elif choice == PRODUCT:
        product()
    elif choice == TRANSPOSE:
        transpose()
    elif choice == DETERMINANT:
        calculate_determinant()
    elif choice == INVERSE:
        calculate_inverse()
