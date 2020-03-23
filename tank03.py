import pygame

clock = pygame.time.Clock()
COLOR_BLACK = pygame.color.Color(0, 0, 0)
SPEED_HERO_TANK = 10
SPEED_MISSILE_TANK = 13
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def hero_missile_move(rect, direction, index):
    if direction == 'U':
        rect.top -= SPEED_MISSILE_TANK
    elif direction == 'D':
        rect.top += SPEED_MISSILE_TANK
    elif direction == 'L':
        rect.left -= SPEED_MISSILE_TANK
    elif direction == 'R':
        rect.left += SPEED_MISSILE_TANK
    if rect.left <= 0 or rect.right >= WINDOW_WIDTH or rect.top <= 0 or rect.bottom >= WINDOW_HEIGHT:
        hero_tank_missile_list.pop(index)
        hero_tank_missile_dir_list.pop(index)


def hero_tank_move(direction):
    if direction == 'U':
        if rect.top > 0:
            rect.top -= SPEED_HERO_TANK
    elif direction == 'D':
        if rect.bottom < WINDOW_HEIGHT:
            rect.top += SPEED_HERO_TANK
    elif direction == 'L':
        if rect.left > 0:
            rect.left -= SPEED_HERO_TANK
    elif direction == 'R':
        if rect.right < WINDOW_WIDTH:
            rect.left += SPEED_HERO_TANK


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('坦克大战')

# 英雄坦克
img_tank_U = pygame.image.load('img/p1tankU.gif')
img_tank_D = pygame.image.load('img/p1tankD.gif')
img_tank_L = pygame.image.load('img/p1tankL.gif')
img_tank_R = pygame.image.load('img/p1tankR.gif')
rect = img_tank_U.get_rect()
rect.left = 300
rect.top = 200
hero_tank_direction = 'U'
img_tank = img_tank_U

# 英雄坦克的子弹
img_hero_tank_missile = pygame.image.load('img/tankmissile.gif')
hero_tank_missile_list = []
hero_tank_missile_dir_list = []
hero_tank_missile_rect = img_hero_tank_missile.get_rect()


while True:

    window.fill(COLOR_BLACK)

    window.blit(img_tank, rect)
	
    i = 0
    for hero_tank_missile in hero_tank_missile_list:
        window.blit(img_hero_tank_missile, hero_tank_missile)
        hero_missile_move(hero_tank_missile, hero_tank_missile_dir_list[i], i)
        i += 1

    pygame.display.update()

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            print('谢谢使用')
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('发射子弹')
                m_rect = pygame.rect.Rect(hero_tank_missile_rect)
                m_rect.center = rect.center
                hero_tank_missile_list.append(m_rect)
                hero_tank_missile_dir_list.append(hero_tank_direction)


    keypressed = pygame.key.get_pressed()
    if keypressed[pygame.K_UP]:
        print('上')
        img_tank = img_tank_U
        hero_tank_move('U')
        hero_tank_direction = 'U'
    elif keypressed[pygame.K_DOWN]:
        print('下')
        img_tank = img_tank_D
        hero_tank_move('D')
        hero_tank_direction = 'D'
    elif keypressed[pygame.K_LEFT]:
        print('左')
        img_tank = img_tank_L
        hero_tank_move('L')
        hero_tank_direction = 'L'
    elif keypressed[pygame.K_RIGHT]:
        print('右')
        img_tank = img_tank_R
        hero_tank_move('R')
        hero_tank_direction = 'R'

    clock.tick(50)

