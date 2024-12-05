import pygame
import sys
import random

pygame.init()

# Window Size
WIDTH = 1368
HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game assets (images and sounds)
def load_assets():
    try:
        assets = {
            'background': pygame.image.load("assets/images/background_space.png").convert(),
            'player': pygame.image.load("assets/images/player.png").convert_alpha(),
            'alien': pygame.image.load("assets/images/alien.png").convert_alpha(),
            'shooting_sound': pygame.mixer.Sound("assets/sounds/shooting.wav"),
            'explosion_sound': pygame.mixer.Sound("assets/sounds/explosion.wav"),
            'enemy_shooting_sound': pygame.mixer.Sound("assets/sounds/enemy_shooting.wav"),
            'background_music': pygame.mixer.Sound("assets/sounds/background_music.mp3")
        }
        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.7)  # Background music volume dominant
        assets['shooting_sound'].set_volume(0.1)  # Reduce bullet sound volume
        assets['enemy_shooting_sound'].set_volume(0.1)  # Reduce enemy bullet sound volume
        return assets
    except pygame.error as e:
        print(f"Error loading assets: {e}")
        pygame.quit()
        sys.exit()

# Game classes
class Player(pygame.sprite.Sprite):
    def __init__(self, player_image):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (50, 50))  # Player size
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 70)
        self.invincible = True  # Invisible

    def move(self, dx, dy):
        if 0 < self.rect.left + dx < WIDTH - self.rect.width:
            self.rect.x += dx
        if 0 < self.rect.top + dy < HEIGHT - self.rect.height:
            self.rect.y += dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))  # Bullet Size
        self.image.fill(GREEN)  # Laser color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_image):
        super().__init__()
        self.image = pygame.transform.scale(alien_image, (70, 70))  # Alien size
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(50, 200)

    def update(self):
        self.rect.y += 1
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))  
        self.image.fill((0, 0, 255))  # Blue bullet for Aliens
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.kill()

# Game Engine
class Game:
    def __init__(self):
        self.running = True
        self.player = None
        self.aliens = None
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.score = 0
        self.assets = load_assets()

    def start(self):
        self.player = Player(self.assets['player'])
        self.aliens = pygame.sprite.Group([Alien(self.assets['alien']) for _ in range(10)])  # How much Aliens will appear
        self.score = 0
        pygame.mixer.music.play(-1)  # Loop background music

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(5, 0)
        if keys[pygame.K_UP]:
            self.player.move(0, -5)
        if keys[pygame.K_DOWN]:
            self.player.move(0, 5)
        if keys[pygame.K_SPACE]:
            self.shoot_bullet()

    def shoot_bullet(self):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
        self.bullets.add(bullet)
        self.assets['shooting_sound'].play()

    def update(self):
        self.bullets.update()
        self.aliens.update()
        self.enemy_bullets.update()

        for bullet in self.bullets:
            collided_aliens = pygame.sprite.spritecollide(bullet, self.aliens, True)
            for _ in collided_aliens:
                bullet.kill()
                self.score += 10
                self.assets['explosion_sound'].play()
                self.respawn_alien()  # Respawn an alien when one is destroyed

        for alien in self.aliens:
            if random.randint(0, 100) < 2:  # Random chance for alien to shoot
                alien_bullet = AlienBullet(alien.rect.centerx, alien.rect.bottom)
                self.enemy_bullets.add(alien_bullet)
                self.assets['enemy_shooting_sound'].play()

        return 'playing'

    def respawn_alien(self):
        if len(self.aliens) < 10:  # Respawn if there are less than 10 aliens
            alien = Alien(self.assets['alien'])
            self.aliens.add(alien)

    def draw(self):
        screen.blit(self.assets['background'], (0, 0))
        self.player.draw(screen)
        self.aliens.draw(screen)
        self.bullets.draw(screen)
        self.enemy_bullets.draw(screen)

        # Display the score
        score_text = small_font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def game_over(self):
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

        pygame.display.flip()
        pygame.time.wait(2000)  # 2 seconds before quitting

    def restart(self):
        self.start()

# Main game Engine
def main():
    game = Game()
    game.start()

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        game.handle_input()
        game_state = game.update()
        if game_state == 'game_over':
            game.game_over()
            game.restart()

        game.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
