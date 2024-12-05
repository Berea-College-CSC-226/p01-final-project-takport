import unittest
import os
from P03_takport import (
    read_leaderboard,
    save_score,
    spawn_obstacle,
    update_player_position,
    update_obstacles,
    handle_collision,
    leaderboard_file,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    obstacles,
    player_rect
)


class TestCarDodgeGame(unittest.TestCase):
    def setUp(self):
        self.test_leaderboard_file = "test_highscores.txt"
        global leaderboard_file
        leaderboard_file = self.test_leaderboard_file
        with open(self.test_leaderboard_file, "w") as file:
            file.write("Alice,100\nBob,150\nCharlie,90\n")

    def tearDown(self):
        if os.path.exists(self.test_leaderboard_file):
            os.remove(self.test_leaderboard_file)

    def test_read_leaderboard(self):
        leaderboard = read_leaderboard()
        self.assertEqual(len(leaderboard), 3)
        self.assertEqual(leaderboard[0], ("Bob", 150))
        self.assertEqual(leaderboard[1], ("Alice", 100))
        self.assertEqual(leaderboard[2], ("Charlie", 90))

    def test_save_score(self):
        save_score("David", 200)
        leaderboard = read_leaderboard()
        self.assertEqual(len(leaderboard), 5)
        self.assertEqual(leaderboard[0], ("David", 200))

    def test_spawn_obstacle(self):
        obstacle = spawn_obstacle()
        self.assertIn(obstacle["x"], [-obstacle["width"], SCREEN_WIDTH])
        self.assertGreaterEqual(obstacle["y"], 0)
        self.assertLessEqual(obstacle["y"] + obstacle["height"], SCREEN_HEIGHT)
        self.assertIn(obstacle["speed"], list(range(-7, -2)) + list(range(3, 8)))

    def test_update_player_position(self):
        global player_rect, move_left, move_right, move_up, move_down
        player_rect.x = 100
        move_left = True
        update_player_position()
        self.assertEqual(player_rect.x, 95)  # Moved left

        move_left = False
        move_right = True
        update_player_position()
        self.assertEqual(player_rect.x, 100)  # Moved right

    def test_update_obstacles(self):
        global obstacles
        obstacles = [
            {"x": -10, "y": 100, "width": 30, "height": 30, "speed": 5},
            {"x": SCREEN_WIDTH + 10, "y": 200, "width": 30, "height": 30, "speed": -5},
            {"x": 400, "y": 300, "width": 30, "height": 30, "speed": 0},
        ]
        update_obstacles()
        self.assertEqual(len(obstacles), 2)

    def test_handle_collision(self):
        global player_rect, obstacles, running
        player_rect.x = 100
        player_rect.y = 100
        obstacles = [{"x": 100, "y": 100, "width": 50, "height": 50, "speed": 0}]
        running = False
        handle_collision()
        self.assertFalse(running)


if __name__ == "__main__":
    unittest.main()
