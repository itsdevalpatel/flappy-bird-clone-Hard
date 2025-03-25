import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
PIPE_WIDTH = 60
GAP_SIZE = 150
GRAVITY = 0.2
FLAP_STRENGTH = -4.5
PIPE_SPEED = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy DFC')

# Load fonts
font = pygame.font.SysFont("Arial", 50)

# Load bird images
bird_images = [
    pygame.transform.scale(pygame.image.load('assets/bird1.png'), (BIRD_WIDTH, BIRD_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/bird2.png'), (BIRD_WIDTH, BIRD_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/bird3.png'), (BIRD_WIDTH, BIRD_HEIGHT))
]

# Load high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# Bird class
class Bird:
    def __init__(self, bird_index):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = bird_images[bird_index]

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(160, SCREEN_HEIGHT - GAP_SIZE - 160)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + GAP_SIZE, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + GAP_SIZE))

        # Load tree images
        self.tree_image = pygame.image.load('assets/tree3.png')

        # Scale images properly
        self.tree_image_top = pygame.transform.scale(self.tree_image, (PIPE_WIDTH, self.height))
        self.tree_image_bottom = pygame.transform.scale(self.tree_image, (PIPE_WIDTH, SCREEN_HEIGHT - (self.height + GAP_SIZE)))

        self.sway_offset = 0  # Offset for sway animation

    def move(self):
        self.x -= PIPE_SPEED

        # Apply a subtle swaying effect
        self.sway_offset = math.sin(pygame.time.get_ticks() * 0.005) * 5  # Adjust 0.005 for speed

        self.top.x = self.x
        self.bottom.x = self.x

    def draw(self):
        # Apply sway to both images
        screen.blit(self.tree_image_top, (self.x + self.sway_offset, 0))  
        screen.blit(self.tree_image_bottom, (self.x - self.sway_offset, self.height + GAP_SIZE))

    def off_screen(self):
        return self.x < -PIPE_WIDTH

# Start screen
def start_screen():
    selected_bird = 0
    while True:
        screen.fill(WHITE)
        title_text = font.render("Select Your Bird", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        for i, img in enumerate(bird_images):
            x = SCREEN_WIDTH // 4 + (i * 100)
            y = 250
            screen.blit(img, (x, y))
            if i == selected_bird:
                pygame.draw.rect(screen, BLACK, (x - 5, y - 5, BIRD_WIDTH + 10, BIRD_HEIGHT + 10), 3)
        
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_bird = (selected_bird - 1) % 3
                if event.key == pygame.K_RIGHT:
                    selected_bird = (selected_bird + 1) % 3
                if event.key == pygame.K_RETURN:
                    return selected_bird
        
        pygame.display.update()

# Main game function
def game():
    bird_index = start_screen()
    bird = Bird(bird_index)
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()

        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.move()

        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        for pipe in pipes:
            if bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
                if bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + GAP_SIZE:
                    game_over = True

        if bird.y >= SCREEN_HEIGHT - BIRD_HEIGHT or bird.y < 0:
            game_over = True
        for pipe in pipes:
            if not hasattr(pipe, 'passed') and bird.x > pipe.x + PIPE_WIDTH:
                pipe.passed = True
                score += 1

        screen.fill(WHITE)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        score_text = font.render(str(score), True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        pygame.display.update()
        clock.tick(60)
    
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))
    
    game()

# Start the game
game()
