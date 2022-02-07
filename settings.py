import pygame, random


class Settings:
    """A class that documents and controls all of the games settings."""

    def __init__(self, ai_game):
        """Initalizes Game settings."""
        # Background Settings.
        self.screen = ai_game.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.screen_height = self.screen.get_height()
        self.bgColor = (0,0,25)

        self.alien_points = 50

        self.score_scale = 1.5 

        # Bullet Settings.
        self.bullet_height = 15
        self.bullet_width = 5
        self.bullet_color = (255,100, 0)
        self.bullets_allowed = 2

        self.fleet_drop_speed = 14

        #Scale the Difficulty of the game each round.
        self.speedup_scale = 1.1

        self.intialize_dynamic_settings()

    def intialize_dynamic_settings(self):
        self.bullet_speed = 1.5
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.alien_speed = 1.75
        # 'fleet_direction' of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.aliens_points = int(self.alien_points * self.score_scale)