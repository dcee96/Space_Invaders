import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Blueprint for creating aliens's."""
    def __init__(self, aa_game):
        super().__init__()
        self.screen = aa_game.screen
        self.settings = aa_game.setting

        # Load the rect assests.
        self.image = pygame.image.load('C:/Users/coole/Python Code/Space_Invaders/game_assests/alien2.png')
        self.rect = self.image.get_rect()

        # start each new alien near the topleft.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height - 100 

        # Store the aliens horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move Ships to the Right."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True
