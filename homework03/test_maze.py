import unittest
from random import seed

import maze


class MazeTest(unittest.TestCase):
    def test_remove_wall(self):
        seed(2)
        grid_1 = [
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        coord_1 = (1, 1)
        self.assertEqual(
            [
                ["■", "■", "■", "■", "■"],
                ["■", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■"],
                ["■", " ", "■", " ", "■"],
                ["■", "■", "■", "■", "■"],
            ],
            maze.remove_wall(grid_1, coord_1),
        )

        seed(23)
        grid_2 = [
            ["■", "■", "■", "■", "■", "■", "■"],
            ["■", " ", " ", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■", "■", "■"],
        ]
        coord_2 = (5, 1)
        self.assertEqual(
            [
                ["■", "■", "■", "■", "■", "■", "■"],
                ["■", " ", " ", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■", " ", "■"],
                ["■", " ", " ", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■", "■", "■"],
                ["■", " ", " ", " ", "■", " ", "■"],
                ["■", "■", "■", "■", "■", "■", "■"],
            ],
            maze.remove_wall(grid_2, coord_2),
        )

        seed(14)
        grid_4 = [
            ["■", "■", "■", "■", "■", "■", "■"],
            ["■", " ", " ", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■", "■", "■"],
            ["■", " ", " ", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■", "■", "■"],
        ]
        coord_4 = (5, 5)
        self.assertEqual(
            [
                ["■", "■", "■", "■", "■", "■", "■"],
                ["■", " ", " ", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■", " ", "■"],
                ["■", " ", " ", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■", " ", "■"],
                ["■", " ", " ", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■", "■", "■"],
            ],
            maze.remove_wall(grid_4, coord_4),
        )

    def test_bin_tree_maze(self):
        seed(13)
        expected_grid_42 = [
            ["■", "■", "■", "■", "■"],
            ["X", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual(expected_grid_42, maze.bin_tree_maze(5, 5))

        seed(1115)
        expected_grid_222 = [
            ["■", "X", "■", "X", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual(expected_grid_222, maze.bin_tree_maze(5, 5))

        seed(571)
        expected_grid_622 = [
            ["■", "■", "■", "X", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["X", "■", "■", "■", "■"],
        ]
        self.assertEqual(expected_grid_622, maze.bin_tree_maze(5, 5))

        seed(171)
        expected_grid_f = [
            ["■", "■", "■", "X", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "X", "■", "■", "■"],
        ]
        self.assertEqual(expected_grid_f, maze.bin_tree_maze(5, 5, random_exit=False))

    def test_get_exits(self):
        grid_1 = [
            ["■", "X", "■", "■", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["X", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual([(0, 1), (3, 0)], maze.get_exits(grid_1))
        grid_2 = [
            ["■", "■", "■", "■", "X"],
            ["■", " ", " ", " ", "■"],
            ["X", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual([(0, 4), (2, 0)], maze.get_exits(grid_2))
        grid_3 = [
            ["■", "■", "■", "■", "■"],
            ["X", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual([(1, 0)], maze.get_exits(grid_3))

    def test_encircled_exit(self):
        grid = [
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]

        self.assertFalse(maze.encircled_exit(grid, (1, 0)))
        self.assertFalse(maze.encircled_exit(grid, (0, 1)))
        self.assertFalse(maze.encircled_exit(grid, (4, 3)))
        self.assertFalse(maze.encircled_exit(grid, (3, 1)))
        self.assertTrue(maze.encircled_exit(grid, (0, 0)))
        self.assertTrue(maze.encircled_exit(grid, (4, 4)))
        self.assertTrue(maze.encircled_exit(grid, (0, 4)))
        self.assertTrue(maze.encircled_exit(grid, (4, 0)))
        self.assertTrue(maze.encircled_exit(grid, (0, 2)))
        self.assertTrue(maze.encircled_exit(grid, (2, 0)))
        self.assertTrue(maze.encircled_exit(grid, (2, 4)))
        self.assertTrue(maze.encircled_exit(grid, (4, 2)))

    def test_make_step(self):
        grid_1 = [
            ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
            ["■", 0, 0, 0, 0, 0, 0, 0, 0, 0, "■"],
            ["■", "■", "■", "■", "■", 0, "■", 0, "■", 0, "■"],
            ["■", 0, 0, 0, 0, 0, "■", 0, "■", 3, "■"],
            ["■", "■", "■", "■", "■", "■", "■", "■", "■", 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, "■"],
            ["■", "■", "■", "■", "■", "■", "■", 0, "■", 0, "■"],
            ["■", 0, 0, 0, 0, 0, 0, 0, "■", 0, "■"],
            ["■", "■", "■", 0, "■", "■", "■", 0, "■", 0, "■"],
            ["■", 0, 0, 0, "■", 0, 0, 0, "■", 0, "■"],
            ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ]
        k_1 = 3
        self.assertEqual(
            [
                ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
                ["■", 0, 0, 0, 0, 0, 0, 0, 0, 0, "■"],
                ["■", "■", "■", "■", "■", 0, "■", 0, "■", 4, "■"],
                ["■", 0, 0, 0, 0, 0, "■", 0, "■", 3, "■"],
                ["■", "■", "■", "■", "■", "■", "■", "■", "■", 2, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 4, 3, "■"],
                ["■", "■", "■", "■", "■", "■", "■", 0, "■", 4, "■"],
                ["■", 0, 0, 0, 0, 0, 0, 0, "■", 0, "■"],
                ["■", "■", "■", 0, "■", "■", "■", 0, "■", 0, "■"],
                ["■", 0, 0, 0, "■", 0, 0, 0, "■", 0, "■"],
                ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
            ],
            maze.make_step(grid_1, k_1),
        )

        grid_2 = [
            ["■", "■", 1, "■", "■"],
            ["■", 0, 2, 0, "■"],
            ["■", "■", "■", 0, "■"],
            [0, 0, 0, 0, "■"],
            ["■", "■", "■", "■", "■"],
        ]
        k_2 = 2
        self.assertEqual(
            [
                ["■", "■", 1, "■", "■"],
                ["■", 3, 2, 3, "■"],
                ["■", "■", "■", 0, "■"],
                [0, 0, 0, 0, "■"],
                ["■", "■", "■", "■", "■"],
            ],
            maze.make_step(grid_2, k_2),
        )

        grid_3 = [
            ["■", "■", "■", "■", "■"],
            ["■", 4, 3, 2, 1],
            [0, 5, "■", 3, "■"],
            ["■", 0, "■", 4, "■"],
            ["■", "■", "■", "■", "■"],
        ]
        k_3 = 5
        self.assertEqual(
            [
                ["■", "■", "■", "■", "■"],
                ["■", 4, 3, 2, 1],
                [6, 5, "■", 3, "■"],
                ["■", 6, "■", 4, "■"],
                ["■", "■", "■", "■", "■"],
            ],
            maze.make_step(grid_3, k_3),
        )

    def test_solve_maze(self):
        seed(163)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertEqual([(3, 0), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (2, 4)], path_)

        seed(152)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertEqual([(3, 0), (3, 1), (2, 1), (1, 1), (1, 0)], path_)

        seed(40)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertEqual([(2, 0), (1, 0)], path_)

        seed(1725)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertIsNone(path_)

        seed(1725)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertIsNone(path_)

        seed(177)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertEqual([(4, 3), (3, 3), (3, 2), (3, 1), (3, 0)], path_)

    def test_shortest_path(self):
        grid_1 = [
            ["■", "■", "■", "■", "■"],
            ["■", 0, 0, 0, "■"],
            ["■", "■", "■", 5, "■"],
            [1, 2, 3, 4, "■"],
            ["■", "■", "■", 5, "■"],
        ]
        second_exit_1 = (4, 3)
        self.assertEqual(
            [(4, 3), (3, 3), (3, 2), (3, 1), (3, 0)],
            maze.shortest_path(grid_1, second_exit_1),
        )

        grid_2 = [
            ["■", "■", "■", "■", "■", 1, "■"],
            ["■", 6, 5, 4, 3, 2, "■"],
            ["■", "■", "■", "■", "■", 3, "■"],
            [9, 8, 7, 6, 5, 4, "■"],
            ["■", 9, "■", 7, "■", 5, "■"],
            ["■", 0, "■", 8, "■", 6, "■"],
            ["■", "■", "■", "■", "■", "■", "■"],
        ]
        second_exit_2 = (3, 0)
        self.assertEqual(
            [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (2, 5), (1, 5), (0, 5)],
            maze.shortest_path(grid_2, second_exit_2),
        )

        grid_3 = [
            ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
            ["■", 0, 12, 11, 10, 9, 8, 7, 6, 5, "■"],
            ["■", "■", "■", "■", "■", 10, "■", 8, "■", 4, "■"],
            ["■", 0, 0, 0, 12, 11, "■", 9, "■", 3, "■"],
            ["■", "■", "■", "■", "■", "■", "■", "■", "■", 2, 1],
            [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, "■"],
            ["■", "■", "■", "■", "■", "■", "■", 6, "■", 4, "■"],
            ["■", 0, 12, 11, 10, 9, 8, 7, "■", 5, "■"],
            ["■", "■", "■", 12, "■", "■", "■", 8, "■", 6, "■"],
            ["■", 0, 0, 0, "■", 11, 10, 9, "■", 7, "■"],
            ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ]
        second_exit_3 = (5, 0)
        self.assertEqual(
            [
                (5, 0),
                (5, 1),
                (5, 2),
                (5, 3),
                (5, 4),
                (5, 5),
                (5, 6),
                (5, 7),
                (5, 8),
                (5, 9),
                (4, 9),
                (4, 10),
            ],
            maze.shortest_path(grid_3, second_exit_3),
        )


if __name__ == "__main__":
    unittest.main()
