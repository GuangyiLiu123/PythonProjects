import pygame
import random

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors (RGB)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 69, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

# Display height
DISPLAY_HEIGHT = HEIGHT + 40  # Extra space for element selection bar

# Cell size
CELL_SIZE = 4  # Each particle is 4x4 pixels

# Grid dimensions
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Particle types
EMPTY = 0
SAND = 1
WATER = 2
DIRT = 3
LAVA = 4
STONE = 5
WALL = 6

grid = [[EMPTY for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Falling Sand Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Cursor size
cursor_size = 1

def draw_grid():
    """Draw the grid based on the particle states."""
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == SAND:
                pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))
            elif grid[x][y] == WATER:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))
            elif grid[x][y] == DIRT:
                pygame.draw.rect(screen, BROWN, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))
            elif grid[x][y] == LAVA:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))
            elif grid[x][y] == STONE:
                pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))
            elif grid[x][y] == WALL:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))

def update_grid():
    """Update the position of each particle."""
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT - 2, -1, -1):  # Start from the second-to-last row
            if grid[x][y] == SAND:  # Sand behavior
                if grid[x][y + 1] == EMPTY:
                    grid[x][y + 1] = SAND
                    grid[x][y] = EMPTY
                elif x > 0 and grid[x - 1][y + 1] == EMPTY:
                    grid[x - 1][y + 1] = SAND
                    grid[x][y] = EMPTY
                elif x < GRID_WIDTH - 1 and grid[x + 1][y + 1] == EMPTY:
                    grid[x + 1][y + 1] = SAND
                    grid[x][y] = EMPTY
                elif grid[x][y + 1] == LAVA:  # Sand melts into lava
                    grid[x][y + 1] = LAVA
                    grid[x][y] = LAVA
            elif grid[x][y] == WATER:  # Water behavior
                if grid[x][y + 1] == EMPTY:
                    grid[x][y + 1] = WATER
                    grid[x][y] = EMPTY
                elif x > 0 and grid[x - 1][y + 1] == EMPTY:
                    grid[x - 1][y + 1] = WATER
                    grid[x][y] = EMPTY
                elif x < GRID_WIDTH - 1 and grid[x + 1][y + 1] == EMPTY:
                    grid[x + 1][y + 1] = WATER
                    grid[x][y] = EMPTY
            elif grid[x][y] == LAVA:  # Lava behavior
                if grid[x][y + 1] == EMPTY:
                    grid[x][y + 1] = LAVA
                    grid[x][y] = EMPTY
                elif x > 0 and grid[x - 1][y + 1] == EMPTY:
                    grid[x - 1][y + 1] = LAVA
                    grid[x][y] = EMPTY
                elif x < GRID_WIDTH - 1 and grid[x + 1][y + 1] == EMPTY:
                    grid[x + 1][y + 1] = LAVA
                    grid[x][y] = EMPTY
                elif grid[x][y + 1] == WATER:
                    grid[x][y + 1] = STONE
                    grid[x][y] = EMPTY
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Spread lava horizontally and vertically
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[nx][ny] == SAND:
                        grid[nx][ny] = LAVA
            elif grid[x][y] == DIRT:  # Dirt behavior
                if grid[x][y + 1] == EMPTY:
                    grid[x][y + 1] = DIRT
                    grid[x][y] = EMPTY

def spawn_particle(mouse_pos, particle_type):
    x, y = mouse_pos
    if y > 40:  # Avoid placing particles in the top bar
        grid_x = x // CELL_SIZE
        grid_y = (y - 40) // CELL_SIZE
        for dx in range(-cursor_size, cursor_size + 1):
            for dy in range(-cursor_size, cursor_size + 1):
                nx, ny = grid_x + dx, grid_y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if particle_type == WALL or grid[nx][ny] == EMPTY:  # Only overwrite empty cells (except WALL)
                        grid[nx][ny] = particle_type

def draw_selection_bar(selected_particle):
    elements = [SAND, WATER, DIRT, LAVA, WALL]
    colors = [YELLOW, BLUE, BROWN, RED, WHITE]
    for i, (element, color) in enumerate(zip(elements, colors)):
        rect = pygame.Rect(i * 80 + 10, 5, 60, 30)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        if selected_particle == element:
            pygame.draw.rect(screen, BLACK, rect, 3)  # Highlight selected element
    reset_button = pygame.Rect(WIDTH - 90, 5, 80, 30)
    pygame.draw.rect(screen, GRAY, reset_button, border_radius=8)
    font = pygame.font.SysFont(None, 24)
    text = font.render('Reset', True, WHITE)
    screen.blit(text, (WIDTH - 75, 10))
    return reset_button

def draw_cursor_indicator(mouse_pos):
    x, y = mouse_pos
    pygame.draw.circle(screen, WHITE, (x, y), cursor_size * CELL_SIZE, 1)

def main():
    global cursor_size
    running = True
    selected_particle = SAND  # Default particle to place
    while running:
        screen.fill(BLACK)  
        reset_button = draw_selection_bar(selected_particle)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    global grid
                    grid = [[EMPTY for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
                else:
                    x, y = event.pos
                    if y < 40:
                        selected_particle = (x // 80) + 1
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    spawn_particle(pygame.mouse.get_pos(), selected_particle)
            elif event.type == pygame.MOUSEWHEEL:
                cursor_size = max(1, cursor_size + event.y)  # Ensure cursor size is at least 1
        update_grid()
        draw_grid()
        draw_cursor_indicator(pygame.mouse.get_pos())
        pygame.display.flip()  
        clock.tick(60)  
    pygame.quit()

if __name__ == "__main__":
    main()
