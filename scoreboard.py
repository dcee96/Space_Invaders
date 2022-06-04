import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report and record scoring info."""

    def __init__(self, aa_game):
        """Initalize Scorekeeping attributes."""
        self.aa_game = aa_game
        self.screen = aa_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = aa_game.setting
        self.stats = aa_game.stats

        #Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Prepare the inital score image.
        self.prep_score()

        #Preparing the indicator of remaining ships.
        self.prep_ships()

    def load_HS(self):
        """Retrive Highscores."""
        with open("C:/Users/coole/Python Code/Space_Invaders/game_assests/data/game_data.txt", 'r') as HS_data:
            old_hs = HS_data.read()
            return float(old_hs)   

    def save_HS(self):
        if self.highscore <= self.stats.score:
            self.highscore = self.stats.score
            with open('C:/Users/coole/Python Code/Space_Invaders/game_assests/data/game_data.txt', 'w') as hs_data:
                hs_data.write(str(self.highscore))
            hs_data.close

    def prep_score(self):
        """Turn the score into a rendered image."""
        round = self.stats.round
        round_str = "round: {}".format(round)
        self.round_image = self.font.render(round_str, True,
                        self.text_color, self.settings.bgColor)

        self.highscore = self.load_HS()
        self.rounded_HS = int(self.highscore)
        self.HS_str = "Highscore: {:,}".format(self.rounded_HS)
        self.HS_image = self.font.render(self.HS_str, True,
                        self.text_color, self.settings.bgColor)

        self.rounded_score = self.stats.score
        self.score_str = "Score: {:,}".format(self.rounded_score)
        self.score_image = self.font.render(self.score_str, True,
                        self.text_color, self.settings.bgColor)

        #Display the score at the top right of the screen.
        self.round_rect = self.round_image.get_rect()
        self.round_rect.right = self.round_rect.right + 300
        self.round_rect.top = 20

        self.HS_rect = self.HS_image.get_rect()
        self.HS_rect.right = self.HS_rect.right + 600
        self.HS_rect.top = 20

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.score_rect.right + 20
        self.score_rect.top = 20
        self.save_HS()

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.HS_image, self.HS_rect)
        self.screen.blit(self.round_image, self.round_rect)
        self.ships.draw(self.screen)

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.aa_game, sb_Ship=1)
            ship.rect.x = self.screen_rect.width - (100 + ship_number * ship.rect.width)
            ship.rect.y = 10
            self.ships.add(ship)
