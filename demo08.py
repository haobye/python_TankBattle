"""
新增功能：
1、双方坦克的碰撞
    ·哪方坦克主动碰撞、则哪方坦克主动停下来、stay()
2、音效处理

注意事项：
    1、84行Bug尚未处理
    2、Bug我方坦克被打死后会报错
"""
import pygame
import time
import random

_display = pygame.display
COLOR_BLACK = pygame.Color(0, 30, 50)
COLOR_RED = pygame.Color(255, 0, 0)
version = "1.8"


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 800
    # 创建我方坦克
    tank_p1 = None
    # 创建敌方坦克列表、及其数量
    enemy_tank = []
    enemy_count = 5
    # 存储我方子弹的列表
    bullet_list = []
    # 存储敌方子弹的列表
    enemy_bullet_list = []
    # 爆炸效果的列表
    explode_list = []
    # 墙壁列表
    wall_list = []

    def __init__(self):
        pass

    # 开始游戏
    def start_game(self):
        # 初始化display模块
        _display.init()
        # 创建游戏加载窗口，可尝试直接使用数字
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 创建我方坦克、重生
        self.creat_my_tank()
        # 创建墙壁
        self.creat_walls()
        # 设置标题
        _display.set_caption("坦克大战" + version)
        # 创建我方坦克、设置坦克位置
        MainGame.tank_p1 = Tank(MainGame.SCREEN_HEIGHT / 2, MainGame.SCREEN_WIDTH / 2)
        # 创建敌方坦克
        self.creat_enemy_tank()
        # 让窗口持续刷新，以保持界面
        while True:
            # 给窗口颜色
            MainGame.window.fill(COLOR_BLACK)
            # 将制作的小画布贴到窗口(参数：文本，左上角的坐标)
            MainGame.window.blit(self.get_text_surface("剩余敌方坦克%s辆" % len(MainGame.enemy_tank)), (10, 10))
            # 再循环中完成事件的获取
            self.get_event()
            # 调用展示墙壁方法
            self.blit_walls()
            # 如果我方坦克存在
            if MainGame.tank_p1 and MainGame.tank_p1.live:
                # 将我方坦克加入到窗口中
                MainGame.tank_p1.displayTank()
            # 如果不存在
            else:
                del MainGame.tank_p1
                MainGame.tank_p1 = None
            # 展示敌方坦克
            self.blit_enemy_tank()
            # 根据坦克开关判断是否持续调用移动方法
            if MainGame.tank_p1 and not MainGame.tank_p1.stop:
                MainGame.tank_p1.move()
                # 若是碰撞墙壁、则还原。调用的是碰撞墙壁的方法
                MainGame.tank_p1.hit_walls()
                # # 我方坦克是否碰撞到敌方坦克、调用不到此方法、导致报错
                # MainGame.tank_p1.hit_enemy_tank()
            # 调用渲染子弹列表的方法
            self.blit_bullet()
            # 调用渲染敌方子弹列表的方法
            self.blit_enemy_bullet()
            # 调用展示爆炸效果的方法
            self.display_explode()

            # 减缓循环次数
            time.sleep(0.02)
            # 窗口刷新
            _display.update()

    # 我方坦克重生
    def creat_my_tank(self):
        MainGame.tank_p1 = MyTank(400, 400)
        # 创建音乐对象
        music = Music('img/start.wav')
        # 调用播放
        music.play()

    # 创建墙壁
    def creat_walls(self):
        # 创建多少个墙壁
        for i in range(6):
            wall = Wall(130*i, 240)
            MainGame.wall_list.append(wall)

    # 展示墙壁
    def blit_walls(self):
        for wall in MainGame.wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.wall_list.remove(wall)

    # 实现剩余坦克的提示
    def get_text_surface(self, text):
        # 初始化字体模块
        pygame.font.init()
        # 查看系统支持的字体
        # fontlist = pygame.font.get_fonts()
        # print(font)
        # 选中一个合适的字体kaiti、其对中文兼容性较好
        font = pygame.font.SysFont('kaiti', 18)
        # 在新Surface上绘制文本，参数：文本，抗锯齿，颜色
        text_surface = font.render(text, True, COLOR_RED)
        return text_surface

    # 获取程序期间所有事件的方法
    def get_event(self):
        # 获取时间
        event_list = pygame.event.get()
        # 判断是鼠标点击(关闭退出)还是键盘输入(上下左右、射击)
        for event in event_list:
            # 若是QUIT则调用本类中的退出方法
            if event.type == pygame.QUIT:
                self.end_game()
            # 若是KEYDOWN则再判断其KEY具体是那个
            if event.type == pygame.KEYDOWN:
                # 按下ESC键让我方坦克重生，确定我方坦克已经死亡(消失)
                if event.key == pygame.K_ESCAPE and not MainGame.tank_p1:
                    self.creat_my_tank()
                if MainGame.tank_p1 and MainGame.tank_p1.live:
                    if event.key == pygame.K_LEFT:
                        print("向左调头，移动")
                        # 调头
                        MainGame.tank_p1.direction = 'l'
                        # 更改stop
                        MainGame.tank_p1.stop = False
                        # # 移动
                        # MainGame.tank_p1.move()
                    if event.key == pygame.K_RIGHT:
                        print("向右调头，移动")
                        MainGame.tank_p1.direction = 'r'
                        MainGame.tank_p1.stop = False
                        # MainGame.tank_p1.move()
                    if event.key == pygame.K_UP:
                        print("向上调头，移动")
                        MainGame.tank_p1.direction = 'u'
                        MainGame.tank_p1.stop = False
                        # MainGame.tank_p1.move()
                    if event.key == pygame.K_DOWN:
                        print("向下调头，移动")
                        MainGame.tank_p1.direction = 'd'
                        MainGame.tank_p1.stop = False
                        # MainGame.tank_p1.move()
                    if event.key == pygame.K_SPACE:  # space空格
                        # m = Bullet(MainGame.tank_p1)
                        # MainGame.bullet_list.append(m)
                        print("发射子弹")
                        # 控制子弹数量
                        if len(MainGame.bullet_list) < 3:
                            # 产生一颗子弹
                            m = Bullet(MainGame.tank_p1)
                            # 将子弹加入子弹列表
                            MainGame.bullet_list.append(m)
                            # 创建发射音效
                            music = Music('img/fire.wav')
                            music.play()
                        else:
                            print("当前子弹数量不足")
            # 若是键盘按键松开，则将坦克停下来
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.tank_p1 and MainGame.tank_p1.live:
                        # 修改坦克状态
                        MainGame.tank_p1.stop = True

    # 创建敌方坦克
    def creat_enemy_tank(self):
        top = 100  # left、top参数、因为top不变可使敌方坦克在一条线上随机产生
        for i in range(MainGame.enemy_count):
            speed = random.randint(3, 5)  # 每个坦克都时随机速度
            left = random.randint(1, 7)  # 每次都随机生成一个left值
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.enemy_tank.append(eTank)

    # 将敌方坦克放入窗口中
    def blit_enemy_tank(self):
        for eTank in MainGame.enemy_tank:
            if eTank.live:
                # 敌方坦克展示
                eTank.displayTank()
                # 敌方坦克随机移动
                eTank.random_move()
                # 调用敌方坦克与墙壁碰撞的方法
                eTank.hit_walls()
                # 敌方坦克碰撞我方坦克、停下
                eTank.hit_my_tank()
                # 调用敌方坦克射击方法
                eBullet = eTank.shot()
                # 如果子弹不是空，即None，再加入到列表
                if eBullet:
                    # 将敌方子弹存储到敌方子弹列表中
                    MainGame.enemy_bullet_list.append(eBullet)
            # 很明显，坦克若是挂掉啦，则直接从列表中删除
            else:
                MainGame.enemy_tank.remove(eTank)

    # 将我方子弹加入到窗口中
    def blit_bullet(self):
        for bullet in MainGame.bullet_list:
            # 如果子弹活着，则渲染，如果死亡，则移除
            if bullet.live:
                # 显示子弹
                bullet.displayButtle()
                # 紧接着让子弹移动
                bullet.move()
                # 如果存在、调用我方子弹与敌方坦克碰撞的方法
                if MainGame.tank_p1 and MainGame.tank_p1.live:
                    bullet.hit_enemy_tank()
                # 调用我方子弹与墙壁的碰撞
                bullet.hit_walls()
            else:
                MainGame.bullet_list.remove(bullet)

    # 将敌方子弹加入到窗口中
    def blit_enemy_bullet(self):
        for ebullet in MainGame.enemy_bullet_list:
            # 如果子弹活着，则渲染，如果死亡，则移除
            if ebullet.live:
                # 显示子弹
                ebullet.displayButtle()
                # 紧接着让子弹移动
                ebullet.move()
                if MainGame.tank_p1 and MainGame.tank_p1.live:
                    # 实现敌方子弹与我方坦克碰撞后，我方坦克和敌方子弹消失
                    ebullet.hit_my_tank()
                ebullet.hit_walls()
            else:
                MainGame.enemy_bullet_list.remove(ebullet)

    # 新增方法：展示爆炸效果列表
    def display_explode(self):
        for explode in MainGame.explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explode_list.remove(explode)

    # 结束游戏
    def end_game(self):
        print("感谢使用")
        # 直接结束python解释器
        exit()


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
    def __init__(self, left, top):
        self.images = {
            'u': pygame.image.load('img/p1tankU.gif'),
            'd': pygame.image.load('img/p1tankD.gif'),
            'l': pygame.image.load('img/p1tankL.gif'),
            'r': pygame.image.load('img/p1tankR.gif'),
        }
        self.direction = 'u'  # direction方向
        self.img = self.images[self.direction]
        # 坦克所在区域、默认
        self.rect = self.img.get_rect()
        # 坦克所在区域、自定义、分别距xy轴的距离
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = 5
        # 新增坦克移动开关属性
        self.stop = True
        # 新增坦克是否活着属性
        self.live = True
        # 新增坦克坐标属性、用于坐标还原
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 坦克移动方法
    def move(self):
        # 每次都先记录移动前的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 然后再判断
        if self.direction == 'u':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        if self.direction == 'd':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
        if self.direction == 'r':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        if self.direction == 'l':
            if self.rect.left > 0:
                self.rect.left -= self.speed

    # 坦克坐标还原
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    # 碰撞墙壁
    def hit_walls(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()

    # 坦克攻击方法
    def shot(self):
        return Bullet(self)

    # 显示坦克(将坦克绘制到窗口)
    def displayTank(self):
        # 重新设置坦克图片
        self.img = self.images[self.direction]
        # 将坦克加入窗口
        MainGame.window.blit(self.img, self.rect)


class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    # 新增我方坦克碰撞敌方坦克的方法
    def hit_enemy_tank(self):
        for eTank in MainGame.enemy_tank:
            if pygame.sprite.collide_rect(eTank, self):
                self.stay()


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        self.images = {
            'u': pygame.image.load('img/enemy1U.gif'),
            'd': pygame.image.load('img/enemy1D.gif'),
            'l': pygame.image.load('img/enemy1L.gif'),
            'r': pygame.image.load('img/enemy1R.gif'),
        }
        self.direction = self.random_direction()
        self.img = self.images[self.direction]
        # 坦克所在区域、默认
        self.rect = self.img.get_rect()
        # 坦克所在区域、自定义、分别距xy轴的距离
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        # 新增坦克移动开关属性
        self.stop = True
        # 新增坦克步数属性，用来控制敌方坦克随机移动
        self.step = 50

    # 敌方坦克碰撞我方坦克
    def hit_my_tank(self):
        if pygame.sprite.collide_rect(self, MainGame.tank_p1):
            self.stay()

    # 随机选择方向
    def random_direction(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'u'
        if num == 2:
            return 'd'
        if num == 3:
            return 'l'
        if num == 4:
            return 'r'

    # 敌方坦克随机移动的方法
    def random_move(self):
        if self.step == 0:
            self.direction = self.random_direction()
            self.step = 50
        else:
            self.move()
            self.step -= 1

    # 重写父类子弹发射方法(控制敌方子弹速度)
    def shot(self):
        num = random.randint(1, 50)
        if num == 1:
            return Bullet(self)


class Bullet(BaseItem):
    def __init__(self, tank):
        # 图像
        self.image = pygame.image.load('img/tankmissile.gif')
        # 坦克方向
        self.direction = tank.direction
        # 位置
        self.rect = self.image.get_rect()
        if self.direction == 'u':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'd':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'l':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'r':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        # 子弹速度
        self.speed = 7
        # 子弹是否活着
        self.live = True

    # 子弹移动的方法
    def move(self):
        if self.direction == 'u':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 碰撞到墙壁，则子弹消亡
                self.live = False
        elif self.direction == 'd':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'l':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'r':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    # 展示子弹
    def displayButtle(self):
        MainGame.window.blit(self.image, self.rect)

    # 新增我方子弹与敌方坦克碰撞的方法
    def hit_enemy_tank(self):
        for eTank in MainGame.enemy_tank:
            if pygame.sprite.collide_rect(eTank, self):
                self.live = False
                eTank.live = False
                # 产生一个爆炸效果
                explode = Explode(eTank)
                # 将爆炸效果加入到列表
                MainGame.explode_list.append(explode)

    # 新增敌方子弹与我方坦克的碰撞
    def hit_my_tank(self):
        if pygame.sprite.collide_rect(self, MainGame.tank_p1):
            # 产生爆炸效果，并加入到爆炸列表中
            explode = Explode(MainGame.tank_p1)
            MainGame.explode_list.append(explode)
            # 修改子弹状态
            self.live = False
            # 修改坦克状态
            MainGame.tank_p1.live = False

    # 新增子弹和墙壁的碰撞
    def hit_walls(self):
        for wall in MainGame.wall_list:
            # 如果子弹与墙壁产生碰撞
            if pygame.sprite.collide_rect(self, wall):
                # 修改子弹状态
                self.live = False
                # 墙壁每次被攻击，生命值都会减一
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif')
        ]
        self.image = self.images[self.step]
        self.live = True

    # 展示爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Wall():
    def __init__(self, left, top):
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        # 判断是否展示墙壁
        self.live = True
        # 墙壁的生命值
        self.hp = 7

    # 展示墙壁
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)


class Music():
    def __init__(self, music_name):
        self.music_name = music_name
        # 先初始化混响器，才可以使用
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_name)

    # 播放音乐
    def play(self):
        pygame.mixer.music.play()


if __name__ == '__main__':
    MainGame().start_game()
