import pygame
from configs.config import BROWN, DARK_BROWN


class Wall:
    def __init__(self, x, y, width, height):
        self.__rect = pygame.Rect(x, y, width, height)
        self.__sprite = self.__create_sprite()

    def __create_sprite(self):
        surf = pygame.Surface((self.__rect.width, self.__rect.height))
        surf.fill(BROWN)

        brick_w = 40
        brick_h = 15

        for y in range(0, self.__rect.height, brick_h):
            offset = (y // brick_h % 2) * (brick_w // 2)
            for x in range(-offset, self.__rect.width, brick_w):
                brick_rect = pygame.Rect(x, y, brick_w - 4, brick_h - 2)
                pygame.draw.rect(surf, DARK_BROWN, brick_rect)
                pygame.draw.rect(surf, (150, 100, 50), brick_rect, 1)

        return surf

    def draw(self, screen):
        screen.blit(self.__sprite, self.__rect)

    def draw_with_offset(self, screen, rect):
        screen.blit(self.__sprite, rect)

    def get_rect(self):
        return self.__rect