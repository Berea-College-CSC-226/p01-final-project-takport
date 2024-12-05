import pygame
import random
import sys

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
    car_image.fill((0, 255, 0))  # Green rectangle placeholder

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


# Game Functionality
def game_loop():
    global move_left, move_right, move_up, move_down, obstacles, running

    spawn_timer = 0
    running = True
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

        # Draw everything
        draw_game_objects()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


# Run the game
game_loop()

