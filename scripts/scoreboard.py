import pygame

class Scoreboard:
    def __init__(self, font: pygame.font.Font, x: int, y: int) -> None:
        """
        Initialize the Scoreboard object.
        Args:
            font (pygame.font.Font): The font to render the score.
            x (int): The x-coordinate to position the score.
            y (int): The y-coordinate to position the score.
        """
        self.font = font
        self.x = x
        self.y = y
        self.score = 0

    def increase_score(self, points: int) -> None:
        """
        Increase the score by the specified points.
        Args:
            points (int): Points to add to the score.
        """
        self.score += points

    def display_score(self, screen: pygame.Surface) -> None:
        """
        Render the score and display it on the screen.
        Args:
            screen (pygame.Surface): The game screen.
        """
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (self.x, self.y))

    def reset_score(self) -> None:
        """
        Reset the score to zero.
        """
        self.score = 0
