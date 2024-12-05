import pygame
from alien import Alien
import random 

class LevelManager:
    def __init__(self, screen, width, height, font_path=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_path = font_path or pygame.font.get_default_font()
        self.font = pygame.font.Font(self.font_path, 40)  # Font size for level display
        self.current_level = 1
        self.max_levels = 10  # Define how many levels 
        self.aliens_per_level = 1  #
        self.alien_speed_increment = 0.5  # Speed increment for aliens per level

    def display_level(self):
        """
        Display the current level at the top center of the screen.
        """
        level_text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))  # White text
        level_rect = level_text.get_rect(center=(self.width // 2, 30))  # Position near the top center
        self.screen.blit(level_text, level_rect)

    def create_aliens(self, aliens_group):
        """
        Create and spawn aliens for the current level.
        Args:
            aliens_group (pygame.sprite.Group): The group to add the aliens to.
        """
        rows = min(5, self.current_level + 1)  # Increase rows as levels progress (up to 5 rows)
        cols = self.aliens_per_level  # Number of aliens increases with the level
        alien_speed = 1 + (self.alien_speed_increment * (self.current_level - 1))

        # Spread aliens more as the level progresses
        for row in range(rows):
            for col in range(cols):
                x_position = 80 * col + random.randint(-20, 20)  # Slight random spread for variety
                y_position = 50 * row + random.randint(-20, 20)  # Slight random spread for variety
                alien = Alien(
                    x=x_position,
                    y=y_position,
                    speed=alien_speed
                )
                aliens_group.add(alien)

    def check_level_up(self, aliens_group):
        """
        Check if all aliens are cleared to move to the next level.
        Args:
            aliens_group (pygame.sprite.Group): The current alien group.
        Returns:
            bool: True if all aliens are cleared (level up), False otherwise.
        """
        if len(aliens_group) == 0:  # All aliens defeated
            self.aliens_per_level += 1  # Increase the number of aliens per level
            self.current_level += 1
            return True
        return False

    def is_game_complete(self):
        """
        Check if the game has reached the final level.
        Returns:
            bool: True if the game is complete, False otherwise.
        """
        return self.current_level > self.max_levels

    def display_transition(self):
        """
        Display a level transition screen between levels.
        """
        # Fill the screen with a transition background color
        self.screen.fill((0, 0, 50))  # Dark blue background

        # Render the level transition text
        transition_text = self.font.render(f"Level {self.current_level}", True, (255, 255, 0))  # Yellow text
        transition_rect = transition_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(transition_text, transition_rect)

        # Update the display and pause briefly
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds before the next level

    def increase_level(self):
        """Increase the level after all aliens are destroyed."""
        self.current_level += 1
        if self.current_level > self.max_levels:
            self.current_level = self.max_levels  
