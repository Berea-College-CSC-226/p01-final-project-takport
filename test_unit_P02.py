import unittest
from P02_takport import read_leaderboard, save_score, spawn_obstacle, update_obstacles

# Test Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing leaderboard
        self.test_leaderboard_file = "test_highscores.txt"
        global leaderboard_file
        leaderboard_file = self.test_leaderboard_file  # Redirect leaderboard file to test file
        with open(self.test_leaderboard_file, "w") as file:
            file.write("Alice,100\nBob,150\nCharlie,90\n")

    def tearDown(self):
        # Remove the test leaderboard file after tests
        import os
        if os.path.exists(self.test_leaderboard_file):
            os.remove(self.test_leaderboard_file)

    def test_read_leaderboard(self):
        """Test that the leaderboard is read correctly and sorted."""
        leaderboard = read_leaderboard()
        self.assertEqual(len(leaderboard), 3)
        self.assertEqual(leaderboard[0], ("Bob", 150))
        self.assertEqual(leaderboard[1], ("Alice", 100))
        self.assertEqual(leaderboard[2], ("Charlie", 90))

    def test_save_score(self):
        """Test saving a new score to the leaderboard."""
        save_score("David", 200)
        leaderboard = read_leaderboard()
        self.assertEqual(len(leaderboard), 4)  # Added new score
        self.assertEqual(leaderboard[0], ("David", 200))  # New high score is at the top

    def test_spawn_obstacle(self):
        """Test obstacle spawning logic."""
        obstacle = spawn_obstacle()
        self.assertIn(obstacle["x"], [-obstacle["width"], SCREEN_WIDTH])
        self.assertGreaterEqual(obstacle["y"], 0)
        self.assertLessEqual(obstacle["y"] + obstacle["height"], SCREEN_HEIGHT)
        self.assertIn(obstacle["speed"], range(-7, -2) + range(3, 8))

    def test_update_obstacles(self):
        """Test that obstacles move correctly and off-screen obstacles are removed."""
        obstacles = [
            {"x": -10, "y": 100, "width": 30, "height": 30, "speed": 5},   # Moves right
            {"x": SCREEN_WIDTH + 10, "y": 200, "width": 30, "height": 30, "speed": -5},  # Moves left
            {"x": 400, "y": 300, "width": 30, "height": 30, "speed": 10},  # Stays on screen
        ]
        updated_obstacles = update_obstacles(obstacles)
        self.assertEqual(len(updated_obstacles), 1)  # Only the one on screen remains
        self.assertEqual(updated_obstacles[0]["x"], 410)


if __name__ == "__main__":
    unittest.main()
