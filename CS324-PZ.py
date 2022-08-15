import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 540))
    screen.blit(floor_surface, (floor_x_pos + 376, 540))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (400, random_pipe_pos - 170))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 624:
           screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes: 
       if bird_rect.colliderect(pipe):
          return False
    
    if bird_rect.top <= -50 or bird_rect.bottom >= 540:
        return False
    
    return True

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (190, 60))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (190, 60))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (190, 500))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((376, 624))
clock = pygame.time.Clock()
game_font = pygame.font.Font('C:/Users/Dell/Desktop/flappy/04B_19.ttf', 25)

# Game Variables
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0

# background
bg_surface = pygame.image.load('C:/Users/Dell/Desktop/flappy/assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (376, 624))

# floor
floor_surface = pygame.image.load('C:/Users/Dell/Desktop/flappy/assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (376, 100))
floor_x_pos = 0

# bird
bird_surface = pygame.image.load('C:/Users/Dell/Desktop/flappy/assets/yellowbird-midflap.png').convert()
bird_surface = pygame.transform.scale(bird_surface, (40,28))
bird_rect = bird_surface.get_rect(center = (60, 290))

# pipe
pipe_surface = pygame.image.load('C:/Users/Dell/Desktop/flappy/assets/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface, (65, 400))
pipe_list = []

SPAWNPIPE = pygame.USEREVENT 
pygame.time.set_timer(SPAWNPIPE, 1600)
pipe_height = [270, 370, 350, 300, 400]

game_over_surface = pygame.image.load('C:/Users/Dell/Desktop/flappy/assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (190,270))

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE and game_active:
               bird_movement = 0
               bird_movement -= 5
           if event.key == pygame.K_SPACE and game_active == False:
               game_active = True
               score = 0
               pipe_list.clear()
               bird_movement = 0
               bird_rect.center = (60, 290)
               
       if event.type == SPAWNPIPE:
           pipe_list.extend(create_pipe())
           
# dodavanje pozadine na ekran
    screen.blit(bg_surface, (0,0))

    if game_active:
       # dodavanje ptice na ekran i njeno pomeranje gore-dole
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

       # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        for pipe in pipe_list:
            if pipe.centerx==60:
                score+=0.5

       
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

# dodavanje poda na ekran
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -376:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
