import pathlib

import pygame
import pygame.freetype
from pygame.locals import QUIT

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.height = self.cell_size * life.cols
        self.width = self.cell_size * life.rows
        # Устанавливаем размер окна
        self.screen_size = self.height, self.width
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.width))
        for y in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.height, y))

    def draw_grid(self) -> None:
        grid = self.life.curr_generation
        for y, value in enumerate(grid):
            for x, _ in enumerate(value):
                if grid[y][x] == 0:
                    c_y = self.cell_size * y + 1
                    c_x = self.cell_size * x + 1
                    r_x, r_y = self.cell_size - 1, self.cell_size - 1
                    pygame.draw.rect(self.screen, pygame.Color("white"), (c_x, c_y, r_x, r_y))
                if grid[y][x] == 1:
                    c_y = self.cell_size * y + 1
                    c_x = self.cell_size * x + 1
                    r_x, r_y = self.cell_size - 1, self.cell_size - 1
                    pygame.draw.rect(self.screen, pygame.Color("green"), (c_x, c_y, r_x, r_y))

    def run(self) -> None:
        pygame.init()
        game_font = pygame.freetype.SysFont("Comic Sans MS", 25)
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running, pause = True, False
        state = running
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        state = pause
                    elif event.key == pygame.K_s:
                        state = running
            else:
                if state == running:
                    self.draw_lines()
                    self.draw_grid()  # Отрисовка списка клеток
                    self.life.step()  # Выполнение одного шага игры (обновление состояния ячеек)

                    if not self.life.is_changing:
                        game_font.render_to(self.screen, (40, 1), "Life not changing!", (220, 0, 0))
                        running = False
                        pygame.display.flip()
                        pygame.time.delay(4000)
                    if self.life.is_max_generations_exceeded:
                        game_font.render_to(self.screen, (40, 1), "Max gen exceeded!", (220, 0, 0))
                        running = False
                        pygame.display.flip()
                        pygame.time.delay(4000)
                    else:
                        pygame.display.flip()
                        clock.tick(self.speed)
                        continue

                elif state == pause:
                    self.draw_grid()
                    pygame.display.flip()
                    while state == pause:
                        event = pygame.event.wait()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            pos = pos[0] // self.cell_size, pos[1] // self.cell_size
                            x, y = pos
                            grid = self.life.curr_generation
                            if grid[y][x] == 1:
                                grid[y][x] = 0
                                self.draw_grid()
                            elif grid[y][x] == 0:
                                grid[y][x] = 1
                                self.draw_grid()
                            pygame.display.flip()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_s:
                                state = running
                            elif event.key == pygame.K_f:
                                file_name = input()
                                self.life.save(pathlib.Path(file_name))
                        elif event.type == QUIT:
                            break
                    continue
            break
        pygame.quit()
