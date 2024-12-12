######################################################################
# Author(s): Tobore Takpor
# Username(s): takport
#
# Assignment: Final Project
#
# Purpose: To create an interactive video game for users to play
#
######################################################################
# Acknowledgements:


import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Dodge Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load Car Image or Use Placeholder
try:
    car_image = pygame.image.load("car.png")  # Replace with your car image file path
    car_width = 50
    car_height = 100
    car_image = pygame.transform.scale(car_image, (car_width, car_height))
except FileNotFoundError:
    print("Error: 'car.png' not found. Using a green rectangle as a placeholder.")
    car_width = 50
    car_height = 100
    car_image = pygame.Surface((car_width, car_height))
    car_image.fill(GREEN)  # Green rectangle placeholder

# Load Truck Image for Obstacles
try:
    truck_image = pygame.image.load("truck.png")  # Replace with your truck image file path
    truck_width = 60  # Adjust the truck size
    truck_height = 100  # Adjust the truck size
    truck_image = pygame.transform.scale(truck_image, (truck_width, truck_height))
except FileNotFoundError:
    print("Error: 'truck.png' not found. Using a red rectangle as a placeholder.")
    truck_width = 60
    truck_height = 100
    truck_image = pygame.Surface((truck_width, truck_height))
    truck_image.fill(RED)  # Red rectangle placeholder

# Fonts for displaying text
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Player (Car) Object
player_x = SCREEN_WIDTH // 2 - car_width // 2
player_y = SCREEN_HEIGHT - car_height - 10
player_rect = pygame.Rect(player_x, player_y, car_width, car_height)

# Obstacle List
obstacles = []

# Movement Flags
move_left = False
move_right = False
move_up = False
move_down = False

# Game Variables
score = 0
player_name = ""
running = True
leaderboard_file = "highscores.txt"

# Ensure the highscores.txt file exists
if not os.path.exists(leaderboard_file):
    with open(leaderboard_file, "w") as file:
        file.write("")  # Create an empty highscores.txt file


def read_leaderboard():
    if not os.path.exists(leaderboard_file):
        return []
    scores = []
    with open(leaderboard_file, "r") as file:
        for line in file:
            try:
                name, score = line.strip().split(",")
                scores.append((name, int(score)))
            except (ValueError, IndexError):
                continue
    return sorted(scores, key=lambda x: x[1], reverse=True)[:5]


def save_score(name, new_score):
    scores = read_leaderboard()
    scores.append((name, new_score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    with open(leaderboard_file, "w") as file:
        for name, score in scores:
            file.write(f"{name},{score}\n")


def spawn_obstacle():
    obs_width = truck_width
    obs_height = truck_height
    obs_y = random.randint(0, SCREEN_HEIGHT - obs_height)
    if random.choice([True, False]):
        obs_x = -obs_width
        direction = 1
    else:
        obs_x = SCREEN_WIDTH
        direction = -1
    obs_speed = random.randint(3, 7) * direction
    return {"x": obs_x, "y": obs_y, "width": obs_width, "height": obs_height, "speed": obs_speed}


def update_player_position():
    global player_rect
    if move_left and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if move_right and player_rect.right < SCREEN_WIDTH:
        player_rect.x += PLAYER_SPEED
    if move_up and player_rect.top > 0:
        player_rect.y -= PLAYER_SPEED
    if move_down and player_rect.bottom < SCREEN_HEIGHT:
        player_rect.y += PLAYER_SPEED


def handle_collision():
    global running
    for obs in obstacles:
        obs_rect = pygame.Rect(obs["x"], obs["y"], obs["width"], obs["height"])
        if player_rect.colliderect(obs_rect):
            pygame.mixer.music.stop()  # Stop music on collision
            print("Collision detected! Game over!")
            running = False  # Stop the game loop


def update_obstacles():
    global obstacles
    for obs in obstacles:
        obs["x"] += obs["speed"]
    obstacles = [obs for obs in obstacles if 0 <= obs["x"] <= SCREEN_WIDTH]


def draw_game_objects():
    screen.fill(BLACK)
    screen.blit(car_image, (player_rect.x, player_rect.y))
    for obs in obstacles:
        screen.blit(truck_image, (obs["x"], obs["y"]))


def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    leaderboard = read_leaderboard()
    y_offset = 50
    for i, (name, high_score) in enumerate(leaderboard, start=1):
        high_score_text = font.render(f"{i}. {name}: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, y_offset))
        y_offset += 30


def display_game_over():
    screen.fill(BLACK)
    game_over_text = large_font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    leaderboard = read_leaderboard()
    y_offset = SCREEN_HEIGHT // 2 + 50
    for i, (name, high_score) in enumerate(leaderboard, start=1):
        high_score_text = font.render(f"{i}. {name}: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, y_offset))
        y_offset += 30
    pygame.display.flip()
    pygame.time.wait(5000)


def input_name_screen():
    global player_name
    screen.fill(BLACK)
    input_text = ""
    prompt = large_font.render("Enter Your Name:", True, WHITE)
    screen.blit(prompt, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    typing = True
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_name = input_text if input_text else "Player"
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill(BLACK)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        entered_name = font.render(input_text, True, WHITE)
        screen.blit(entered_name, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()


def game_loop():
    global move_left, move_right, move_up, move_down, score, obstacles, player_name, running

    try:
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
    except FileNotFoundError:
        print("Error: 'background_music.mp3' not found. No music will be played.")

    obstacles.clear()
    player_rect.x = SCREEN_WIDTH // 2 - car_width // 2
    player_rect.y = SCREEN_HEIGHT - car_height - 10
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False

        update_player_position()

        if random.random() < 0.02:
            obstacles.append(spawn_obstacle())

        update_obstacles()
        handle_collision()

        draw_game_objects()
        display_score()
        pygame.display.flip()
        clock.tick(FPS)

        score += 1

    save_score(player_name, score)
    display_game_over()


# Main Program Execution
if __name__ == "__main__":
    input_name_screen()
    game_loop()
