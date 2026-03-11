import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

def restart():
    global grid,colors,current_row,current_col,word,game_over
    
    grid = [["" for _ in range(COLS)] for _ in range(ROWS)]
    colors = [[(30,30,30) for _ in range(COLS)] for _ in range(ROWS)]

    current_row = 0
    current_col = 0
    
    word = random.choice(WORDS)
    
    game_over = False
    

WIDTH = 500
HEIGHT = 700

ROWS = 6
COLS = 5

BOX = 70
GAP = 10
TOP_OFFSET = 150

WORDS = ["MATKA","KOTEK","EKRAN","ROWER","ZEGAR","PILOT","WIDOK","MOTYL","WAGON","MODEL","ZAMEK","GROTA","DROGA","SERIA","RABAT","SKARB"]

word = random.choice(WORDS)

font = pygame.font.SysFont("arial",50,bold=True)

grid = [["" for _ in range(COLS)] for _ in range(ROWS)]
colors = [[(30,30,30) for _ in range(COLS)] for _ in range(ROWS)]

current_row = 0
current_col = 0

anim_row = -1
anim_progress = 0
anim_speed = 0.08

pending_res = None

result_time = None
result_delay = 500

btn_anim = False
btn_scale = 1
btn_speed = 0.1
next_state = None

fade_aplha = 0
fading = False
fade_speed = 15
fade_dir = 1

pop_row = -1
pop_col = -1
pop_scale = 1.12
pop_speed = 0.06

game_over = False

game_state = "menu"

play_sound = None

win_sound = pygame.mixer.Sound("/Users/chleebekk/pygame/sounds/win_sound.wav")
lose_sound = pygame.mixer.Sound("/Users/chleebekk/pygame/sounds/lose_sound.wav")
btn_click_sound = pygame.mixer.Sound("/Users/chleebekk/pygame/sounds/btn_click_sound.wav")

win_sound.set_volume(0.3)
lose_sound.set_volume(0.3)
btn_click_sound.set_volume(0.3)

button_font = pygame.font.SysFont("arial",35,bold=True)

play_button = pygame.Rect(WIDTH//2-100,400,200,70)

res_btn = pygame.Rect(WIDTH//2-100,400,200,70)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("WordGuess")

clock = pygame.time.Clock()

running = True

while running:
    
    clock.tick(60)
    
    if play_button.collidepoint(pygame.mouse.get_pos()) or res_btn.collidepoint(pygame.mouse.get_pos()):
        color = (120,120,120)
    else:
        color = (80,80,80)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
             
            if game_state == "menu":
                if play_button.collidepoint(mouse_pos):
                    btn_anim = True
                    next_state = "playing"
                    btn_click_sound.play()
            elif game_state == "lost":
                if res_btn.collidepoint(mouse_pos):
                    btn_anim = True
                    next_state = "restart"
                    btn_click_sound.play()
            
        if event.type == pygame.KEYDOWN and game_state == "playing" and not game_over:
            
            if event.key == pygame.K_BACKSPACE:
                if current_col > 0:
                    current_col -=1
                    grid[current_row][current_col] = ""
            
            elif event.key == pygame.K_RETURN:
                
                
                
                if current_col == COLS:
                    guess = "".join(grid[current_row])
                    
                    anim_row = current_row
                    anim_progress = 0
                    
                    if guess == word:
                        pending_res = "win"
                        result_time = pygame.time.get_ticks()
                    
                    temp_word = list(word)
                    
                    for i in range(COLS):
                        if guess[i] == word[i]:
                            colors[current_row][i] = (83,141,78)
                            temp_word[i] = None
                    for i in range(COLS):    
                        if colors[current_row][i] == (83,141,78):
                            continue
                        
                        if guess[i] in temp_word:
                            colors[current_row][i] = (181,159,59)
                            temp_word[temp_word.index(guess[i])] = None
                        else:
                            colors[current_row][i] = (58,58,60)
                    
                    if current_row<ROWS-1:
                        current_row+=1
                        current_col = 0
                    else:
                        pending_res = "lose"
                        result_time = pygame.time.get_ticks()
            
            elif pygame.K_a <= event.key <= pygame.K_z:
                if current_col < COLS:
                    letter = chr(event.key).upper()
                    grid[current_row][current_col] = letter
                    
                    pop_row = current_row
                    pop_col = current_col
                    pop_scale = 1.3
                    
                    current_col +=1
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                restart()
            
    screen.fill((30,30,30))
    
    if game_state == "playing":
        
        if anim_row != -1:
            anim_progress += anim_speed
            
            if anim_progress >=1:
                anim_row = -1
        
        if pop_scale > 1:
            pop_scale+=(1-pop_scale)*0.3
            
            if pop_scale <=1:
                pop_scale = 1
                pop_row = -1
                pop_col = -1
                
        if pending_res is not None and anim_row==-1:
            if pygame.time.get_ticks() - result_time > result_delay:
                
                if pending_res == "win":
                    game_state = "lost"
                    game_over = True
                    win_sound.play()
                elif pending_res == "lose":
                            
                    game_state = "lost"
                    game_over = True
                    lose_sound.play()
                        
                pending_res = None
        
        for row in range(ROWS):
            for col in range(COLS):
                
                x = WIDTH//2-(COLS*(BOX+GAP))//2 + col*(BOX+GAP)
                y = TOP_OFFSET + row*(BOX+GAP)
                
                height = BOX
                y_offset = 0
                
                if row == anim_row:
                    scale = abs(1-anim_progress*2)
                    height = BOX * scale
                    y_offset = (BOX - height)/2
                    
                width = BOX
                draw_height = height
                
                if row == pop_row and col == pop_col:
                    width = BOX * pop_scale
                    draw_height = height * pop_scale
                    x-=(width-BOX)/2
                    y-=(draw_height-height)/2
                
                rect = pygame.Rect(x,y + y_offset,width,draw_height)
                
                letter = grid[row][col]
                
                pygame.draw.rect(screen,colors[row][col],rect)
                
                if letter != "":
                    border_color = (120,120,120)
                else:
                    border_color = (40,40,40)
                pygame.draw.rect(screen,border_color,rect,2)
                
                
                
                if letter !="" and height > BOX * 0.5:
                    text = font.render(letter,True,(255,255,255))
                    screen.blit(text,
                                (x+BOX//2 - text.get_width()//2,
                                y+BOX//2 - text.get_height()//2))
                
        
        title = font.render("WORD GUESS",True,(255,255,255))
        screen.blit(title,(WIDTH//2 - title.get_width()//2,40))
        
    if btn_anim:
        btn_scale -= btn_speed
        
        if btn_scale <= 0.8:
            btn_anim = False
            btn_scale = 1
            fading = True
            fade_dir =1
            
                
    if fading:
        fade_aplha += fade_speed * fade_dir
        
        if fade_aplha >=255 and fade_dir == 1:
            
            if next_state == "restart":
                restart()
                game_state = "playing"
            else:
                game_state = next_state
            
            fade_dir = -1
        
        if fade_aplha <= 0 and fade_dir == -1:
            
            fade_aplha = 0
            fading = False
    
        
    if game_state == "menu":
        screen.fill((20,20,20))
        
        title = font.render("WORD GUESS",True,(255,255,255))
        screen.blit(title,(WIDTH//2-title.get_width()//2,200))
        
        scaled_rect = play_button.inflate(
            -play_button.width*(1-btn_scale),
            -play_button.height*(1-btn_scale)
        )
        
        pygame.draw.rect(screen,color,scaled_rect,border_radius=10)
        
        play_text = button_font.render("PLAY",True,(255,255,255))
        screen.blit(play_text,
                    (scaled_rect.x + scaled_rect.width//2 - play_text.get_width()//2,
                    scaled_rect.y + scaled_rect.height//2 - play_text.get_height()//2))
    
    if game_state == "lost":
        screen.fill((20,20,20))
        
        title = font.render("WORD GUESS",True,(255,255,255))
        screen.blit(title,(WIDTH//2-title.get_width()//2,200))
        
        if guess == word:
            message = "YOU WIN"
        else:
            message = f"THE WORD WAS {word}"
        msg_font = pygame.font.SysFont("arial",40,bold=True)
        text = msg_font.render(message,True,(255,255,255))
        
        screen.blit(text,(WIDTH//2-text.get_width()//2,300))
        
        pygame.draw.rect(screen,color,res_btn,border_radius=10)
        
        res_text = button_font.render("RESET",True,(255,255,255))
        screen.blit(res_text,
                    (res_btn.x + res_btn.width//2 - res_text.get_width()//2,
                    res_btn.y + res_btn.height//2 - res_text.get_height()//2))
    
    fade_surface = pygame.Surface((WIDTH,HEIGHT))
    fade_surface.set_alpha(fade_aplha)
    fade_surface.fill((0,0,0))
    screen.blit(fade_surface,(0,0))

    pygame.display.update()
    
pygame.quit()
sys.exit()