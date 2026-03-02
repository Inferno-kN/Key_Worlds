import pygame
from configs.config import *


class Flask:
    def __init__(self, x, y, color, number, letter):
        self.__rect = pygame.Rect(x, y, 40, 60)
        self.__color = color
        self.__number = number
        self.__letter = letter
        self.__selected = False
        self.__solved = False
        self.__sprite = None
        self.__create_sprite()


    def __create_sprite(self):
        self.__sprite = pygame.Surface((40, 60))
        self.__sprite.set_colorkey(BLACK)


    def draw(self, screen):
        color = self.__color if self.__solved else (100, 100, 100)
        pygame.draw.rect(screen, color, (self.__rect.x, self.__rect.y, 30, 40))
        pygame.draw.ellipse(screen, color, (self.__rect.x, self.__rect.y - 5, 30, 10))
        pygame.draw.rect(screen, color, (self.__rect.x + 10, self.__rect.y - 15, 10, 15))
        pygame.draw.rect(screen, self.__color, (self.__rect.x + 5, self.__rect.y + 10, 20, 25))

        # Номер и буква
        font = pygame.font.Font(None, 16)
        number_text = font.render(str(self.__number), True, WHITE)
        screen.blit(number_text, (self.__rect.x + 12, self.__rect.y + 5))

        font_big = pygame.font.Font(None, 24)
        letter_text = font_big.render(self.__letter, True, WHITE)
        screen.blit(letter_text, (self.__rect.x + 12, self.__rect.y + 30))

        if self.__selected:
            pygame.draw.rect(screen, YELLOW, self.__rect, 3)


    def draw_with_offset(self, screen, rect):
        color = self.__color if self.__solved else (100, 100, 100)
        pygame.draw.rect(screen, color, (rect.x, rect.y, 30, 40))
        pygame.draw.ellipse(screen, color, (rect.x, rect.y - 5, 30, 10))
        pygame.draw.rect(screen, color, (rect.x + 10, rect.y - 15, 10, 15))
        pygame.draw.rect(screen, self.__color, (rect.x + 5, rect.y + 10, 20, 25))

        font = pygame.font.Font(None, 16)
        number_text = font.render(str(self.__number), True, WHITE)
        screen.blit(number_text, (rect.x + 12, rect.y + 5))

        font_big = pygame.font.Font(None, 24)
        letter_text = font_big.render(self.__letter, True, WHITE)
        screen.blit(letter_text, (rect.x + 12, rect.y + 30))

        if self.__selected:
            pygame.draw.rect(screen, YELLOW, rect, 3)


    def get_rect(self):
        return self.__rect


    def get_number(self):
        return self.__number


    def select(self):
        self.__selected = True


    def deselect(self):
        self.__selected = False


    def solve(self):
        self.__solved = True