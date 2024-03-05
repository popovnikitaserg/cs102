import random
import typing as tp
from pprint import pprint as pp
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)# Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            self.draw_grid() # Отрисовка списка клеток
            self.grid = self.get_next_generation()# Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for y, value in enumerate(self.grid):
            for x, _ in enumerate(value):
                if self.grid[y][x] == 0:
                    coord_y = self.cell_size * y + 1
                    coord_x = self.cell_size * x + 1
                    pygame.draw.rect(self.screen, pygame.Color("white"),
                                     (coord_x, coord_y, self.cell_size - 1, self.cell_size - 1))
                if self.grid[y][x] == 1:
                    coord_y = self.cell_size * y + 1
                    coord_x = self.cell_size * x + 1
                    pygame.draw.rect(self.screen, pygame.Color("green"),
                                     (coord_x, coord_y, self.cell_size - 1, self.cell_size - 1))


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        next_cells = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        special = [(0, 0), (0, self.cell_width - 1), (self.cell_height - 1, 0), (self.cell_height - 1, self.cell_width - 1)]
        neighbours = []
        coord_y, coord_x = cell

        if cell in special:
            if cell == special[0]:
                for y, x in [(0, 1), (1, 0), (1, 1)]:
                    if self.grid[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if cell == special[1]:
                for y, x in [(coord_y, coord_x - 1), (coord_y + 1, coord_x - 1), (coord_y + 1, coord_x)]:
                    if self.grid[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if cell == special[2]:
                for y, x in [(coord_y - 1, coord_x), (coord_y - 1, coord_x + 1), (coord_y, coord_x + 1)]:
                    if self.grid[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            if cell == special[3]:
                for y, x in [(coord_y - 1, coord_x), (coord_y - 1, coord_x - 1), (coord_y, coord_x - 1)]:
                    if self.grid[y][x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
        elif coord_y == 0 or coord_y == self.cell_height - 1 or coord_x == 0 or coord_x == self.cell_width - 1:
            if coord_y == 0:
                for y, x in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]:
                    if self.grid[coord_y + y][coord_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            elif coord_y == self.cell_height - 1:
                for y, x in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
                    if self.grid[coord_y + y][coord_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            elif coord_x == 0:
                for y, x in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]:
                    if self.grid[coord_y + y][coord_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
            elif coord_x == self.cell_width - 1:
                for y, x in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]:
                    if self.grid[coord_y + y][coord_x + x] == 1:
                        neighbours.append(1)
                    else:
                        neighbours.append(0)
        else:
            for i in next_cells:
                y, x = i
                if self.grid[coord_y + y][coord_x + x] == 1:
                    neighbours.append(1)
                else:
                    neighbours.append(0)
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        for y, row in enumerate(self.grid):
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



game = GameOfLife(640, 400, 20)
game.run()
