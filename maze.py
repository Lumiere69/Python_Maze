from pygame import *

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Не лабиринт а филиал ада')
background = transform.scale(image.load(
    'background.jpg'), (win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, p_speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (65, 65))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed


class Enemy(GameSprite):
    direction = 'left'

    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
# музыка
# mixer.init()
# mixer.music.load(jungles.ogg)
# mixer.music.play()


font.init()
font = font.Font(None, 70)

win = font.render('YOU WIN', True, (255, 215, 0))
lose = font.render('YOU LOSE', True, (0, 0, 0))


class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.wall_height = wall_height
        self.wall_width = wall_width
        self.image = Surface((self.wall_width, self.wall_height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


cyborg = Enemy('cyborg.png', win_width - 80, 280, 3)
hero = Player('hero.png', win_height - 480, 420, 10)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)


walls = []
walls.append(Wall(255, 0, 0, 0, 0, 15, 500))
walls.append(Wall(255, 0, 0, 0, 0, 515, 15))
walls.append(Wall(255, 0, 0, 500, 150, 15, 350))
walls.append(Wall(255, 0, 0, 200, 111, 15, 389))
walls.append(Wall(255, 0, 0, 350, 0, 15, 389))


FPS = 60
clock = time.Clock()
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        cyborg.update()
        cyborg.reset()
        hero.update()
        hero.reset()
        final.reset()
        for wall in walls:
            wall.draw_wall()
        # Условия победы
        if sprite.collide_rect(hero, final):
            window.blit(win, (200, 200))
            # money.play()
            finish = True
        # Условия проигрыша
        for wall in walls:
            if sprite.collide_rect(hero, wall):
                window.blit(lose, (200, 200))
                finish = True
                # kick.play()

        if sprite.collide_rect(hero, cyborg):
            window.blit(lose, (200, 200))
            finish = True
            # kick.play()

    clock.tick(FPS)
    display.update()
