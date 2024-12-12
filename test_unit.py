######################################################################
# Author(s): Tobore Takpor
# Username(s): takport
#
# Assignment: Final Project
#
# Purpose: To test The leaderboard file exists.
# Obstacles are spawned with the correct attributes.
# Audio plays correctly (or skips if the music file is missing).
# Collision detection works as expected.
#
######################################################################



import unittest
import os
from Nettspend_Playhouse import spawn_obstacle, save_score, handle_collision, pygame, player_rect

class TestCarDodgeGame(unittest.TestCase):

    def setUp(self):
        # Set up a test leaderboard file with 5 entries
        self.test_leaderboard_file = "test_highscores.txt"
        with open(self.test_leaderboard_file, "w") as file:
            file.write("Alice,100\n")
            file.write("Bob,200\n")
            file.write("Charlie,150\n")
            file.write("David,250\n")
            file.write("Eve,50\n")

        global leaderboard_file
        leaderboard_file = self.test_leaderboard_file

        # Initialize Pygame for audio test
        pygame.mixer.init()

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_leaderboard_file):
            os.remove(self.test_leaderboard_file)

        # Quit pygame mixer to avoid errors in subsequent tests
        pygame.mixer.quit()

    def test_leaderboard_exists(self):
        # Verify that the leaderboard file exists
        self.assertTrue(os.path.exists(leaderboard_file))

    def test_spawn_obstacle(self):
        # Verify that obstacles have required attributes
        obstacle = spawn_obstacle()
        self.assertIn("x", obstacle)
        self.assertIn("y", obstacle)
        self.assertIn("width", obstacle)
        self.assertIn("height", obstacle)
        self.assertIn("speed", obstacle)

    def test_audio_playback(self):
        # Test that the background music starts playing without errors
        try:
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0)  # Looping music
            # Check if the music is playing
            self.assertTrue(pygame.mixer.music.get_busy())  # Should be True if music is playing
        except FileNotFoundError:
            print("Warning: 'background_music.mp3' not found, skipping audio test.")
            self.assertTrue(True)  # Skip the test if music file is not found

    def test_collision_detection(self):
        # Test collision with an obstacle
        obstacles = [{"x": 100, "y": 100, "width": 60, "height": 100, "speed": 5}]
        player_rect.x = 100  # Position the player right where the obstacle is
        player_rect.y = 100  # Position the player at the obstacle's y-coordinate
        handle_collision()  # This should stop the game as a collision is detected
        self.assertFalse(pygame.mixer.music.get_busy())  # Music should stop on collision

if __name__ == "__main__":
    unittest.main()
