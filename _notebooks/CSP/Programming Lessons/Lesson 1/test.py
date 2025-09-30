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
bird = pygame.Rect(50, HEIGHT//2, 30, 30)   # rectangle for bird
gravity = 0.25
bird_movement = 0

pipes = []  
pipe_height_options = [200, 250, 300, 350]  
PIPE_SPEED = 3

score = 0
font = pygame.font.Font(None, 36)

# --- Functions ---
def draw_bird():
    pygame.draw.ellipse(screen, WHITE, bird)

def create_pipe():
    """Create a new pipe at random height and return as a pair (top, bottom)."""
    height = random.choice(pipe_height_options)  # abstraction with list
    bottom_pipe = pygame.Rect(WIDTH, height, 50, HEIGHT - height)
    top_pipe = pygame.Rect(WIDTH, 0, 50, height - 150)  # gap of 150
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    """Move all pipes in the list to the left."""
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
    """Display score using a string (data abstraction)."""
    score_str = f"Score: {score}"
    text = font.render(score_str, True, WHITE)
    screen.blit(text, (10, 10))

def reset_game():
    """Reset bird, pipes, and score (data abstraction in action)."""
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
                bird_movement = -6  # jump up
            if event.key == pygame.K_r and not game_active:
                reset_game()
                game_active = True

        if event.type == pipe_timer and game_active:
            pipes.extend(create_pipe())

    # Background
    screen.fill(BLUE)

    if game_active:
        # Bird
        bird_movement += gravity
        bird.centery += int(bird_movement)
        draw_bird()

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Collision
        if not check_collision(pipes):
            game_active = False

        # Update score
        score += 0.01
        display_score(int(score))
    else:
        # Game over message
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (30, HEIGHT//2))

        # Final score
        display_score(int(score))

    # Update screen
    pygame.display.update()
    clock.tick(60)

 