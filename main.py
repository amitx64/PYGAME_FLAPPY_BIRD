import pygame
import sys
import random

##########################################
#       INITIALIZE pygame                #
##########################################
pygame.init()

# Frame per Second time clock initialize
FPS = pygame.time.Clock()
fpsVar = 100
# Create font
game_font = pygame.font.Font('04B_19.TTF', 30)

#########################################
#    Global Variables for the game      #
#########################################
game_active = True
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
# pygame.display.set_mode : It initialize a window or screen for display
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Flappy Bird")
# initialize icon
ICON = pygame.image.load('gallery/sprites/bird.png')
# display icon
pygame.display.set_icon(ICON)

# Background
BACKGROUND = pygame.image.load('gallery/sprites/background.png').convert_alpha()
BACKGROUNDX = 0
BACKGROUNDY = 0
BACKGROUND_FLAG = True


# Function blit Background
def background():
    SCREEN.blit(BACKGROUND, (BACKGROUNDX, BACKGROUNDY))


# Base
BASE = pygame.image.load('gallery/sprites/base.png').convert_alpha()
BASE_X = 0
BASE_Y = SCREEN_HEIGHT * 0.8
BASE_FLAG = True


# function to blit BASE on 20% of the screen on bottom
def base():
    SCREEN.blit(BASE, (BASE_X, BASE_Y))


# DRAW BACKGROUND method
def draw_background():
    SCREEN.blit(BACKGROUND, (BACKGROUNDX, BACKGROUNDY))
    SCREEN.blit(BACKGROUND, (BACKGROUNDX + 289, BACKGROUNDY))


# DRAW BASE (or DRAW_FLOOR) method
def draw_base():
    SCREEN.blit(BASE, (BASE_X, BASE_Y))
    SCREEN.blit(BASE, (BASE_X + 289, BASE_Y))


# Message
MESSAGE = pygame.image.load('gallery/sprites/message.png').convert_alpha()
MESSAGE_X = SCREEN_WIDTH / 2
MESSAGE_Y = SCREEN_HEIGHT / 2
MESSAGE_FLAG = True


# Function to blit message on welcome screen
def message():
    SCREEN.blit(MESSAGE, MESSAGE.get_rect(center=(MESSAGE_X, MESSAGE_Y)))


# #BIRD SURFACE
# BIRD_SURFACE = pygame.image.load('gallery/sprites/bird.png').convert_alpha()
# #put BIRD inside a RECTANGLE
# BIRD_RECT = BIRD_SURFACE.get_rect(center = (80,SCREEN_HEIGHT/2))
BIRD_FLAG = False
# BIRD ANIMATION EFFECT
BIRD_DOWNFLAP = pygame.image.load('gallery/sprites/bird-downflap.png').convert_alpha()
BIRD_MIDFLAP = pygame.image.load('gallery/sprites/bird.png').convert_alpha()
BIRD_UPFLAP = pygame.image.load('gallery/sprites/bird-upflap.png').convert_alpha()
BIRD_FRAME = [BIRD_DOWNFLAP, BIRD_MIDFLAP, BIRD_UPFLAP]
BIRD_INDEX = 0
BIRD_SURFACE = BIRD_FRAME[BIRD_INDEX]
BIRD_RECT = BIRD_SURFACE.get_rect(center=(80, SCREEN_HEIGHT / 2))
# TIMER set for to blit images of bird that creates illusion of flapping wing
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)


# function for BIRD animation
def bird_animation():
    new_bird = BIRD_FRAME[BIRD_INDEX]
    new_bird_rect = new_bird.get_rect(center=(80, BIRD_RECT.centery))
    return new_bird, new_bird_rect


# BIRD MOVEMENT PARAMETERS
gravity = 0.17
bird_movement = 0


# BIRD REACTION MOVEMENT through rotatation
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * (-3.5), 1)
    return new_bird


# PIPES
PIPE_SURFACE = pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
PIPE_LIST = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
# PIPE shows when player starts moving
SPAWNPIPE_FLAG = False
# PIPE height used fo1r random height generation between some range
PIPE_HEIGHT = []


# Random Height generation of PIPE
def ran_height():
    ran_h = random.randint(150, 380)
    return ran_h


# Function to create PIPES
def create_pipe():
    random_pipe_pos = random.choice(PIPE_HEIGHT)
    bottom_pipe = PIPE_SURFACE.get_rect(midtop=(295, random_pipe_pos))
    top_pipe = PIPE_SURFACE.get_rect(midbottom=(295, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


# Function to move PIPES
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 380:
            SCREEN.blit(PIPE_SURFACE, pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPE_SURFACE, False, True)
            SCREEN.blit(flip_pipe, pipe)


# Function to CHECK COLLISION between BIRD and PIPES
def check_collision(pipes):
    for pipe in pipes:
        if BIRD_RECT.colliderect(pipe):
            # for debugging purpose
            # print('collide')
            SPAWNPIPE_FLAG = False
            # collide sound
            hit_sound.play()
            die_sound.play()
            return False
    if BIRD_RECT.top <= 0 or BIRD_RECT.bottom >= BASE_Y - 10:
        # for debugging purpose
        # print('collide')
        SPAWNPIPE_FLAG = False
        # collide sound
        hit_sound.play()
        die_sound.play()
        return False

    return True


# Variable to Score
SCORE = 0
HIGH_SCORE = 0


# function display score
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(SCORE)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 60))
        SCREEN.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(SCORE)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 60))
        SCREEN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(HIGH_SCORE)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(144, 380))
        SCREEN.blit(high_score_surface, high_score_rect)


# Function to update score
def update_score(SCORE, HIGH_SCORE):
    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
    return HIGH_SCORE


# SOUND EFFECT
flap_sound = pygame.mixer.Sound('gallery/audio/wing.wav')
hit_sound = pygame.mixer.Sound('gallery/audio/hit.wav')
die_sound = pygame.mixer.Sound('gallery/audio/die.wav')
swoosh_sound = pygame.mixer.Sound('gallery/audio/swoosh.wav')
score_sound = pygame.mixer.Sound('gallery/audio/point.wav')
score_sound_counter = 100


##########################################
#           WELCOME SCREEN               #
##########################################
def welcomeScreen():
    # background() : this method blit background image
    if BACKGROUND_FLAG == True:
        background()
    # base() : this method blit base image
    if BASE_FLAG == True:
        base()
    # When Message_Flag is False then message disappear
    if MESSAGE_FLAG == True:
        # message() : this method blit message image
        message()


#############################################
#        MAIN point to start the game       #
#############################################
if __name__ == "__main__":

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    MESSAGE_FLAG = False
                    BIRD_FLAG = True
                    BACKGROUND_FLAG = False
                    BASE_FLAG = False
                    # BIRD move up when space or up key press
                    bird_movement = 0
                    bird_movement -= 4
                    # PIPE shows when player starts moving
                    SPAWNPIPE_FLAG = True
                    # BIRD WINGS FLAP SOUND
                    flap_sound.play()
                    swoosh_sound.play()
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active == False:
                    game_active = True
                    PIPE_LIST.clear()
                    BIRD_RECT.center = (80, SCREEN_HEIGHT / 2)
                    SPAWNPIPE_FLAG = True
                    SCORE = 0

            if event.type == SPAWNPIPE and SPAWNPIPE_FLAG == True:
                # print("AMIT")
                PIPE_LIST.extend(create_pipe())
                # print(PIPE_LIST)

            if event.type == BIRD_FLAP:
                if BIRD_INDEX < 2:
                    BIRD_INDEX += 1
                else:
                    BIRD_INDEX = 0
                BIRD_SURFACE, BIRD_RECT = bird_animation()

        if game_active:
            # Show Starting Screen
            welcomeScreen()
            # Random Height of PIPE store in a list PIPE_HEIGHT
            PIPE_HEIGHT.append(ran_height())
            # BACKGROUND ,BASE and PIPES blit and move when game starts
            if BACKGROUND_FLAG == False and BASE_FLAG == False:
                # background running when game start
                BACKGROUNDX -= 1
                draw_background()
                if BACKGROUNDX <= -289:
                    BACKGROUNDX = 0
                # shows PIPES and MOVEMENT of PIPES
                PIPE_LIST = move_pipes(PIPE_LIST)
                draw_pipes(PIPE_LIST)
                # BASE running when game start
                BASE_X -= 1
                draw_base()
                if BASE_X <= -289:
                    BASE_X = 0
                # Display Score
                SCORE += 0.01
                score_display('main_game')
                score_sound_counter -= 1
                if score_sound_counter <= 0:
                    score_sound.play()
                    score_sound_counter = 100

                    # blit BIRD IMAGE when BIRD_FLAG is TRUE
            if BIRD_FLAG == True and MESSAGE_FLAG == False and BACKGROUND_FLAG == False:
                # BIRD MOVEMENT
                # BIRD move down continously
                bird_movement += gravity
                rotated_bird = rotate_bird(BIRD_SURFACE)
                BIRD_RECT.centery += bird_movement
                # SIMPLE BIRD BLIT
                # SCREEN.blit(BIRD_SURFACE,BIRD_RECT)
                # Reactive BIRD BLIT
                SCREEN.blit(rotated_bird, BIRD_RECT)
                game_active = check_collision(PIPE_LIST)
        else:
            HIGH_SCORE = update_score(SCORE, HIGH_SCORE)
            score_display('game_over')

        pygame.display.update()
        FPS.tick(fpsVar)
