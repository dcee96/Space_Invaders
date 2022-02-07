import pygame, settings

class Ship:
    """A Class to manange the ship."""

    def __init__(self, aa_game):
        """Intialize the ship at the starting position."""
        self.screen = aa_game.screen
        self.screen_rect = aa_game.screen.get_rect()

        # Load the ship into the game and return it rect()
        self.image = pygame.image.load('C:/Users/coole/Python Code/Space_Invaders/game_assests/8-bitShip_128x97 .png')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom middle of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Decimal value of ships horizontal positon.
        self.x = float(self.rect.x)

        #Ships movement speed.
        self.speed = settings.Settings(aa_game).ship_speed

        #Flags for making the ship move.
        self.moving_right = False
        self.moving_left = False
            
    def blitme(self):
        """Draw ship at is current location."""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """Update ships position based on what flag is true."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.speed
        
        # Update the actual Rect after new value is calculated.
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)