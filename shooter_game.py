from pygame import *
from random import randint

#background music
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 72)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_ufo = "ufo.png"
img_bullet = "bullet.png"
lost = 0
Skor = 0

#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
       print('tembak')

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(60, 520)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    Shoot = key.get_pressed()
    if Shoot[K_SPACE] :
        ship.fire()
        

    if not finish:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            Skor = Skor + 1
            monster = Enemy(img_ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        window.blit(background,(0,0))
        Shoot = key.get_pressed()
        if Shoot[K_SPACE] :
            ship.fire()
        text_lose = font2.render("Missed:" + str(lost), 1, (255, 255, 255))
        text_Skor = font2.render("Score:" + str(Skor), 1, (255, 255, 255))
        win = font1.render('YOU WIN', True, (255, 255, 255))
        lose = font1.render('YOU LOSE', True, (255, 255, 255))
        if Skor >= 30:
            window.blit(win, (230, 230))
            finish = True
        if lost >= 1:
            window.blit(lose, (230, 230))
            finish = True
        window.blit(text_lose, (10, 50))
        window.blit(text_Skor, (10, 3))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        display.update()
    time.delay(50)
    