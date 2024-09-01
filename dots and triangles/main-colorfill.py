import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
ROWS, COLS = 10, 12
DOT_RADIUS = 5
LINE_WIDTH = 2
COLORS = [(0, 102, 255), (255, 51, 51)]  # Vibrant Blue, Vibrant Red
MAX_LINE_LENGTH = 80
PADDING = 50
EXTRA_HEIGHT = 100  # Message Height
NEON_LEMON = (206, 255, 20)
VIBRANT_YELLOW = (255, 255, 0)  # New color for nearby dots

icon = pygame.image.load('./logo.png')  # Logo
pygame.display.set_icon(icon)

# Calculate dot positions
dots = []
for row in range(ROWS):
    for col in range(COLS):
        x = col * (MAX_LINE_LENGTH) + PADDING + (MAX_LINE_LENGTH // 2 if row % 2 else 0)
        y = row * (MAX_LINE_LENGTH * math.sqrt(3) / 2) + PADDING
        dots.append((x, y))

# Calculate window size based on the dots positions
WIDTH = max(x for x, y in dots) + PADDING
HEIGHT = max(y for x, y in dots) + PADDING + EXTRA_HEIGHT

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Triangles")

# Game state
lines = []
line_colors = []
triangles = []
triangle_colors = []
current_player = 0
scores = [0, 0]
congratulation_message = ""
congratulation_timer = 0
game_over = False

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_closest_dot(pos):
    return min(dots, key=lambda dot: distance(dot, pos))

def get_nearby_dots(dot):
    return [d for d in dots if 0 < distance(dot, d) <= MAX_LINE_LENGTH * 1.1]

def check_triangles(last_line):
    new_triangles = []
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines[i+1:], i+1):
            if last_line != line1 and last_line != line2:
                points = set(line1 + line2 + last_line)
                if len(points) == 3:
                    triangle = tuple(sorted(points))
                    if triangle not in triangles:
                        new_triangles.append(triangle)
    return new_triangles

def is_valid_line(start, end):
    if start == end:
        return False
    new_line = tuple(sorted([start, end]))
    if new_line in lines:
        return False
    if distance(start, end) > MAX_LINE_LENGTH * 1.1:
        return False
    return True

def draw_x_mark(screen, center, color, size=10):
    x, y = center
    thickness = 3
    pygame.draw.line(screen, color, (x - size//2, y - size//2), (x + size//2, y + size//2), thickness)
    pygame.draw.line(screen, color, (x - size//2, y + size//2), (x + size//2, y - size//2), thickness)


def lighten_color(color, factor=0.5):
    return tuple(min(255, int(c + (255 - c) * factor)) for c in color)

def update_congratulation_message():
    global congratulation_message, congratulation_timer, game_over
    if len(triangles) == max_possible_triangles:
        game_over = True
        if scores[0] > scores[1]:
            congratulation_message = "Blue wins! Congratulations!"
        elif scores[1] > scores[0]:
            congratulation_message = "Red wins! Congratulations!"
        else:
            congratulation_message = "It's a tie! Well played!"
        congratulation_timer = 300
    else:
        if scores[0] > scores[1]:
            congratulation_message = "Congratulations Blue! You're in the lead!"
        elif scores[1] > scores[0]:
            congratulation_message = "Congratulations Red! You're in the lead!"
        else:
            congratulation_message = "It's a tie! The game is heating up!"
        congratulation_timer = 180  # Show message for 3 seconds (60 frames per second)

# Precompute maximum possible triangles
max_possible_triangles = 0
for i, dot1 in enumerate(dots):
    for j, dot2 in enumerate(dots[i+1:], i+1):
        for k, dot3 in enumerate(dots[j+1:], j+1):
            if distance(dot1, dot2) <= MAX_LINE_LENGTH * 1.1 and distance(dot2, dot3) <= MAX_LINE_LENGTH * 1.1 and distance(dot1, dot3) <= MAX_LINE_LENGTH * 1.1:
                max_possible_triangles += 1

# Main game loop
running = True
selected_dot = None
nearby_dots = []
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            closest_dot = find_closest_dot(pos)
            if selected_dot is None:
                selected_dot = closest_dot
                nearby_dots = get_nearby_dots(selected_dot)
            elif closest_dot in nearby_dots:
                if is_valid_line(selected_dot, closest_dot):
                    new_line = tuple(sorted([selected_dot, closest_dot]))
                    lines.append(new_line)
                    line_colors.append(COLORS[current_player])
                    new_triangles = check_triangles(new_line)
                    if new_triangles:
                        triangles.extend(new_triangles)
                        triangle_colors.extend([COLORS[current_player]] * len(new_triangles))
                        scores[current_player] += len(new_triangles)
                        update_congratulation_message()
                    else:
                        current_player = 1 - current_player
                selected_dot = None
                nearby_dots = []
            else:
                selected_dot = closest_dot
                nearby_dots = get_nearby_dots(selected_dot)

    # Draw
    screen.fill((0, 0, 0))  # Black background

    # Draw triangles
    for triangle, color in zip(triangles, triangle_colors):
        light_color = lighten_color(color)
        pygame.draw.polygon(screen, light_color, triangle)
        pygame.draw.polygon(screen, color, triangle, 2)  # Draw outline
        center = tuple(map(lambda x: sum(x) / 3, zip(*triangle)))
        draw_x_mark(screen, center, color, size=10)

    # Draw lines
    for line, color in zip(lines, line_colors):
        pygame.draw.line(screen, color, line[0], line[1], LINE_WIDTH)

    # Draw dots
    for dot in dots:
        if dot in nearby_dots:
            pygame.draw.circle(screen, (255, 255, 255), dot, DOT_RADIUS * 1.5)  # White for selected
        else:
            pygame.draw.circle(screen, (255, 255, 255), dot, DOT_RADIUS)  # White for normal dots

    # Draw selected dot
    if selected_dot:
        pygame.draw.circle(screen, COLORS[current_player], selected_dot, DOT_RADIUS * 2)

    # Draw scores
    font = pygame.font.Font(None, 36)
    blue_score = font.render(f"Blue: {scores[0]}", True, (255, 255, 255))
    red_score = font.render(f"Red: {scores[1]}", True, (255, 255, 255))
    screen.blit(blue_score, (10, 10))
    screen.blit(red_score, (WIDTH - 110, 10))

    # Draw current player indicator
    pygame.draw.circle(screen, COLORS[current_player], (WIDTH // 2, 20), 10)

    # Draw congratulation message
    if congratulation_timer > 0:
        congrat_font = pygame.font.Font(None, 48)
        congrat_text = congrat_font.render(congratulation_message, True, (255, 255, 255))
        text_rect = congrat_text.get_rect(center=(WIDTH // 2, HEIGHT - EXTRA_HEIGHT // 2))
        
        # Draw a neon lemon border for the message
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, NEON_LEMON, bg_rect, 2)
        
        screen.blit(congrat_text, text_rect)
        congratulation_timer -= 1

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
sys.exit()
