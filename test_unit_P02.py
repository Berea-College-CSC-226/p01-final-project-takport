import unittest
from pygame import Rect

# Replace 'P02_takport' with the name of your game script
from P02_takport import spawn_obstacle, update_obstacles, check_collision

# Screen dimensions for consistency
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class TestGameLogic(unittest.TestCase):
    def test_spawn_obstacle(self):
        """Test obstacle spawning logic."""
        obstacle = spawn_obstacle()
        self.assertIn(obstacle["x"], [-obstacle["width"], SCREEN_WIDTH])
        self.assertGreaterEqual(obstacle["y"], 0)
        self.assertLessEqual(obstacle["y"] + obstacle["height"], SCREEN_HEIGHT)
        self.assertTrue(-7 <= obstacle["speed"] <= -2 or 3 <= obstacle["speed"] <= 7)

    def test_update_obstacles(self):
        """Test that obstacles move correctly and off-screen obstacles are removed."""
        obstacles = [
            {"x": -10, "y": 100, "width": 30, "height": 30, "speed": 5},   # Moves right
            {"x": SCREEN_WIDTH + 10, "y": 200, "width": 30, "height": 30, "speed": -5},  # Moves left
            {"x": 400, "y": 300, "width": 30, "height": 30, "speed": 10},  # Stays on screen
        ]
        updated = update_obstacles(obstacles)
        self.assertEqual(len(updated), 1)
        self.assertEqual(updated[0]["x"], 410)

    def test_check_collision(self):
        """Test collision detection between player and obstacles."""
        player_rect = Rect(100, 100, 50, 50)
        obstacle = {"x": 120, "y": 120, "width": 30, "height": 30}
        self.assertTrue(check_collision(player_rect, obstacle))

        no_collision_obstacle = {"x": 200, "y": 200, "width": 30, "height": 30}
        self.assertFalse(check_collision(player_rect, no_collision_obstacle))

if __name__ == "__main__":
    unittest.main()
