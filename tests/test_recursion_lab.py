import pytest

FOLDER = 'Recursion - Lab'


@pytest.fixture(scope='module')
def array_sum_mod(load):
    return load(FOLDER, '01_recursive_array_sum.py')


@pytest.fixture(scope='module')
def factorial_mod(load):
    return load(FOLDER, '02_recursive_factorial.py')


@pytest.fixture(scope='module')
def drawing_mod(load):
    return load(FOLDER, '03_recursive_drawing.py')


@pytest.fixture(scope='module')
def vectors_mod(load):
    return load(FOLDER, '04_generating_vectors.py')


@pytest.fixture(scope='module')
def labyrinth_mod(load):
    return load(FOLDER, '05_paths_in_labyrinth.py')


@pytest.fixture(scope='module')
def queens_mod(load):
    return load(FOLDER, '06_8_queens_puzzle.py')


@pytest.fixture(scope='module')
def fibonacci_mod(load):
    return load(FOLDER, '07_recursive_fibonacci.py')


def test_array_sum(array_sum_mod):
    assert array_sum_mod.array_sum([1, 2, 3, 4], 0) == 10
    assert array_sum_mod.array_sum([-5, 5, 7], 0) == 7


def test_array_sum_one_item(array_sum_mod):
    assert array_sum_mod.array_sum([42], 0) == 42


@pytest.mark.parametrize('n, expected', [(0, 1), (1, 1), (5, 120), (10, 3628800)])
def test_factorial(factorial_mod, n, expected):
    assert factorial_mod.calc_fact(n) == expected
    assert factorial_mod.iterative_fact(n) == expected


@pytest.mark.parametrize('n, expected', [(1, 1), (2, 2), (5, 8), (10, 89)])
def test_fibonacci(fibonacci_mod, n, expected):
    assert fibonacci_mod.calc_fib(n) == expected
    assert fibonacci_mod.iterative_fib(n) == expected


def test_fibonacci_zero(fibonacci_mod):
    assert fibonacci_mod.calc_fib(0) == 1


def test_fibonacci_iterative_big(fibonacci_mod):
    assert fibonacci_mod.iterative_fib(50) == 20365011074


def test_drawing(drawing_mod):
    assert drawing_mod.get_figure(3) == ['***', '**', '*', '#', '##', '###']


def test_drawing_one_and_zero(drawing_mod):
    assert drawing_mod.get_figure(1) == ['*', '#']
    assert drawing_mod.get_figure(0) == []


def test_vectors(vectors_mod):
    assert vectors_mod.generate_vectors(2) == ['00', '01', '10', '11']
    assert len(vectors_mod.generate_vectors(5)) == 32


def test_vectors_edge(vectors_mod):
    assert vectors_mod.generate_vectors(1) == ['0', '1']
    assert vectors_mod.generate_vectors(0) == ['']


def test_labyrinth_one_path(labyrinth_mod):
    assert labyrinth_mod.get_all_paths(['-e']) == ['R']


def test_labyrinth_two_paths(labyrinth_mod):
    assert labyrinth_mod.get_all_paths(['--', '-e']) == ['RD', 'DR']


def test_labyrinth_wall_blocks_exit(labyrinth_mod):
    assert labyrinth_mod.get_all_paths(['-*e']) == []


def test_labyrinth_does_not_change_input(labyrinth_mod):
    lab = ['--', '-e']
    labyrinth_mod.get_all_paths(lab)
    assert lab == ['--', '-e']


@pytest.mark.parametrize('n, count', [(1, 1), (2, 0), (3, 0), (4, 2), (6, 4), (8, 92)])
def test_queens_count(queens_mod, n, count):
    assert len(queens_mod.solve_queens(n)) == count


def test_queens_first_solution_for_four(queens_mod):
    assert queens_mod.solve_queens(4)[0] == [
        '- * - -',
        '- - - *',
        '* - - -',
        '- - * -',
    ]


def test_queens_solutions_are_valid(queens_mod):
    for solution in queens_mod.solve_queens(6):
        positions = []
        for row, line in enumerate(solution):
            cells = line.split()
            assert cells.count('*') == 1
            positions.append((row, cells.index('*')))

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                (r1, c1), (r2, c2) = positions[i], positions[j]
                assert c1 != c2
                assert abs(r1 - r2) != abs(c1 - c2)
