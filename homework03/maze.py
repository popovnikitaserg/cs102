from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    y, x = x, y
    grid_width, grid_height = len(grid[0]) - 2, len(grid) - 2
    if x != grid_width:
        if choice((0, 1)) == 0:
            if y != 1:
                grid[y - 1][x] = " "
            else:
                grid[y][x + 1] = " "
        else:
            grid[y][x + 1] = " "
    else:
        if y != 1:
            grid[y - 1][x] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for x in range(1, cols - 1, 2):
        for y in range(1, rows - 1, 2):
            remove_wall(grid, (y, x))

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if grid[y][x] == "X":
                exits.append((y, x))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    coords = []
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if grid[y][x] == k:
                coords.append((y, x))
    grid_width, grid_height = len(grid[0]) - 1, len(grid) - 1
    k += 1
    for coord_y, coord_x in coords:
        if coord_x == 0 or coord_x == grid_width or coord_y == 0 or coord_y == grid_height:
            if coord_x == 0:
                grid[coord_y][coord_x + 1] = k
            elif coord_x == grid_width:
                grid[coord_y][coord_x - 1] = k
            elif coord_y == 0:
                grid[coord_y + 1][coord_x] = k
            else:
                grid[coord_y - 1][coord_x] = k
        else:
            if grid[coord_y][coord_x + 1] == 0:
                grid[coord_y][coord_x + 1] = k
            if grid[coord_y][coord_x - 1] == 0:
                grid[coord_y][coord_x - 1] = k
            if grid[coord_y + 1][coord_x] == 0:
                grid[coord_y + 1][coord_x] = k
            if grid[coord_y - 1][coord_x] == 0:
                grid[coord_y - 1][coord_x] = k
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    path = []
    y, x = exit_coord
    y1, x1 = exit_coord
    k = grid[y][x]
    grid_width, grid_height = len(grid[0]) - 1, len(grid) - 1
    while len(path) != (grid[y1][x1] - 1):
        path = []
        while k != 1:
            if x == 0 or x == grid_width or y == 0 or y == grid_height:
                if x == 0 and grid[y][x + 1] == k - 1:
                    k -= 1
                    path.append((y, x + 1))
                    x += 1
                elif x == grid_width and grid[y][x - 1] == k - 1:
                    k -= 1
                    path.append((y, x - 1))
                    x -= 1
                elif y == 0 and grid[y + 1][x] == k - 1:
                    k -= 1
                    path.append((y + 1, x))
                    y += 1
                elif y == grid_height and grid[y - 1][x] == k - 1:
                    k -= 1
                    path.append((y - 1, x))
                    y -= 1
            else:
                dir = choice([(0, 1), (1, 0), (-1, 0), (0, -1)])
                if dir == (1, 0) and grid[y][x + 1] == k - 1:
                    k -= 1
                    path.append((y, x + 1))
                    x += 1
                elif dir == (-1, 0) and grid[y][x - 1] == k - 1:
                    k -= 1
                    path.append((y, x - 1))
                    x -= 1
                elif dir == (0, 1) and grid[y + 1][x] == k - 1:
                    k -= 1
                    path.append((y + 1, x))
                    y += 1
                elif dir == (0, -1) and grid[y - 1][x] == k - 1:
                    k -= 1
                    path.append((y - 1, x))
                    y -= 1
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    y, x = coord
    grid_height, grid_width = len(grid) - 1, len(grid[0]) - 1
    if coord in [(0, 0), (grid_height, 0), (0, grid_width), (grid_height, grid_width)]:
        return True
    if x == 0:
        if grid[y + 1][x] == "■" and grid[y - 1][x] == "■" and grid[y][x + 1] == "■":
            return True
    elif x == grid_width:
        if grid[y + 1][x] == "■" and grid[y - 1][x] == "■" and grid[y][x - 1] == "■":
            return True
    elif y == 0:
        if grid[y][x + 1] == "■" and grid[y][x - 1] == "■" and grid[y + 1][x] == "■":
            return True
    elif y == grid_height:
        if grid[y][x + 1] == "■" and grid[y][x - 1] == "■" and grid[y - 1][x] == "■":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    if len(get_exits(grid)) == 1:
        return grid, get_exits(grid)[0]
    grid1 = deepcopy(grid)
    entry, exit = get_exits(grid1)[0], get_exits(grid1)[1]
    x_e, y_e = entry
    x1, y1 = exit
    if encircled_exit(grid, entry) or encircled_exit(grid, exit):
        return grid, None
    for x in range(1, len(grid1) - 1):
        for y in range(1, len(grid1[x]) - 1):
            if grid1[x][y] != "■":
                grid1[x][y] = 0
    grid1[x_e][y_e], grid1[x1][y1] = 1, 0
    k = 1
    while grid1[x1][y1] == 0:
        grid1 = make_step(grid1, k)
        k += 1
    short_path = shortest_path(grid1, (x1, y1))
    return grid, short_path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(5, 5)))
    GRID = bin_tree_maze(5, 5)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
