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
    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.clear()
        for i in range(1, self.height + 1):
            screen.addch(i, 0, "|", self.color)
            screen.addch(i, self.width + 1, "|", self.color)
        for i in range(1, self.width + 1):
            screen.addch(0, i, "-", self.color)
            screen.addch(self.height + 1, i, "-", self.color)
        screen.addch(0, 0, "~", self.color)
        screen.addch(self.height + 1, 0, "~", self.color)
        screen.addch(0, self.width + 1, "~", self.color)
        screen.addch(self.height + 1, self.width + 1, "~", self.color)
        screen.refresh()
        screen.getch()


    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i, row in enumerate(self.life.curr_generation):
            for j, value in enumerate(row):
                if value == 1:
                    screen.addch(i + 1, j + 1, "#", self.color_green)
                elif value == 0:
                    screen.addch(i + 1, j + 1, " ", self.color_green)
        screen.refresh()
        self.key = screen.getch()

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.color = curses.color_pair(1)
        self.color_green = curses.color_pair(2)
        self.color_red = curses.color_pair(3)
        running = True
        self.draw_borders(screen)
        while running:
            curses.halfdelay(3)
            self.draw_grid(screen)
            self.life.step()
            if not self.life.is_changing:
                running = False
                screen.clear()
                screen.addstr(0, 0, "Life is not changing!", self.color_red)
                screen.refresh()
                screen.getch()
                time.sleep(4)
            if self.life.is_max_generations_exceeded:
                running = False
                screen.clear()
                screen.addstr(0, 0, "Maximum generations exceeded!", self.color_red)
                screen.refresh()
                screen.getch()
                time.sleep(4)
        curses.endwin()

cons = Console(GameOfLife((10,10)))
cons.run()
