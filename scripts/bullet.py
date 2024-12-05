# File: bullet.py

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-10, color=(0, 255, 0), width=5, height=15, image_path=None):
        super().__init__()
        
        # Load or create the bullet's image
        if image_path:  
        else:  
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Bullet movement properties
        self.speed = speed  

    def update(self):
        """
        Update the bullet's position.
        """
        self.rect.y += self.speed  # Move the bullet in the vertical direction

        # Remove the bullet if it goes off-screen
        if self.rect.bottom < 0 or self.rect.top > 800:  
            self.kill()

    def check_collision(self, target_group):
        """
        Check for collisions with a group of targets (e.g., aliens).
        Returns a list of targets hit by the bullet.
        """
        return pygame.sprite.spritecollide(self, target_group, True)  # Remove targets upon collision
