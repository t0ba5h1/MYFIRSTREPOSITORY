from pygame import *
from random import randint


#основной класс Sprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=100, size_y=100):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс для игрока    
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 150:
            self.rect.x += self.speed



#класс для врага
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1,3)
            lost += 1


#класс для пуль   
class bullet(GameSprite):
    
    def update(self):
        self.rect.y -= self.speed
        
            
        



#создание обьектов
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load('7936937.jpg'), (win_width, win_height))
player = Player('png-klev-club-3vet-p-pvo-png-1.png', 275, 400, 5)
#группы спрайтов
bullets = sprite.Group()
drones = sprite.Group()
weapons = sprite.Group()
for i in range(3):
    weapons.add(Enemy('5en49mq7e9sez1wpr9j4y58abux1lx6g-416x489.png', randint(0,600), randint(-200,0), 1))
for i in range(5):
    drones.add(Enemy('pngtree-drone-png-graphic-png-image_14594979.png', randint(0,600), randint(-200,0), 1))

game = True
finish = False

score = 0
lost = 0
font.init()
font1 = font.Font('Arial', 36)


clock = time.Clock()
F_P_S = 90


#игровой цикл
while game:
    #проверка выхода из приложения
    for e in event.get():
        if e.type == QUIT:
            game = False
    #обновление экрана
    if finish != True:
        window.blit(background, (0,0))



    #обновление игрока
        player.reset()
        player.update()
        #выпуск пули
        if key.get_pressed()[K_SPACE]:
            bullets.add(bullet('bullet.png', player.rect.centerx, player.rect.y, 1, 15, 30))
        #обновление пули
        bullets.update()
        bullets.draw(window)

        #обновление врага
        drones.draw(window)
        drones.update()
        
        weapons.draw(window)
        weapons.update()
        #надпись
        text_lose = font1.render(
        "Пропущено: " + str(lost), 1, (255, 255, 255)
            )
        window.blit(text_lose, (0, 20))


        scores = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(scores, (0, 100))


        if sprite.spritecollide(player, drones, False) or lost == 3 or sprite.spritecollide(player, weapons, False):
            lose = font1.render('вы проиграли!', 1, (255, 255, 255))
            window.blit(lose, (250, 250))
            finish = True

        
        collides = sprite.groupcollide(drones, bullets, True, True)
        for c in collides:
            score = score + 1
            drones.add(Enemy('pngtree-drone-png-graphic-png-image_14594979.png', randint(0,600), randint(-200,0), 1))


        if score == 10:
                ura = font1.render('вы выиграли!', 1, (255, 255, 255))
                window.blit(ura, (250, 250))
                finish = True

    display.update()
    clock.tick(F_P_S)