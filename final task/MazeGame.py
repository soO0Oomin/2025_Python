import pygame

# =====================
# 기본 설정
# =====================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("패치의 모험")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# =====================
# Player 클래스
# =====================
class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("patch.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
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

# =====================
# Wall 클래스
# =====================
class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

# =====================
# Enemy (함정) 클래스
# =====================
class Enemy:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# =====================
# Goal 클래스
# =====================
class Goal:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# =====================
# 오브젝트 생성
# =====================
player = Player(50, 50)

walls = [
    Wall(100, 0, 20, 500),
    Wall(200, 100, 20, 500),
    Wall(300, 0, 20, 500),
    Wall(400, 100, 20, 500),
]

enemies = [
    Enemy(150, 520, 40),
    Enemy(350, 520, 40),
    Enemy(550, 520, 40),
]

goal = Goal(700, 520, 60, 60)

font = pygame.font.SysFont(None, 36)

# =====================
# 메인 루프
# =====================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN and not player.alive:
            player.reset(50, 50)

    mouse_pos = pygame.mouse.get_pos()
    player.update(mouse_pos)

    # 충돌 처리
    for wall in walls:
        if player.rect.colliderect(wall.rect):
            player.die()

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.die()

    if player.rect.colliderect(goal.rect) and player.alive:
        print("🎉 도착 성공!")
        player.reset(50, 50)

    # =====================
    # 화면 그리기
    # =====================
    screen.fill(WHITE)

    for wall in walls:
        wall.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    goal.draw(screen)
    player.draw(screen)

    if not player.alive:
        text = font.render("죽었습니다! 클릭하면 재시작", True, RED)
        screen.blit(text, (230, 280))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()