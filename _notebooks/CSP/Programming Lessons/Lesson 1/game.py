import pygame, sys, random

# --- Initialize pygame ---
pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Data Abstraction")
clock = pygame.time.Clock()

# --- Colors ---
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)

# --- Game Variables ---
bird = pygame.Rect(50, HEIGHT//2, 30, 30)
gravity = 0.25
bird_movement = 0

pipes = []
pipe_height_options = [200, 250, 300, 350]
PIPE_SPEED = 3

score = 0
font = pygame.font.Font(None, 36)

def draw_bird():
    pygame.draw.ellipse(screen, WHITE, bird)

def create_pipe():
    height = random.choice(pipe_height_options)
    bottom_pipe = pygame.Rect(WIDTH, height, 50, HEIGHT - height)
    top_pipe = pygame.Rect(WIDTH, 0, 50, height - 150)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_SPEED
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return False
    if bird.top <= -50 or bird.bottom >= HEIGHT:
        return False
    return True

def display_score(score):
    score_str = f"Score: {score}"
    text = font.render(score_str, True, WHITE)
    screen.blit(text, (10, 10))

def reset_game():
    global bird, bird_movement, pipes, score
    bird = pygame.Rect(50, HEIGHT//2, 30, 30)
    bird_movement = 0
    pipes = []
    score = 0

# --- Main Game Loop ---
pipe_timer = pygame.USEREVENT
pygame.time.set_timer(pipe_timer, 1500)

running = True
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -6
            if event.key == pygame.K_r and not game_active:
                reset_game()
                game_active = True

        if event.type == pipe_timer and game_active:
            pipes.extend(create_pipe())

    screen.fill(BLUE)

    if game_active:
        bird_movement += gravity
        bird.centery += int(bird_movement)
        draw_bird()
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        if not check_collision(pipes):
            game_active = False

        score += 0.01
        display_score(int(score))
    else:
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (30, HEIGHT//2))
        display_score(int(score))

    pygame.display.update()
    clock.tick(60)
