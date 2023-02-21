import pygame
import random
import os
# Инициализация Pygame
pygame.init()
# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 205)
# Окно
WIDTH = 1600
HEIGHT = 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
FPS = 60
NUM_COINS = 8
NUM_OBSTACLES = 10

# Изображения
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
background_image = pygame.image.load(os.path.join(img_folder, "background2.png")).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pygame.font.init()
font = pygame.font.Font(None, 28)

# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder, "player.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 76))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rect.x -= 5
        if keystate[pygame.K_RIGHT]:
            self.rect.x += 5
        if keystate[pygame.K_UP]:
            self.rect.y -= 5
        if keystate[pygame.K_DOWN]:
            self.rect.y += 5
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder, "obstacle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)
class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 50)
    def update(self, amount):
        self.score += amount
    def draw(self, screen):
        text = self.font.render(f'Score: {self.score}', True, BLACK)
        screen.blit(text, (100, 100))
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder, "coin.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Загружаем фоновую картинку
background_image = pygame.image.load("background2.png").convert()
# Загружаем звук
pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Создание персонажа
player = Player()
all_sprites.add(player)

# Создание препятствий и монет
for i in range(8):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

# Создаем объект для отображения счета
score = Score()

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Обработка событий (нажатия клавиш, клики мыши и др.)
    for event in pygame.event.get():
        # проверка на закрытие окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        score.update(10)
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

    # Проверка столкновений игрока с препятствиями
    hits = pygame.sprite.spritecollide(player, obstacles, False)
    if hits:
        # Выводим сообщение о проигрыше и кнопку "Начать заново"
        screen.blit(background_image, (0, 0))
        text = font.render("ОУ НООУ, ДИМАСИК УВИДЕЛ СЛИВНОЙ СТОЯК И ПОТЕРЯЛ ВСЮ МАНУ", True, BLACK)
        text_rect = text.get_rect(midtop=(WIDTH / 2, 100))
        screen.blit(text, text_rect)

        # Отрисовываем кнопку "Начать заново"
        button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, BLUE, button_rect)
        button_text = font.render("Удалить Змеевик", True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        # Ожидаем, пока игрок нажмет на кнопку "Начать заново"
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False
                        # Перезапускаем игру
                        all_sprites.empty()
                        coins.empty()
                        obstacles.empty()
                        player = Player()
                        all_sprites.add(player)
                        for i in range(NUM_COINS):
                            coin = Coin()
                            all_sprites.add(coin)
                            coins.add(coin)
                        for i in range(NUM_OBSTACLES):
                            obstacle = Obstacle()
                            all_sprites.add(obstacle)
                            obstacles.add(obstacle)
        continue

    # Рисуем на экране
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    score.draw(screen)

    # Переключаем экран и обновляем время
    pygame.display.flip()

# Закрываем Pygame
pygame.quit()



