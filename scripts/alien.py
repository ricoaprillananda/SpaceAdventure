import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3, image_path="assets/images/alien.png", health=100, shoot_cooldown_range=(1000, 3000)):
        super().__init__()
        # Load and scale alien image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (60, 600)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Alien movement properties
        self.speed_x = speed  # Horizontal movement speed (updated to accept external speed)
        self.speed_y = speed // 2  # Vertical movement speed for diagonal movements
        self.direction = 1  # 1: Right, -1: Left
        self.chase_player = False  # Flag to enable chasing behavior

        # Alien shooting cooldown timer 
        self.shoot_cooldown_min, self.shoot_cooldown_max = shoot_cooldown_range
        self.shoot_cooldown = random.randint(self.shoot_cooldown_min, self.shoot_cooldown_max)  # Time in milliseconds
        self.last_shot = pygame.time.get_ticks()  # Track the last shot time

        # Alien hit points (for more advanced gameplay mechanics)
        self.health = health  # Default 100 health, can be modified per alien type

    def update(self, screen_width, screen_height, player_rect):
        """
        Update alien movement and behavior.
        """
        # Chase the player when the flag is set
        if self.chase_player:
            if self.rect.centerx < player_rect.centerx:
                self.rect.x += self.speed_x
            elif self.rect.centerx > player_rect.centerx:
                self.rect.x -= self.speed_x

            if self.rect.centery < player_rect.centery:
                self.rect.y += self.speed_y
            elif self.rect.centery > player_rect.centery:
                self.rect.y -= self.speed_y
        else:
            # Horizontal movement with wrapping around the screen edges
            self.rect.x += self.speed_x * self.direction
            if self.rect.right >= screen_width:  # Wrap to left side
                self.rect.left = 0
            elif self.rect.left <= 0:  # Wrap to right side
                self.rect.right = screen_width

            # Change direction when hitting screen edges
            if self.rect.right >= screen_width or self.rect.left <= 0:  # Assuming screen width = 1280
                self.direction *= -1  # Reverse direction
                self.rect.y += 40  # Move down when changing direction

        # Randomly shoot bullets or lasers
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_cooldown:
            self.shoot()
            self.last_shot = current_time
            self.shoot_cooldown = random.randint(self.shoot_cooldown_min, self.shoot_cooldown_max)  # Reset cooldown

    def shoot(self):
        """
        Alien fires a bullet downwards or shoots a laser towards the player.
        Returns a bullet object to be added to the main game's bullet group.
        """
        from alien_bullet import AlienBullet  # Import the AlienBullet class
        from alien_laser import AlienLaser  # Import the AlienLaser class

        # Randomly choose between shooting a bullet or a laser
        if random.choice([True, False]):
            alien_bullet = AlienBullet(self.rect.centerx, self.rect.bottom)  # Create a new bullet
            return alien_bullet
        else:
            alien_laser = AlienLaser(self.rect.centerx, self.rect.bottom)  # Create a new laser
            return alien_laser

    def take_damage(self, amount):
        """
        Handle alien being hit by a bullet or laser.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove alien from the game when health reaches 0
            self.play_explosion() 

    def play_explosion(self):
        """
        Play explosion effect when the alien is killed (optional).
        """
        explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        explosion_sound.play()

    def activate_chase(self):
        """Activate the alien to chase the player."""
        self.chase_player = True

    def deactivate_chase(self):
        """Deactivate chasing behavior for the alien."""
        self.chase_player = False
