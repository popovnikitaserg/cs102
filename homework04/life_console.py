import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.height = life.rows
        self.width = life.cols
        self.speed = 10
        self.begin_x = 20
        self.begin_y = 7
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.color = curses.color_pair(1)
        self.color_green = curses.color_pair(2)
        self.color_red = curses.color_pair(3)
        self.key = None

    def draw_borders(self) -> None:
        """Отобразить рамку."""
        self.screen.clear()
        for i in range(1, self.height + 1):
            self.screen.addch(i, 0, "|", self.color)
            self.screen.addch(i, self.width + 1, "|", self.color)
        for i in range(1, self.width + 1):
            self.screen.addch(0, i, "-", self.color)
            self.screen.addch(self.height + 1, i, "-", self.color)
        self.screen.addch(0, 0, "~", self.color)
        self.screen.addch(self.height + 1, 0, "~", self.color)
        self.screen.addch(0, self.width + 1, "~", self.color)
        self.screen.addch(self.height + 1, self.width + 1, "~", self.color)
        self.screen.refresh()
        self.screen.getch()

    def draw_grid(self) -> None:
        """Отобразить состояние клеток."""
        for i, row in enumerate(self.life.curr_generation):
            for j, value in enumerate(row):
                if value == 1:
                    self.screen.addch(i + 1, j + 1, "#", self.color_green)
                elif value == 0:
                    self.screen.addch(i + 1, j + 1, " ", self.color_green)
        self.screen.refresh()
        self.key = self.screen.getch()

    def run(self) -> None:
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.color = curses.color_pair(1)
        self.color_green = curses.color_pair(2)
        self.color_red = curses.color_pair(3)
        running = True
        self.draw_borders()
        while running:
            curses.halfdelay(3)
            self.draw_grid()
            self.life.step()
            if not self.life.is_changing:
                running = False
                self.screen.clear()
                self.screen.addstr(0, 0, "Life is not changing!", self.color_red)
                self.screen.refresh()
                self.screen.getch()
                time.sleep(4)
            if self.life.is_max_generations_exceeded:
                running = False
                self.screen.clear()
                self.screen.addstr(0, 0, "Maximum generations exceeded!", self.color_red)
                self.screen.refresh()
                self.screen.getch()
                time.sleep(4)
        curses.endwin()


cons = Console(GameOfLife((10, 10)))
cons.run()
