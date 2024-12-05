# File: game_over.py

import pygame
import sys

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class GameOverScreen:
    def __init__(self, screen, width, height, font_path=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_path = font_path or pygame.font.get_default_font()
        self.font = pygame.font.Font(self.font_path, 50)  
        self.small_font = pygame.font.Font(self.font_path, 30)  

    def display(self, message, score):
        """
        Display the game over screen with the given message and score.
        """
        # Dark background Screen
        self.screen.fill(BLACK)

        # Render the game over message
        game_over_text = self.font.render(message, True, RED)
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(game_over_text, game_over_rect)

        # Display the player's final score
        score_text = self.small_font.render(f"Your Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)

        # Display restart and quit options
        restart_text = self.small_font.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 1.7))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.small_font.render("Press Q to Quit", True, YELLOW)
        quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 1.5))
        self.screen.blit(quit_text, quit_rect)

        # Update the display
        pygame.display.flip()

    def handle_events(self):
        """
        Handle events for the game over screen.
        Returns:
            "restart" if the player chooses to restart,
            "quit" if the player chooses to quit.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        return "restart"
                    elif event.key == pygame.K_q:  # Quit
                        pygame.quit()
                        sys.exit()
            pygame.time.Clock().tick(60)  # Maintain FPS
