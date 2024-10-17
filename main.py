import pygame as pg
import sys, random

pg.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

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