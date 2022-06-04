import pygame, sys, settings, ship
from pygame.constants import FULLSCREEN
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard


class Alien_Assault:
    """Main class that handles game assests/behaviors."""

    def __init__(self):
        """Initalize the game, and create game resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), FULLSCREEN)
        self.setting = settings.Settings(self)
        pygame.display.set_caption("Alien Assault")

        #Create an instance to store game variables.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # The game's elements.
        self.ship = ship.Ship(self) 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def _keyUp_events(self, event):
        if event == pygame.K_d:
            self.ship.moving_right = False
        elif event == pygame.K_a:
            self.ship.moving_left = False

    def _keyDown_events(self, event):
        if event == pygame.K_d:
            self.ship.moving_right = True
        elif event == pygame.K_a:
            self.ship.moving_left = True
        elif event == pygame.K_q:
            sys.exit()
        if event == pygame.K_SPACE:
            self.fire_bullet()

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYUP:
                self._keyUp_events(event.key)

            elif event.type == pygame.KEYDOWN:
                self._keyDown_events(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """Updates the positions of bullets and deletes old bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

        if not self.aliens:
            # Destory existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.stats.round += 1

    def fire_bullet(self):
        """Bullets are limited to 3 shots at a time."""
        if len(self.bullets) <= self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        #Redraw the screen during each pass.
            self.screen.fill(self.setting.bgColor)
            self.ship.blitme()
            
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.sb.show_score()

            if not self.stats.game_active:
                self.play_button.draw_button()
            #Displays the most recent frame.
            pygame.display.flip()

    def _create_fleet(self):
        """Create a fleet of aliens."""
        #Make one alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Determine the how many aliens per row.
        available_space_x = self.setting.screen_width - (2 * alien_width) - 20
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine how any rows there will be.
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height -
                        (3 * alien_height) - ship_height) - 20
        number_rows = available_space_y // (4 * alien_height)

        # Create a full fleet of aliens. 
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): 
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number) + 40
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Look for ship alien collision events.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """Respond to bullet Collisions."""
        # Remove and bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.stats.score += self.setting.alien_points
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)  
            self.sb.prep_score()

        if not self.aliens:
            # Destory existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()
            self.stats.round += 1

    def _ship_hit(self):
        """Respond to the ship colliding with aliens."""
        if self.stats.ships_left > 0:
            #Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and recenter ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.stats.reset_stats()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()


if __name__ == "__main__":
    AA = Alien_Assault()
    AA.run_game() 