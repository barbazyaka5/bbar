import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''класс для представления одного противника'''
    def __init__(self, ai_game):
        '''инициализирует чувака и задает его начальную позицию'''
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings

        '''загрузка изображения'''
        self.image=pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()

        '''каждый новый противник появляется в левом верхнем углу экрана'''
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        '''сохранение точной горизонтальной позиции прищельца'''
        self.x=float(self.rect.x)

    def check_edges(self):
        '''возвращает True если противник находится у края экрана'''
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True

    def update(self):
        '''перемещение вправо или влево'''
        self.x+=(self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x=self.x