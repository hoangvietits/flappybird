import pygame as pg
import sys, random

pg.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
#game function
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-650))

    bot_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    return bot_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=384:        
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pg.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
    
def rotate_bird(bird1):
    new_bird = pg.transform.rotozoom(bird1,-bird_move*3,1)
    return new_bird

def bird_animation():

    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface= game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface= game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(216,630))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pg.init()
#game parameter
screen = pg.display.set_mode((432,768))
clock = pg.time.Clock()
game_font = pg.font.Font('04B_19.TTF',40)
gravity = 0.25
score = 0
high_score = 0
#background + floor 
bg = pg.image.load('assests/bg.png').convert_alpha()
bg = pg.transform.scale2x(bg)
floor = pg.image.load('assests/floor.png').convert_alpha()
floor = pg.transform.scale2x(floor)
floor_x_pos = 0
#bird
bird_down = pg.transform.scale2x(pg.image.load('assests/bird-down.png').convert_alpha())
bird_mid = pg.transform.scale2x(pg.image.load('assests/bird-mid.png').convert_alpha())
bird_up = pg.transform.scale2x(pg.image.load('assests/bird-up.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up]
bird_index =0
bird = bird_list[bird_index]
# bird = pg.image.load('assests/bird-mid.png').convert_alpha()
# bird = pg.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100,384))
bird_move = 0
#pipe
pipe_surface = pg.image.load('assests/pipe.png').convert_alpha()
pipe_surface = pg.transform.scale2x(pipe_surface)
pipe_list =[]
#timer

spawnpipe = pg.USEREVENT
bird_flap =  pg.USEREVENT+1
pg.time.set_timer(spawnpipe,1200)
pg.time.set_timer(bird_flap,200)
pipe_height = [200,300,400]
game_active = True
#end screen
game_over_surface = pg.transform.scale2x(pg.image.load('assests/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
#sound
flap_sound = pg.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pg.mixer.Sound('sound/sfx_hit.wav')
score_sound = pg.mixer.Sound('sound/sfx_point.wav')
countdown = 100