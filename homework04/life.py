import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        if randomize:
            grid = [[random.randint(0, 1) for i in range(self.cols)] for j in range(self.rows)]
        else:
            grid = [[0] * self.cols for i in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        next_cells = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        special = [(0, 0), (self.rows - 1, 0), (0, self.cols - 1), (self.rows - 1, self.cols - 1)]
        neighbours = []
        c_y, c_x = cell

        if cell in special:
            if cell == special[0]:
                for y, x in [(0, 1), (1, 0), (1, 1)]:
                    if self.curr_generation[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if cell == special[1]:
                for y, x in [(c_y, c_x + 1), (c_y - 1, c_x + 1), (c_y - 1, c_x)]:
                    if self.curr_generation[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if cell == special[2]:
                for y, x in [(c_y + 1, c_x), (c_y + 1, c_x - 1), (c_y, c_x - 1)]:
                    if self.curr_generation[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if cell == special[3]:
                for y, x in [(c_y - 1, c_x), (c_y - 1, c_x - 1), (c_y, c_x - 1)]:
                    if self.curr_generation[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
        elif c_y == 0 or c_y == self.rows - 1 or c_x == 0 or c_x == self.cols - 1:
            if c_y == 0:
                for y, x in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]:
                    if self.curr_generation[c_y + y][c_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if c_y == self.rows - 1:
                for y, x in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
                    if self.curr_generation[c_y + y][c_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if c_x == 0:
                for y, x in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]:
                    if self.curr_generation[c_y + y][c_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if c_x == self.cols - 1:
                for y, x in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]:
                    if self.curr_generation[c_y + y][c_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
        else:
            for i in next_cells:
                y, x = i
                if self.curr_generation[c_y + y][c_x + x] == 1:
                    neighbours.append(1)
                else:
                    neighbours.append(0)
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = [[0] * self.cols for i in range(self.rows)]
        for y, row in enumerate(self.curr_generation):
            for x, value in enumerate(row):
                neighbours = self.get_neighbours((y, x))
                if value == 1:
                    if sum(neighbours) == 2 or sum(neighbours) == 3:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
                else:
                    if sum(neighbours) == 3:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]
            lines.remove("")
        new_grid = [[0] * len(lines[0]) for i in range(len(lines))]
        for i, row in enumerate(lines):
            for j, value in enumerate(row):
                new_grid[i][j] = int(value)
        life = GameOfLife((len(new_grid), len(new_grid[0])))
        life.curr_generation = new_grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for _, row in enumerate(self.curr_generation):
                for _, value in enumerate(row):
                    f.write(str(value))
                f.write("\n")
