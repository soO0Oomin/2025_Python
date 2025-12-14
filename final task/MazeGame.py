import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("패치의 위험한 귀갓길")
clock = pygame.time.Clock()

# RGB 색상 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Player 클래스
class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("patch.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 69))
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True

    def update(self, mouse_pos):
        if self.alive:
            self.rect.center = mouse_pos

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)

    def die(self):
        self.alive = False

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.alive = True

# Wall 클래스
class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

# Enemy 클래스
class Enemy:
    def __init__(self, x, y, size):
        self.image = pygame.image.load("bacteria.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Goal 클래스
class Goal:
    def __init__(self, x, y):
        self.image = pygame.image.load("home.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (144, 130))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 객체 생성
player = Player(29, 65)

walls = [
    Wall(100, 0, 20, 500),
    Wall(200, 100, 20, 500),
    Wall(300, 0, 20, 500),
    Wall(400, 100, 20, 500),
    Wall(500, 0, 20, 500)
]

enemies = [
    Enemy(200, 300, 40),
    Enemy(400, 200, 40),
    Enemy(600, 350, 40),
]

goal = Goal(650, 470)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

game_state = "PLAY"

# 메인 루프
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "PLAY":
        mouse_pos = pygame.mouse.get_pos()
        player.update(mouse_pos)

        for enemy in enemies:
            enemy.update()

        # 벽과 충돌 시 게임 오버
        for wall in walls:
            if player.rect.colliderect(wall.rect):
                player.die()
                game_state = "GAMEOVER"
        
        # 세균과 충돌 시 게임 오버
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player.die()
                game_state = "GAMEOVER"

        # 집과 충돌 시 게임 클리어
        if player.rect.colliderect(goal.rect):
            game_state = "CLEAR"

    # 게임 화면 그리기
    screen.fill(WHITE)

    # 시작 지점 표시
    start_point = small_font.render("START", True, GREEN)
    screen.blit(start_point, (5, 5))

    for wall in walls:
        wall.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    goal.draw(screen)
    player.draw(screen)

    # 게임 오버 글씨 생성
    if game_state == "GAMEOVER":
        text = font.render("Game Over", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

    # 게임 클리어 글씨 생성
    if game_state == "CLEAR":
        text = font.render("Clear!", True, GREEN)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()