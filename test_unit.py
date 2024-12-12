######################################################################
# Author(s): Tobore Takpor
# Username(s): takport
#
# Assignment: Final Project
#
# Purpose: To test The leaderboard file exists.
# Obstacles are spawned with the correct attributes.
# Audio plays correctly (or skips if the music file is missing).
#
######################################################################



import unittest
import os
import pygame
from Nettspend_Playhouse import CarDodgeGame

class TestCarDodgeGame(unittest.TestCase):

    def test_leaderboard_file_exists(self):
        """Test if the leaderboard file is created and exists."""
        leaderboard_file = "highscores.txt"
        self.assertTrue(os.path.exists(leaderboard_file), "Leaderboard file does not exist.")

    def test_obstacle_spawn_structure(self):
        """Test if the spawn_obstacle method returns a dictionary with correct keys."""
        game = CarDodgeGame()
        obstacle = game.spawn_obstacle()
        self.assertIn("x", obstacle)
        self.assertIn("y", obstacle)
        self.assertIn("width", obstacle)
        self.assertIn("height", obstacle)
        self.assertIn("speed", obstacle)

    def test_audio_playback(self):
        """Test if the audio file loads and plays correctly."""
        game = CarDodgeGame()
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.play()
            is_playing = pygame.mixer.music.get_busy()
            self.assertTrue(is_playing, "Audio did not start playing correctly.")
        except pygame.error:
            self.fail("Audio file could not be loaded or played.")

if __name__ == "__main__":
    unittest.main()
