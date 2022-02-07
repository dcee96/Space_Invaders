
class GameStats:
    """Track game data for Alien Assault."""
    def __init__(self, aa_game):
        self.settings = aa_game.setting
        self.reset_stats()
        self.game_active = False
        self.score = 0
        self.highscore = 0
        self.round = 1

    def reset_stats(self): 
        """Initalialize the game variables."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.round = 0
        self.settings.intialize_dynamic_settings()