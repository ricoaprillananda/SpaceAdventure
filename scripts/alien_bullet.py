import pygame

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface((5, 15)) 
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

      
        self.speed = 5  

    def update(self):
        """
        Update the bullet's position.
        """
        self.rect.y += self.speed  

        if self.rect.top > pygame.display.get_surface().get_height():  
            self.kill()
