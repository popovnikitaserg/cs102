import pathlib
import random as rn
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open(encoding="utf-8") as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [tuple(i for i in grid[j][pos[1]])[0] for j in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    n = 2
    a = [
        [i[0] for i in grid[j][k]]
        for j in range(pos[0] - pos[0] % 3, n + pos[0] - pos[0] % 3 + 1)
        for k in range(pos[1] - pos[1] % 3, n + pos[1] - pos[1] % 3 + 1)
    ]
    b = [i[0] for i in a]
    return b


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tuple[int, int]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i, value in enumerate(grid):
        for j, inside_value in enumerate(value):
            if inside_value == ".":
                return i, j
    return -1, -1


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    a = set(str(i) for i in range(1, 10))
    a = a - set(get_col(grid, pos)) - set(get_row(grid, pos)) - set(get_block(grid, pos))
    return a


def solve(grid: tp.List[tp.List[str]]) -> list[list[str]]:
    # Как решать Судоку?
    # 1. Найти свободную позицию
    # 2. Найти все возможные значения, которые могут находиться на этой позиции
    # 3. Для каждого возможного значения:
    # 3.1. Поместить это значение на эту позицию
    # 3.2. Продолжить решать оставшуюся часть пазла
    """Решение пазла, заданного в grid
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    if find_empty_positions(grid) == (-1, -1) or len(find_possible_values(grid, find_empty_positions(grid))) == 0:
        return grid
    for i in find_possible_values(grid, find_empty_positions(grid)):
        row, col = find_empty_positions(grid)
        grid[row][col] = i
        solve(grid)
        if find_empty_positions(grid) == (-1, -1):
            break
        grid[row][col] = "."
    return grid


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    for _, value in enumerate(solution):
        for _, inside_value in enumerate(value):
            if inside_value not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return inside_value in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for row1 in solution:
        if len(set(row1)) != 9:
            return len(set(row1)) == 9
    columns = []
    for col1 in range(len(solution)):
        for row1 in solution:
            columns += [row1[col1]]
        if len(set(columns)) != 9:
            return len(set(columns)) == 9
        columns = []
    for row in range(0, 9, 3):
        for col2 in range(0, 9, 3):
            vals = solution[row][col2 : col2 + 3]
            vals.extend(solution[row + 1][col2 : col2 + 3])
            vals.extend(solution[row + 2][col2 : col2 + 3])
            if len(set(vals)) != 9:
                return len(set(vals)) == 9
            vals = []
    return True


def generate_sudoku(N: int) -> tp.Optional[tp.List[tp.List[str]]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = [["." for i in range(9)] for j in range(9)]
    grid = solve(grid)
    counter = 81 - N
    while counter > 0:
        i = rn.randint(0, 8)
        j = rn.randint(0, 8)
        if grid[i][j] != ".":
            grid[i][j] = "."
            counter -= 1
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
