import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

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
    """
    Read the leaderboard from a file and return the top 5 scores with names as a list of tuples.
    Handles empty or malformed lines gracefully.
    """
    if not os.path.exists(leaderboard_file):
        return []  # Return an empty leaderboard if the file doesn't exist

    scores = []
    with open(leaderboard_file, "r") as file:
        for line in file:
            try:
                name, score = line.strip().split(",")  # Split the line into name and score
                scores.append((name, int(score)))      # Convert score to integer
            except (ValueError, IndexError):
                # Skip lines that are not properly formatted
                continue

    return sorted(scores, key=lambda x: x[1], reverse=True)[:5]


def save_score(name, new_score):
    """
    Save a new score with the player's name to the leaderboard file.
    """
    scores = read_leaderboard()
    scores.append((name, new_score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]  # Keep only the top 5 scores
    with open(leaderboard_file, "w") as file:
        for name, score in scores:
            file.write(f"{name},{score}\n")


def spawn_obstacle():
    """
    Spawn a new obstacle. Randomly decides the side (left or right)
    and returns its position, size, and speed.
    """
    obs_width = random.randint(20, 50)
    obs_height = random.randint(20, 50)
    obs_y = random.randint(0, SCREEN_HEIGHT - obs_height)
    if random.choice([True, False]):  # Randomly choose the side
        obs_x = -obs_width  # Spawn off-screen on the left
        direction = 1       # Move right
    else:
        obs_x = SCREEN_WIDTH  # Spawn off-screen on the right
        direction = -1       # Move left
    obs_speed = random.randint(3, 7) * direction
    return {"x": obs_x, "y": obs_y, "width": obs_width, "height": obs_height, "speed": obs_speed}


def update_player_position():
    """
    Update the player's position based on movement flags.
    """
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
    """
    Check for collisions between the player and obstacles, and handle
    the game state accordingly.
    """
    global running
    for obs in obstacles:
        obs_rect = pygame.Rect(obs["x"], obs["y"], obs["width"], obs["height"])
        if player_rect.colliderect(obs_rect):
            print("Collision detected! Game over!")
            running = False


def update_obstacles():
    """
    Move obstacles sideways and remove any that are off-screen.
    """
    global obstacles
    for obs in obstacles:
        obs["x"] += obs["speed"]  # Move obstacle
    obstacles = [obs for obs in obstacles if 0 <= obs["x"] <= SCREEN_WIDTH]  # Remove off-screen obstacles


def draw_game_objects():
    """
    Draw the player and obstacles on the screen.
    """
    screen.fill(BLACK)  # Clear the screen
    screen.blit(car_image, (player_rect.x, player_rect.y))  # Draw player
    for obs in obstacles:  # Draw all obstacles
        pygame.draw.rect(screen, RED, (obs["x"], obs["y"], obs["width"], obs["height"]))


def display_score():
    """
    Display the current score and leaderboard on the screen.
    """
    # Display the current score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display the leaderboard
    leaderboard = read_leaderboard()
    y_offset = 50
    for i, (name, high_score) in enumerate(leaderboard, start=1):
        high_score_text = font.render(f"{i}. {name}: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, y_offset))
        y_offset += 30


def display_name_input():
    """
    Display a text input box for the user to enter their name.
    """
    global player_name

    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
    active = True
    color = GRAY

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        # Draw input box and name
        screen.fill(BLACK)
        pygame.draw.rect(screen, color, input_box)
        text_surface = font.render(player_name, True, WHITE)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        prompt = font.render("Enter your name and press Enter:", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 80))

        pygame.display.flip()
        clock.tick(FPS)


def display_game_over():
    """
    Display a game-over message and leaderboard.
    """
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
    pygame.time.wait(5000)  # Wait 5 seconds before exiting


# Game Functionality
def game_loop():
    global move_left, move_right, move_up, move_down, obstacles, running, score

    spawn_timer = 0
    running = True
    score = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True

            # Handle key release events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False

        # Update game state
        update_player_position()

        # Spawn obstacles periodically
        spawn_timer += 1
        if spawn_timer > 30:  # Adjust spawn rate
            obstacles.append(spawn_obstacle())
            spawn_timer = 0

        update_obstacles()
        handle_collision()

        # Increase score over time
        score += 1

        # Draw everything
        draw_game_objects()
        display_score()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Save the score and display a game-over screen
    save_score(player_name, score)
    display_game_over()


# Run the game
display_name_input()
game_loop()
