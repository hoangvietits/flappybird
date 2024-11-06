import pygame as pg
import sys, random
import duckdb

# Khởi tạo DuckDB và tạo bảng lưu điểm
conn = duckdb.connect(database='scores.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS player_scores (
    score FLOAT,
    difficulty VARCHAR
)
""")

def save_score( score, difficulty):
    conn.execute("INSERT INTO player_scores VALUES (?, ?)", ( score, difficulty))

# Hàm vẽ sàn
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# Tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 650))
    bot_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    return bot_pipe, top_pipe

# Di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return pipes

# Vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 384:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pg.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def get_high_score(difficulty):
    result = conn.execute("SELECT MAX(score) FROM player_scores WHERE difficulty = ?", (difficulty,)).fetchone()
    return result[0] if result[0] is not None else 0

# Kiểm tra va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

# Xoay chim
def rotate_bird(bird1):
    new_bird = pg.transform.rotozoom(bird1, -bird_move * 3, 1)
    return new_bird

# Chuyển động của chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

# Hiển thị điểm số
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)

# Cập nhật điểm cao nhất
def update_score(score, high_score):
    if score > high_score:

        high_score = score
    return high_score

# Vẽ nút chọn độ khó
def draw_difficulty_button():
    difficulty_button = pg.Rect(10, 10, 150, 50)
    pg.draw.rect(screen, (0, 0, 255), difficulty_button)
    screen.blit(game_font.render("Diff", True, (255, 255, 255)), (20, 20))
    return difficulty_button

# Hiển thị tùy chọn độ khó
def show_difficulty_options():
    easy_button = pg.Rect(50, 200, 100, 50)
    medium_button = pg.Rect(50, 300, 100, 50)
    hard_button = pg.Rect(50, 400, 100, 50)
    
    pg.draw.rect(screen, (0, 255, 0), easy_button)
    pg.draw.rect(screen, (255, 255, 0), medium_button)
    pg.draw.rect(screen, (255, 0, 0), hard_button)
    
    screen.blit(game_font.render("Easy", True, (0, 0, 0)), (60, 210))
    screen.blit(game_font.render("Medium", True, (0, 0, 0)), (60, 310))
    screen.blit(game_font.render("Hard", True, (0, 0, 0)), (60, 410))
    
    return easy_button, medium_button, hard_button

# Khởi tạo game
pg.init()
screen = pg.display.set_mode((432, 768))
clock = pg.time.Clock()
game_font = pg.font.Font('04B_19.TTF', 40)

# Biến trò chơi
score = 0
difficulty = "Easy"
high_score =  get_high_score(difficulty)

show_difficulty_menu = False

# Các mức độ khó
difficulty_levels = {
    "Easy": {"pipe_speed": 5, "gravity": 0.25},
    "Medium": {"pipe_speed": 6, "gravity": 0.3},
    "Hard": {"pipe_speed": 7, "gravity": 0.35}
}

gravity = difficulty_levels[difficulty]["gravity"]
pipe_speed = difficulty_levels[difficulty]["pipe_speed"]

# Tải tài nguyên
bg = pg.image.load('assets/bg.png').convert_alpha()
bg = pg.transform.scale2x(bg)
floor = pg.image.load('assets/floor.png').convert_alpha()
floor = pg.transform.scale2x(floor)
floor_x_pos = 0

bird_down = pg.transform.scale2x(pg.image.load('assets/bird-down.png').convert_alpha())
bird_mid = pg.transform.scale2x(pg.image.load('assets/bird-mid.png').convert_alpha())
bird_up = pg.transform.scale2x(pg.image.load('assets/bird-up.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))
bird_move = 0

pipe_surface = pg.image.load('assets/pipe.png').convert_alpha()
pipe_surface = pg.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [200, 300, 400]

game_over_surface = pg.transform.scale2x(pg.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

flap_sound = pg.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pg.mixer.Sound('sound/sfx_hit.wav')
score_sound = pg.mixer.Sound('sound/sfx_point.wav')

spawnpipe = pg.USEREVENT
bird_flap = pg.USEREVENT + 1
pg.time.set_timer(spawnpipe, 1200)
pg.time.set_timer(bird_flap, 200)

game_active = True
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            difficulty_button = draw_difficulty_button()

            if show_difficulty_menu:
                easy_button, medium_button, hard_button = show_difficulty_options()
                if easy_button.collidepoint(mouse_pos):
                    difficulty = "Easy"
                    high_score = get_high_score("Easy")
                    show_difficulty_menu = False
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = "Medium"
                    high_score = get_high_score("Medium")
                    show_difficulty_menu = False
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = "Hard"
                    high_score = get_high_score("Hard")
                    show_difficulty_menu = False
                gravity = difficulty_levels[difficulty]["gravity"]
                pipe_speed = difficulty_levels[difficulty]["pipe_speed"]
            else:
                bird_move = -9
                flap_sound.play()
                if not game_active:
                    game_active = True
                    score = 0   
                    pipe_list.clear()
                    bird_move = 0
                    bird_rect.center = (100, 384)

            if difficulty_button.collidepoint(mouse_pos):
                show_difficulty_menu = not show_difficulty_menu

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            bird_index = (bird_index + 1) % 3
            bird, bird_rect = bird_animation()

    # Cập nhật màn hình
    screen.blit(bg, (0, 0))
    if game_active and not show_difficulty_menu:
        bird_move += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_move
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        score += 0.01
        score_display('main game')
    elif not game_active:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        save_score(high_score,difficulty)
        score_display('game over')
        
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    if show_difficulty_menu:
        show_difficulty_options()
    draw_difficulty_button()
    
    pg.display.update()
    clock.tick(120)
