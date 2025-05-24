import pygame
from pygame import mixer

pygame.init()
mixer.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Maze Game")

mixer.music.load('kick.ogg')
mixer.music.play(-1)
background = pygame.transform.scale(pygame.image.load("background.jpg"), (700, 500))

font = pygame.font.Font(None, 40)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Player(GameSprite):
    def __init__(self, x, y):
        super().__init__("hero.png", x, y, 50, 50)
        self.speed = 5
    
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < 450:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, x, y):
        super().__init__("cyborg.png", x, y, 50, 50)
        self.speed = 3
        self.direction = 1  
        self.left_bound = 400  
        self.right_bound = 600  
    
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.left_bound:  
            self.direction = 1
        elif self.rect.x >= self.right_bound: 
            self.direction = -1

class Wall(GameSprite):
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 198, 0))  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

wall1 = Wall(425, 275, 275, 10)
wall2 = Wall(425, 5, 10, 270)
wall3 = Wall(350, 65, 10, 500)
wall4 = Wall(5, 375, 295, 10)

player = Player(50, 400)
enemy = Enemy(600, 325)
treasure = GameSprite("treasure.png", 650, 450, 50, 50)

clock = pygame.time.Clock()
FPS = 60
kick = mixer.Sound('money.ogg')

game = True
game_over = False
win_message = None
lose_message = None

while game:
    window.blit(background, (0, 0))
    window.blit(player.image, player.rect)
    window.blit(enemy.image, enemy.rect)
    window.blit(treasure.image, treasure.rect)
    
    window.blit(wall1.image, wall1.rect)
    window.blit(wall2.image, wall2.rect)
    window.blit(wall3.image, wall3.rect)
    window.blit(wall4.image, wall4.rect) 
    
    if game_over:
        if win_message:
            text = font.render("YOU WIN!", True, (0, 255, 0))
            window.blit(text, (300, 200))
        elif lose_message:
            text = font.render("YOU LOSE!", True, (255, 0, 0))
            window.blit(text, (300, 200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if game_over:
        pygame.display.update()
        pygame.time.wait(2000)
        break

    keys = pygame.key.get_pressed()
    player.update(keys)
    enemy.update()

    if player.rect.colliderect(treasure.rect):
        win_message = True
        game_over = True
        mixer.music.stop()
        kick.play()

    if player.rect.colliderect(wall1.rect) or player.rect.colliderect(wall2.rect) or player.rect.colliderect(wall3.rect) or player.rect.colliderect(wall4.rect):  # Check collision with the new wall
        lose_message = True                                  
        game_over = True
        mixer.music.stop()
        kick.play()
    
    if player.rect.colliderect(enemy.rect):
        lose_message = True
        game_over = True
        mixer.music.stop()
        kick.play()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
