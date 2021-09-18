import pygame
import time
import requests
import random
pygame.font.init()

CHEAT = False

r = requests.get('https://raw.githubusercontent.com/ngn13/Astero/main/game/game.py')
with open('game.py', 'r') as f:
    fc = f.read()
    if not fc == r.text:
        CHEAT = True
        

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SHOOTER_IMAGE1 = pygame.image.load('assests/shooter.png')
pygame.display.set_icon(SHOOTER_IMAGE1)
pygame.display.set_caption('Astero / Github - ngn13')

WINNER_FONT = pygame.font.SysFont('comicsans', 100)
CHEATER_FONT = pygame.font.SysFont('comicsans', 50)

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

HEALTH = 100

HIGH_SCORE = 0

SHOTED = 0
FPS = 60

FONT = pygame.font.SysFont('comicsans', 30)

BULLET_MOVE = 1
MAX_BULLETS = 3

BORDER = pygame.Rect(0, HEIGHT-70, WIDTH, 70)

MOVE = 5

HIT = pygame.USEREVENT + 1

SHOOTER = pygame.transform.scale(SHOOTER_IMAGE1, (50, 50))
ROCK_IMAGE = pygame.image.load('assests/rock.png')
ROCK = pygame.transform.scale(ROCK_IMAGE, (20, 20))
BACK_IMAGE = pygame.image.load('assests/back.png')
BACK = pygame.transform.scale(BACK_IMAGE, (WIDTH, HEIGHT))

def openW():
    colrtup = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    WIN.fill(WHITE)
    draw_text = WINNER_FONT.render('Github-ngn13', 1, colrtup)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    time.sleep(2)


def draw(sh, rocks, bullets):    
    WIN.blit(BACK, (0, 0))
    #WIN.fill(BLUE)
    pygame.draw.rect(WIN, (0, 0, 0), BORDER)

    main_text = FONT.render("Shots: " + str(SHOTED), 1, WHITE)
    heal = FONT.render("Health: " + str(HEALTH), 1, WHITE)
    keys = FONT.render("Keys: W,A,S,D,R ", 1, WHITE)
    hs = FONT.render("High Score: " + str(HIGH_SCORE), 1, WHITE)

    WIN.blit(main_text, (WIDTH - main_text.get_width() - 100 , HEIGHT-45))
    WIN.blit(heal, (WIDTH - heal.get_width() - 300 , HEIGHT-45))
    WIN.blit(keys, (WIDTH - keys.get_width() - 450, HEIGHT-45))
    WIN.blit(hs, (WIDTH - hs.get_width() - 700, HEIGHT-45))

    WIN.blit(SHOOTER, (sh.x,sh.y))
    for i in range(0,11):
        WIN.blit(ROCK, (rocks[i].x, rocks[i].y+random.randrange(10,15)))
    for bullet in bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
    pygame.display.update()

def move(key_pressed, sh):
    if key_pressed[pygame.K_a]:
        sh.x -= MOVE
    
    elif key_pressed[pygame.K_r]:
        main()

    elif key_pressed[pygame.K_d]:
        sh.x += MOVE
        
    elif key_pressed[pygame.K_w]:
        sh.y -= MOVE
        
    elif key_pressed[pygame.K_s] and not sh.y > HEIGHT - 120:
        sh.y += MOVE

def cheat():
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False
                    pygame.quit()
        WIN.fill((255, 0, 0))
        draw_text = WINNER_FONT.render('Ops!', 1, WHITE)
        WIN.blit(draw_text, (200,100))
        draw_text2 = CHEATER_FONT.render('Seems like your cheating!', 1, WHITE)
        WIN.blit(draw_text2, (200,200))
        draw_text2 = CHEATER_FONT.render('ERROR: Looser cheater detected', 1, WHITE)
        WIN.blit(draw_text2, (200,270))
        pygame.display.update()

def hs():
    WIN.blit(BACK, (0, 0))
    draw_text = WINNER_FONT.render('High Score: ' + str(HIGH_SCORE), 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    time.sleep(1 / 5)
    WIN.blit(BACK, (0, 0))
    pygame.display.update()
    time.sleep(1 / 5)
    draw_text = WINNER_FONT.render('High Score: ' + str(HIGH_SCORE), 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    time.sleep(1 / 5)
    WIN.blit(BACK, (0, 0))
    pygame.display.update()
    time.sleep(1/ 5)
    draw_text = WINNER_FONT.render('High Score: ' + str(HIGH_SCORE), 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    time.sleep(2)
    main()

def game_over(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    time.sleep(3)
    main()

def check_coll(sh, rock):
    for i in range(0,11):
        if rock[i].colliderect(sh):
            global SHOTED
            global HEALTH
            global HIGH_SCORE
            HEALTH -= 1
            if HEALTH < 1:
                if HIGH_SCORE < SHOTED:
                    HIGH_SCORE = SHOTED
                    SHOTED = 0
                    HEALTH = 100
                    hs()
                else:
                    SHOTED = 0
                    HEALTH = 100
                    r = random.randint(0,1001)
                    if r == 424:
                        game_over("GG!")
                    else:
                        game_over("Game Over!")
                

def first_text():
    draw_text = WINNER_FONT.render('Go!', 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    time.sleep(1)

def handle_bullets(bullets, rocks):
    for i in range(0, 11):
        for bullet in bullets:
            bullet.x += BULLET_MOVE
            if rocks[i].colliderect(bullet):
                bullets.remove(bullet)
                global SHOTED
                SHOTED += 1
            if bullet.x > WIDTH:
                bullets.remove(bullet)


def main():
    rocks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    sh = pygame.Rect(100, 300, 45, 45)
    ROCKX = [600, 700, 750, 520, 620, 800, 500]
    rocks[0] = pygame.Rect(random.choice(ROCKX), 25, 20, 20)
    rocks[1] = pygame.Rect(random.choice(ROCKX), 50, 20, 20)
    rocks[2] = pygame.Rect(random.choice(ROCKX), 30, 20, 20)
    rocks[3] = pygame.Rect(random.choice(ROCKX), 30, 20, 20)
    rocks[4] = pygame.Rect(random.choice(ROCKX), 60, 20, 20)
    rocks[5] = pygame.Rect(random.choice(ROCKX), 100, 20, 20)
    rocks[6] = pygame.Rect(random.choice(ROCKX), 150, 20, 20)
    rocks[7] = pygame.Rect(random.choice(ROCKX), 200, 20, 20)
    rocks[8] = pygame.Rect(random.choice(ROCKX), 250, 20, 20)
    rocks[9] = pygame.Rect(random.choice(ROCKX), 300, 20, 20)
    rocks[9] = pygame.Rect(random.choice(ROCKX), 350, 20, 20)
    rocks[10] = pygame.Rect(random.choice(ROCKX), 370, 20, 20)
    bullets = []
    clock = pygame.time.Clock()
    RUN = True
    first = 1
    if CHEAT:
        cheat()
    while RUN:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(sh.x + sh.width, sh.y + sh.height/2 - 2, 10, 5)
                    bullets.append(bullet)


        #if first == 1:
         #   openW()
          #  first = 2
        key_pressed = pygame.key.get_pressed()
        move(key_pressed,sh)
        #rocks(ROCKX)
        draw(sh, rocks, bullets)

        for i in range(0,11):
            rocks[i].x -= random.randint(7, 15)

        for i in range(0,11):
            if not rocks[i].x > -50:
                rocks[i].x = 1000
                rocks[i].y = random.randint(25,371)
        check_coll(sh, rocks)
        handle_bullets(bullets, rocks)
        if first == 1:
            first_text()
            first = 2
        

if __name__ == "__main__":
    openW()
    main()
