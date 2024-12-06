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


# Stubbed Functions
def spawn_obstacle():
    """
    Spawn a new obstacle. Randomly decides the side (left or right)
    and returns its position, size, and speed.
    """
    pass


def update_player_position():
    """
    Update the player's position based on movement flags.
    """
    pass


def handle_collision():
    """
    Check for collisions between the player and obstacles, and handle
    the game state accordingly.
    """
    pass


def update_obstacles():
    """
    Move obstacles sideways and remove any that are off-screen.
    """
    pass


def draw_game_objects():
    """
    Draw the player and obstacles on the screen.
    """
    pass


# Game Functionality
def game_loop():
    global player_rect, obstacles

    spawn_timer = 0
    running = True
    while running:
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

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 30:
            # Placeholder: Replace with actual spawn_obstacle logic
            obstacles.append({
                "x": random.choice([-50, SCREEN_WIDTH + 50]),
                "y": random.randint(0, SCREEN_HEIGHT - 50),
                "width": random.randint(20, 50),
                "height": random.randint(20, 50),
                "speed": random.randint(3, 7) * (-1 if random.choice([True, False]) else 1),
            })
            spawn_timer = 0

        # Move and remove obstacles
        for obs in obstacles:
            obs["x"] += obs["speed"]
        obstacles = [obs for obs in obstacles if 0 <= obs["x"] <= SCREEN_WIDTH]

        # Clear the screen
        screen.fill(BLACK)

        # Draw player
        screen.blit(car_image, (player_rect.x, player_rect.y))

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, RED, (obs["x"], obs["y"], obs["width"], obs["height"]))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


# Run the game
game_loop()
