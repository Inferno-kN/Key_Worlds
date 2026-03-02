import pygame
from configs.config import *


class Firefly:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__width = 16
        self.__height = 16
        self.__rect = pygame.Rect(x, y, self.__width, self.__height)
        self.__collected = False
        self.__animation_frame = 0
        self.__animation_speed = 0.1
        self.__pulse_direction = 1
        self.__brightness = 255
        self.__sprite = None
        self.__create_sprite()


    def __create_sprite(self):
        self.__sprite = pygame.Surface((self.__width, self.__height))
        self.__sprite.set_colorkey(BLACK)


    def update(self):
        if not self.__collected:
            self.__animation_frame += self.__animation_speed
            if self.__animation_frame >= 4:
                self.__animation_frame = 0

            self.__brightness += self.__pulse_direction * 5
            if self.__brightness >= 255:
                self.__brightness = 255
                self.__pulse_direction = -1
            elif self.__brightness <= 150:
                self.__brightness = 150
                self.__pulse_direction = 1


    def draw(self, screen):
        if not self.__collected:
            color = (255, self.__brightness, 100)
            pygame.draw.circle(screen, color,
                               (self.__x + 8, self.__y + 8), 6)
            if int(self.__animation_frame) % 2 == 0:
                pygame.draw.ellipse(screen, (200, 255, 200),
                                    (self.__x + 2, self.__y + 2, 5, 8))
                pygame.draw.ellipse(screen, (200, 255, 200),
                                    (self.__x + 9, self.__y + 2, 5, 8))
            pygame.draw.circle(screen, BLACK, (self.__x + 6, self.__y + 6), 1)
            pygame.draw.circle(screen, BLACK, (self.__x + 10, self.__y + 6), 1)


    def draw_with_offset(self, screen, rect):
        if not self.__collected:
            color = (255, self.__brightness, 100)
            pygame.draw.circle(screen, color,
                               (rect.x + 8, rect.y + 8), 6)
            if int(self.__animation_frame) % 2 == 0:
                pygame.draw.ellipse(screen, (200, 255, 200),
                                    (rect.x + 2, rect.y + 2, 5, 8))
                pygame.draw.ellipse(screen, (200, 255, 200),
                                    (rect.x + 9, rect.y + 2, 5, 8))
            pygame.draw.circle(screen, BLACK, (rect.x + 6, rect.y + 6), 1)
            pygame.draw.circle(screen, BLACK, (rect.x + 10, rect.y + 6), 1)


    def get_rect(self):
        return self.__rect


    def collect(self):
        self.__collected = True
        return True


    def is_collected(self):
        return self.__collected


    def set_collected(self, value):
        self.__collected = value