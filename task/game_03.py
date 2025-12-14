import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("똥 피하고 사과먹기")

clock = pygame.time.Clock()

apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (40,40))

poop_img = pygame.image.load("poop.png")
poop_img = pygame.transform.scale(poop_img, (40,40))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dukbird.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH //2, HEIGHT // 2)
        self.speed = 3

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        keys  = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = poop_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.speed_x = 3
        self.speed_y = 2
        self.start_x = x
        self.start_y = y

    def reset(self):
        self.rect.topleft = (self.start_x, self.start_y)
        self.speed_x = 2

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

enemy = Enemy(50,260)
all_sprites.add(enemy)
enemy_group.add(enemy)

coin_rect = pygame.Rect(430,130,40,40)
coin_speed_x = 2
coin_speed_y = 2

score = 0
game_over = False
start_screen = True # 시작화면 추가

button_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 40, 120, 40)
button_color = (200, 100, 100)
button_hover_color = (255, 130, 130)
font = pygame.font.SysFont(None, 28)

def reset_game():
    global score, game_over, coin_rect

    score = 0
    game_over = False

    player.reset()
    enemy.reset()

    coin_rect.x = 430
    coin_rect.y = 130

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 시작 화면 클릭 시 게임 시작
        if start_screen and event.type == pygame.MOUSEBUTTONDOWN:
            start_screen = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                reset_game()

    
    # 시작 화면
    if start_screen:
        screen.fill((150, 180, 255))

        title_font = pygame.font.SysFont(None, 50)
        title = title_font.render("똥 피하고 사과먹기", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))

        guide = font.render("CLICK TO START", True, (255,255,0))
        screen.blit(guide, (WIDTH//2 - guide.get_width()//2, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)
        continue


    if not game_over:
        all_sprites.update()

        coin_rect.x += coin_speed_x
        coin_rect.y += coin_speed_y

        if coin_rect.left < 0 or coin_rect.right > WIDTH:
            coin_speed_x *= -1
        if coin_rect.top < 0 or coin_rect.bottom > HEIGHT:
            coin_speed_y *= -1

        if player.rect.colliderect(coin_rect):
            print("사과 먹음!")
            score += 1

            coin_rect.x = random.randint(0, WIDTH - coin_rect.width)
            coin_rect.y = random.randint(0, HEIGHT - coin_rect.height)

            coin_speed_x *= random.choice([-1, 1])
            coin_speed_y *= random.choice([-1, 1])

        hits = pygame.sprite.spritecollide(player, enemy_group, False)
        if hits:
            print("똥과 충돌! 게임 오버")
            game_over = True

    screen.fill((170, 200, 255))
    pygame.draw.rect(screen, (80,170,80),(0, HEIGHT - 60, WIDTH, 60))

    screen.blit(apple_img, coin_rect)
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(score_text, (10,10))

    if game_over:
        over_text = font.render("GAME OVER", True, (255,0,0))
        over_x = (WIDTH - over_text.get_width()) // 2
        over_y = (HEIGHT - over_text.get_height()) // 2
        screen.blit(over_text, (over_x, over_y))

        mouse_pos = pygame.mouse.get_pos()
        btn_color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, btn_color, button_rect)
        text = font.render("Restart", True, (255, 255, 255))

        text_x = button_rect.x + (button_rect.width - text.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()