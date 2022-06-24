class Settings():
    """статические настройки игры"""
    """класс для настроек игры"""
    def __init__(self):
        #параметры экрана
        self.screen_width=1400
        self.screen_height=700
        self.bg_color=(230,230,230)

        '''настройка скорости персонажа'''
        self.ship_speed=5

        '''кол-во жизней'''
        self.ship_limit=3

        '''параметры снарядов персонажа'''

        self.bullet_speed=8
        self.bullet_width=20
        self.bullet_height=15
        self.bullet_color=(170,60,100)
        self.bullets_allowed=15

        ''' настройки противников'''
        self.alien_speed=2.0
        self.fleet_drop_speed=7

        '''темп ускорения игры'''
        self.speedup_scale=1.1
        '''темп роста стоимости противников'''
        self.score_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''инициализирует настройки изменяющиеся в ходе игры'''
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3.0
        self.alien_speed_factor=1.0

        '''1-движение вправо, -1 - движение влево'''
        self.fleet_direction = 1

        '''подсчет очков'''
        self.alien_points=50

    def increase_speed(self):
        '''увеличивает настройки скорости и стоимости противников'''
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale

        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)