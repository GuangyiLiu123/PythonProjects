import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors (RGB format)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Create screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and icon
pygame.display.set_caption("Bouncing Ball Animation")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Ball attributes
ball_radius = 20
ball_x = random.randint(ball_radius, WIDTH - ball_radius)
ball_y = random.randint(ball_radius, HEIGHT - ball_radius)
ball_dx = 5  # X-axis velocity
ball_dy = 5  # Y-axis velocity
ball_color = random.choice([RED, BLUE, GREEN])

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx = -ball_dx
        ball_color = random.choice([RED, BLUE, GREEN])  # Change color on bounce
    
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_dy = -ball_dy
        ball_color = random.choice([RED, BLUE, GREEN])  # Change color on bounce
    
    # Draw everything
    screen.fill(WHITE)  # Clear screen
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)  # Draw ball
    
    # Update display
    pygame.display.flip()
    
    # Cap frame rate
    clock.tick(60)  # 60 frames per second

# Quit Pygame
pygame.quit()
