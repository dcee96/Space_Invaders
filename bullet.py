import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A Class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.bullet_color

        #Create a Bullet Rect at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                                self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullets position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.setting.bullet_speed
        #Update next position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet onto the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    