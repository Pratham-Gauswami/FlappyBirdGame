import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flying Bird Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)

# Bird properties
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Pipe properties
PIPE_WIDTH = 70
PIPE_GAP = 200
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(100, 400)

clock = pygame.time.Clock()

# At the top of your file, after pygame.init()
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (40, 40))
pipe_img = pygame.image.load('pipes.png')
bg_img = pygame.image.load('background.png')
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Keep only the sound effects
jump_sound = pygame.mixer.Sound('jump.mp3')
hit_sound = pygame.mixer.Sound('hit.mp3')

def draw_bird(y):
    screen.blit(bird_img, (80, int(y) - 20))

def draw_pipes(x, height):
    # Draw top pipe
    pygame.draw.rect(screen, GREEN, (x, 0, PIPE_WIDTH, height))
    # Draw bottom pipe
    pygame.draw.rect(screen, GREEN, (x, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

def check_collision(bird_y, pipe_x, pipe_height):
    bird_rect = pygame.Rect(80, int(bird_y) - 20, 40, 40)
    top_pipe = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
    
    return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

# Game loop
running = True
game_over = False
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = JUMP_STRENGTH
                jump_sound.play()
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                bird_y = SCREEN_HEIGHT // 2
                bird_velocity = 0
                pipe_x = SCREEN_WIDTH
                score = 0

    if not game_over:
        # Update bird position
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Update pipe position
        pipe_x -= 5
        if pipe_x < -PIPE_WIDTH:
            pipe_x = SCREEN_WIDTH
            pipe_height = random.randint(100, 400)
            score += 1

        # Check collisions
        if (bird_y < 0 or bird_y > SCREEN_HEIGHT or 
            check_collision(bird_y, pipe_x, pipe_height)):
            hit_sound.play()
            game_over = True

    # Draw everything
    screen.fill(SKY_BLUE)
    draw_bird(bird_y)
    draw_pipes(pipe_x, pipe_height)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render('Game Over! Press R to restart', True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit() 