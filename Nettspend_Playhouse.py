######################################################################
# Author(s): Tobore Takpor
# Username(s): takport
#
# Assignment: Final Project
#
# Purpose: To create an interactive video game for users to play
#
######################################################################


import pygame
import random
import sys
import os


class CarDodgeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Game Setup
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.PLAYER_SPEED = 6

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Initialize the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Car Dodge Game")

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Load Background Image
        self.background_image = self.load_image("background.png", self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Load Car Image
        self.car_width = 50
        self.car_height = 100
        self.car_image = self.load_image("car.png", self.car_width, self.car_height, self.GREEN)

        # Load Truck Image
        self.truck_width = 60
        self.truck_height = 100
        self.truck_image = self.load_image("truck.png", self.truck_width, self.truck_height, self.RED)

        # Fonts for displaying text
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        # Player (Car) Object
        self.player_rect = pygame.Rect(
            self.SCREEN_WIDTH // 2 - self.car_width // 2,
            self.SCREEN_HEIGHT - self.car_height - 10,
            self.car_width,
            self.car_height
        )

        # Obstacle List
        self.obstacles = []

        # Movement Flags
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        # Game Variables
        self.score = 0
        self.player_name = ""
        self.running = True
        self.leaderboard_file = "highscores.txt"

        # Ensure the highscores.txt file exists
        if not os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, "w") as file:
                file.write("")

    def load_image(self, filename, width, height, fallback_color=None):
        try:
            image = pygame.image.load(filename)
            return pygame.transform.scale(image, (width, height))
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Using a placeholder.")
            if fallback_color:
                image = pygame.Surface((width, height))
                image.fill(fallback_color)
                return image
            return None

    def read_leaderboard(self):
        scores = []
        with open(self.leaderboard_file, "r") as file:
            for line in file:
                try:
                    name, score = line.strip().split(",")
                    scores.append((name, int(score)))
                except (ValueError, IndexError):
                    continue
        return sorted(scores, key=lambda x: x[1], reverse=True)[:5]

    def save_score(self, name, new_score):
        scores = self.read_leaderboard()
        scores.append((name, new_score))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
        with open(self.leaderboard_file, "w") as file:
            for name, score in scores:
                file.write(f"{name},{score}\n")

    def spawn_obstacle(self):
        obs_width = self.truck_width
        obs_height = self.truck_height
        obs_y = random.randint(0, self.SCREEN_HEIGHT - obs_height)
        obs_x, direction = (-obs_width, 1) if random.choice([True, False]) else (self.SCREEN_WIDTH, -1)
        obs_speed = random.randint(3, 7) * direction
        return {"x": obs_x, "y": obs_y, "width": obs_width, "height": obs_height, "speed": obs_speed}

    def update_player_position(self):
        if self.move_left and self.player_rect.left > 0:
            self.player_rect.x -= self.PLAYER_SPEED
        if self.move_right and self.player_rect.right < self.SCREEN_WIDTH:
            self.player_rect.x += self.PLAYER_SPEED
        if self.move_up and self.player_rect.top > 0:
            self.player_rect.y -= self.PLAYER_SPEED
        if self.move_down and self.player_rect.bottom < self.SCREEN_HEIGHT:
            self.player_rect.y += self.PLAYER_SPEED

    def handle_collision(self):
        for obs in self.obstacles:
            obs_rect = pygame.Rect(obs["x"], obs["y"], obs["width"], obs["height"])
            if self.player_rect.colliderect(obs_rect):
                pygame.mixer.music.stop()
                print("Collision detected! Game over!")
                self.running = False

    def update_obstacles(self):
        for obs in self.obstacles:
            obs["x"] += obs["speed"]
        self.obstacles = [obs for obs in self.obstacles if 0 <= obs["x"] <= self.SCREEN_WIDTH]

    def draw_game_objects(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.BLACK)

        self.screen.blit(self.car_image, (self.player_rect.x, self.player_rect.y))
        for obs in self.obstacles:
            self.screen.blit(self.truck_image, (obs["x"], obs["y"]))

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        leaderboard = self.read_leaderboard()
        y_offset = 50
        for i, (name, high_score) in enumerate(leaderboard, start=1):
            high_score_text = self.font.render(f"{i}. {name}: {high_score}", True, self.WHITE)
            self.screen.blit(high_score_text, (10, y_offset))
            y_offset += 30

    def display_game_over(self):
        self.screen.fill(self.BLACK)
        game_over_text = self.large_font.render("Game Over!", True, self.WHITE)
        self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 - 50))
        leaderboard = self.read_leaderboard()
        y_offset = self.SCREEN_HEIGHT // 2 + 50
        for i, (name, high_score) in enumerate(leaderboard, start=1):
            high_score_text = self.font.render(f"{i}. {name}: {high_score}", True, self.WHITE)
            self.screen.blit(high_score_text, (self.SCREEN_WIDTH // 2 - 100, y_offset))
            y_offset += 30
        pygame.display.flip()
        pygame.time.wait(5000)

    def input_name_screen(self):
        input_text = ""
        prompt = self.large_font.render("Enter Your Name:", True, self.WHITE)
        self.screen.fill(self.BLACK)
        self.screen.blit(prompt, (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        typing = True
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.player_name = input_text if input_text else "Player"
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            self.screen.fill(self.BLACK)
            self.screen.blit(prompt, (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 50))
            entered_name = self.font.render(input_text, True, self.WHITE)
            self.screen.blit(entered_name, (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 + 50))
            pygame.display.flip()

    def game_loop(self):
        try:
            pygame.mixer.music.load("background_music.mp3")

            pygame.mixer.music.play(-1)
        except FileNotFoundError:
            print("Background music file not found.")

        spawn_timer = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.move_right = True
                    elif event.key == pygame.K_UP:
                        self.move_up = True
                    elif event.key == pygame.K_DOWN:
                        self.move_down = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.move_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.move_right = False
                    elif event.key == pygame.K_UP:
                        self.move_up = False
                    elif event.key == pygame.K_DOWN:
                        self.move_down = False

            self.update_player_position()
            self.handle_collision()
            self.update_obstacles()

            # Spawn new obstacles periodically
            spawn_timer += 1
            if spawn_timer >= self.FPS * 1:  # Spawn every 1 second
                self.obstacles.append(self.spawn_obstacle())
                spawn_timer = 0

            # Update the score
            self.score += 1

            # Draw everything on the screen
            self.draw_game_objects()
            self.display_score()
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)

        self.save_score(self.player_name, self.score)
        self.display_game_over()
        pygame.quit()
        sys.exit()

    def start_game(self):
        self.input_name_screen()
        self.game_loop()


if __name__ == "__main__":
    game = CarDodgeGame()
    game.start_game()
