import pygame
from configs.config import *


class Note:
    def __init__(self, x, y, text, digit):
        self.__rect = pygame.Rect(x, y, 25, 25)
        self.__text = text
        self.__digit = digit
        self.__collected = False
        self.__pulse = 0
        self.__pulse_dir = 1

    def update(self):
        self.__pulse += self.__pulse_dir * 2
        if self.__pulse >= 10:
            self.__pulse_dir = -1
        elif self.__pulse <= 0:
            self.__pulse_dir = 1

    def draw(self, screen):
        if not self.__collected:
            # Бумажка мерцает
            color = (255, 255, 200) if self.__pulse > 5 else (200, 200, 150)
            pygame.draw.rect(screen, color, self.__rect)
            pygame.draw.rect(screen, BLACK, self.__rect, 2)

            # Цифра на бумажке
            font = pygame.font.Font(None, 20)
            digit_text = font.render(str(self.__digit), True, BLACK)
            screen.blit(digit_text, (self.__rect.x + 8, self.__rect.y + 5))

            # Значок бумаги
            pygame.draw.line(screen, BLACK,
                             (self.__rect.x + 18, self.__rect.y + 5),
                             (self.__rect.x + 18, self.__rect.y + 18), 2)

    def draw_with_offset(self, screen, rect):
        if not self.__collected:
            color = (255, 255, 200) if self.__pulse > 5 else (200, 200, 150)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            font = pygame.font.Font(None, 20)
            digit_text = font.render(str(self.__digit), True, BLACK)
            screen.blit(digit_text, (rect.x + 8, rect.y + 5))

            pygame.draw.line(screen, BLACK,
                             (rect.x + 18, rect.y + 5),
                             (rect.x + 18, rect.y + 18), 2)

    def get_rect(self):
        return self.__rect

    def collect(self):
        self.__collected = True
        return self.__digit

    def is_collected(self):
        return self.__collected

    def get_digit(self):
        return self.__digit