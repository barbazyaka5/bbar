import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import Game_Stats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
    '''класс для управления ресурсами и поведением игры'''
    def __init__(self):
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        '''создание экземпляров для хранения статистики и панели результатов'''

        '''Создание экземпляра для хранения игровой статистики'''
        self.stats=Game_Stats(self)
        self.sb=Scoreboard(self)

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()

        '''создание кнопки play'''
        self.play_button=Button(self, "Play")

    def run_game(self):
        '''запуск основного цикла игры'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            pygame.display.flip()


    def _check_events(self):
        '''обрабатывает нажатия клавиш и события мыши'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''запускает новую игру при нажатии кнопки play'''
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            '''сброс игровых настроек'''
            self.settings.initialize_dynamic_settings()
            '''сброс игровой статистики'''
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            '''очистка списков противников и снарядов'''
            self.aliens.empty()
            self.bullets.empty()

            '''создание новых противников и размещение бетмена в центре экрана'''
            self._create_fleet()
            self.ship.center_ship()
            '''указатель мыши скрывается'''
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        '''реагирует на нажатие клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''реагирует на отпускание клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''создание нового снаряда и включение его в группу Bullets'''
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''обновление позиции и уничтожение старых снарядов'''
        '''обновление старых позиций'''
        self.bullets.update()
        '''удаление снарядов вне экрана'''
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        '''обработка коллизий снарядов с противниками'''
        '''удаление снарядов и противников участвующих в коллизиях'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            '''уничтожение существующих снарядов и создание новой партии противников'''
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            '''увелечение уровня'''
            self.stats.level+=1
            self.sb.prep_level()


    def _update_aliens(self):
        '''обновляет позиции всех противников'''
        self._check_fleet_edges()
        self.aliens.update()

        '''проверка столкновений противников с бемтменом'''
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        '''проверить добрались ли противники до границы экрана'''
        self._check_aliens_bottom()


    def _ship_hit(self):
        '''обрабатывает столкновение противников с главным героем'''
        if self.stats.ships_left>0:
            '''уменьшение ships_left и обновление панели счета'''
            self.stats.ships_left-=1
            self.sb.prep_ships()

            '''очистка списка противников и снарядов'''
            self.aliens.empty()
            self.bullets.empty()

            '''создание новых противников и бетмена с помещением его в центре экрана'''
            self._create_fleet()
            self.ship.center_ship()

            '''пауза'''
            sleep(0.5)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        '''проверяет достижение противников нижней границы экрана'''
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                '''происходит то же что и при столкновении противников с бетменом'''
                self._ship_hit()
                break

    def _create_fleet(self):
        '''создание противника'''
        alien=Alien(self)
        alien_width, alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-(2*alien_width)
        number_aliens_x=available_space_x//(2*alien_width)
        '''определние кол-ва рядов помещающих на экране'''
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
        number_rows=available_space_y//(2*alien_height)
        '''создание флота вторжения'''
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        '''создание чувака и размещение его в ряду'''
        alien = Alien(self)
        alien_width, alien_height=alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''реагирует на достижение противника края экрана'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''опускает всех противников и меняет их направление'''
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _update_screen(self):
        '''обновляет изображение на экране и отображает новый экран'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        '''вывод информации о счете'''
        self.sb.show_score()

        '''кнопка play отображается в том случае если игра неактивна'''
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__=='__main__':
    ai=AlienInvasion()
    ai.run_game()