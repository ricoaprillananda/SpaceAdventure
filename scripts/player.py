import pygame
from bullet import Bullet 

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, speed):
        """
        Initialize the Player object.
        Args:
            x (int): Initial x-coordinate of the player.
            y (int): Initial y-coordinate of the player.
            width (int): Width of the player image.
            height (int): Height of the player image.
            image_path (str): Path to the player image.
            speed (int): Speed of the player's movement.
        """
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed  # Player movement speed
        self.health = 100  # Player health
        self.is_power_burst_active = False  # To track power burst status

    def move_left(self, screen_width):
        """Move the player left, wrapping around the screen if needed."""
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Wrap around to the right side
            self.rect.left = screen_width

    def move_right(self, screen_width):
        """Move the player right, wrapping around the screen if needed."""
        self.rect.x += self.speed
        if self.rect.left > screen_width:  # Wrap around to the left side
            self.rect.right = 0

    def move_up(self, screen_height):
        """Move the player up, wrapping around the screen if needed."""
        self.rect.y -= self.speed
        if self.rect.bottom < 0:  # Wrap around to the bottom
            self.rect.top = screen_height

    def move_down(self, screen_height):
        """Move the player down, wrapping around the screen if needed."""
        self.rect.y += self.speed
        if self.rect.top > screen_height:  # Wrap around to the top
            self.rect.bottom = 0

    def draw(self, screen, WIDTH):
        """
        Draw the player on the screen.
        Args:
            screen (pygame.Surface): The game screen.
            WIDTH (int): Screen width for health bar calculation.
        """
        screen.blit(self.image, self.rect)
        
        # Draw the health as a bar on the right side of the screen
        health_bar_width = 200
        health_bar_height = 20
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (WIDTH - health_bar_width - 10, 10, health_bar_width, health_bar_height))  # Background bar
        pygame.draw.rect(screen, (0, 255, 0), (WIDTH - health_bar_width - 10, 10, health_bar_width * health_percentage, health_bar_height))  # Health bar

    def take_damage(self, amount):
        """
        Decrease the player's health when hit by an alien bullet.
        Args:
            amount (int): Amount of damage to the player.
        """
        self.health -= amount
        if self.health < 0:  # Ensure health doesn't go below 0
            self.health = 0
        return self.health <= 0  # Return True if health is depleted

    def reset_position(self, x, y):
        """
        Reset the player's position.
        Args:
            x (int): New x-coordinate.
            y (int): New y-coordinate.
        """
        self.rect.topleft = (x, y)

    def shoot_burst(self, bullets):
        """Shoot multiple bullets during power burst (rainbow burst)."""
        bullet_offset = 0
        for i in range(5):  # Shoot 5 bullets in a burst
            bullet = Bullet(self.rect.centerx + bullet_offset, self.rect.top)
            bullets.add(bullet)
            bullet_offset += 10  # Slightly offset bullets
        self.is_power_burst_active = False  # Deactivate after the burst

    def activate_power_burst(self):
        """Activate the rainbow burst power-up."""
        self.is_power_burst_active = True
