import pygame
import random

CLOCK = pygame.time.Clock()

COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)
GAME_WIDTH = 800
GAME_HEIGHT = 600

HERO_TANK_SPEED = 10
HERO_MISSILE_SPEED = 12
ENEMY_TANK_SPEED = 6

ENEMY_TANK_NUM = 5


def hero_tank_move(direction):
    global rect
    if direction == 'U':
        if rect.top > 0:
            rect.top -= HERO_TANK_SPEED
    elif direction == 'D':
        if rect.bottom < GAME_HEIGHT:
            rect.top += HERO_TANK_SPEED
    elif direction == 'L':
        if rect.left > 0:
            rect.left -= HERO_TANK_SPEED
    elif direction == 'R':
        if rect.right < GAME_WIDTH:
            rect.left += HERO_TANK_SPEED


def enemy_tank_move(rect, direction,index):
    if direction == 'U':
        if rect.top > 0:
            rect.top -= ENEMY_TANK_SPEED
    elif direction == 'D':
        if rect.bottom < GAME_HEIGHT:
            rect.top += ENEMY_TANK_SPEED
    elif direction == 'L':
        if rect.left > 0:
            rect.left -= ENEMY_TANK_SPEED
    elif direction == 'R':
        if rect.right < GAME_WIDTH:
            rect.left += ENEMY_TANK_SPEED
    if rect.left < 0 or rect.top < 0 or rect.bottom > GAME_HEIGHT or rect.right > GAME_WIDTH:
        enemy_direction[index] = change_direction()
    n = random.randint(1, 100)
    if n < 5:
        enemy_direction[index] = change_direction()

def change_direction():
    n = random.randint(1,4)
    if n == 1:
        return 'U'
    elif n==2:
        return 'D'
    elif n == 3:
        return 'L'
    else:
        return 'R'


def hero_missile_move(rect, direction, index):
    if direction == 'U':
        rect.top -= HERO_MISSILE_SPEED
    elif direction == 'D':
        rect.top += HERO_MISSILE_SPEED
    elif direction == 'L':
        rect.left -= HERO_MISSILE_SPEED
    elif direction == 'R':
        rect.left += HERO_MISSILE_SPEED
    if rect.left < 0 or rect.top < 0 or rect.bottom > GAME_HEIGHT or rect.right > GAME_WIDTH:
        hero_missile_direction.pop(index)
        hero_missile_rect_list.pop(index)

    for m in hero_missile_rect_list:
        for e in enemy_rect_list:
            if pygame.Rect.colliderect(m,e):
                hero_missile_rect_list.remove(m)
                hero_missile_direction.pop(index)
                enemy_rect_list.remove(e)
                enemy_direction.pop(index)


def end_game():
    print("谢谢使用")
    exit()


def get_event():
    global img_tank, tank_dir, rect
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            end_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("发射子弹")
                hero_missile_direction.append(tank_dir)
                m_rect = img_hero_missile.get_rect()
                m_rect.center = rect.center
                hero_missile_rect_list.append(m_rect)

    key_pressed = pygame.key.get_pressed()
    # print(len(key_pressed))
    if key_pressed[pygame.K_UP]:
        print("上")
        tank_dir = 'U'
        img_tank = img_tank_U
        hero_tank_move('U')
    elif key_pressed[pygame.K_DOWN]:
        print("下")
        tank_dir = 'D'
        img_tank = img_tank_D
        hero_tank_move('D')
    elif key_pressed[pygame.K_LEFT]:
        print("左")
        tank_dir = 'L'
        img_tank = img_tank_L
        hero_tank_move('L')
    elif key_pressed[pygame.K_RIGHT]:
        print("右")
        tank_dir = 'R'
        img_tank = img_tank_R
        hero_tank_move('R')


def get_text_surface(text):
    pygame.font.init()
    font = pygame.font.SysFont('kaiti', 18)
    text_surface = font.render(text, True, COLOR_RED)
    return text_surface


pygame.display.init()
pygame.display.set_caption('坦克大战V1.0')
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

img_tank_U = pygame.image.load('tank_img/p1tankU.gif')
img_tank_D = pygame.image.load('tank_img/p1tankD.gif')
img_tank_L = pygame.image.load('tank_img/p1tankL.gif')
img_tank_R = pygame.image.load('tank_img/p1tankR.gif')

img_hero_missile = pygame.image.load('tank_img/tankmissile.gif')
hero_missile_rect_list = []
hero_missile_direction = []

img_tank = img_tank_U
tank_dir = 'U'

rect = img_tank_R.get_rect()
rect.left = 300
rect.top = 400

dict_img_enemy = {'U': pygame.image.load('tank_img/enemy1U.gif'),
                  'D': pygame.image.load('tank_img/enemy1D.gif'),
                  'L': pygame.image.load('tank_img/enemy1L.gif'),
                  'R': pygame.image.load('tank_img/enemy1R.gif')
                  }
enemy_rect = dict_img_enemy['U'].get_rect()
enemy_rect.top = 50
enemy_rect_list = []
enemy_direction = ['U', 'D', 'D', 'R', 'L']

# for i in range(ENEMY_TANK_NUM):
#     temp_rect = enemy_rect
#     temp_rect.left = enemy_rect.left+(i+1) * 30
#     enemy_rect_list.append(temp_rect)

for i in range(ENEMY_TANK_NUM):
    temp_rect = pygame.Rect(enemy_rect.left + (i + 1) * 120, enemy_rect.top, enemy_rect.width, enemy_rect.height)
    enemy_rect_list.append(temp_rect)

while True:
    window.fill(COLOR_BLACK)
    window.blit(img_tank, rect)
    window.blit(get_text_surface("剩余敌方坦克%s辆"%len(enemy_rect_list)), (5, 5))

    i = 0
    for m_rect in hero_missile_rect_list:
        window.blit(img_hero_missile, m_rect)
        hero_missile_move(m_rect, hero_missile_direction[i], i)
        i = i + 1

    i = 0
    for e_rect in enemy_rect_list:
        window.blit(dict_img_enemy[enemy_direction[i]], e_rect)
        enemy_tank_move(e_rect, enemy_direction[i],i)
        i = i + 1

    get_event()
    pygame.display.update()
    CLOCK.tick(30)
