import pygame
import math
from configs.config import *


class ShadowClone:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__speed = 3.5
        self.__size = 30
        self.__rect = pygame.Rect(x, y, self.__size, self.__size)
        self.__color = (50, 50, 80)
        self.__animation = 0


    def update(self, player_rect, walls):
        dx = player_rect.x - self.__x
        dy = player_rect.y - self.__y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist > 5:
            new_x = self.__x + (dx / dist) * self.__speed
            new_y = self.__y + (dy / dist) * self.__speed
            new_rect = pygame.Rect(new_x, new_y, self.__size, self.__size)
            collision = False
            for wall in walls:
                if new_rect.colliderect(wall):
                    collision = True
                    break

            if not collision:
                self.__x = new_x
                self.__y = new_y

        self.__rect.x = self.__x
        self.__rect.y = self.__y
        self.__animation += 0.2


    def draw(self, screen):
        pulse = int(50 + 50 * math.sin(self.__animation))
        color = (50 + pulse // 3, 50 + pulse // 3, 100)

        pygame.draw.circle(screen, color,
                           (int(self.__x + self.__size // 2),
                            int(self.__y + self.__size // 2)),
                           self.__size // 2)

        pygame.draw.circle(screen, RED,
                           (int(self.__x + self.__size // 3),
                            int(self.__y + self.__size // 3)), 3)
        pygame.draw.circle(screen, RED,
                           (int(self.__x + 2 * self.__size // 3),
                            int(self.__y + self.__size // 3)), 3)
        pygame.draw.circle(screen, BLACK,
                           (int(self.__x + self.__size // 3),
                            int(self.__y + self.__size // 3)), 1)
        pygame.draw.circle(screen, BLACK,
                           (int(self.__x + 2 * self.__size // 3),
                            int(self.__y + self.__size // 3)), 1)


    def draw_with_offset(self, screen, rect):
        pulse = int(50 + 50 * math.sin(self.__animation))
        color = (50 + pulse // 3, 50 + pulse // 3, 100)

        pygame.draw.circle(screen, color,
                           (rect.x + self.__size // 2, rect.y + self.__size // 2),
                           self.__size // 2)

        pygame.draw.circle(screen, RED,
                           (rect.x + self.__size // 3, rect.y + self.__size // 3), 3)
        pygame.draw.circle(screen, RED,
                           (rect.x + 2 * self.__size // 3, rect.y + self.__size // 3), 3)
        pygame.draw.circle(screen, BLACK,
                           (rect.x + self.__size // 3, rect.y + self.__size // 3), 1)
        pygame.draw.circle(screen, BLACK,
                           (rect.x + 2 * self.__size // 3, rect.y + self.__size // 3), 1)


    def get_rect(self):
        return self.__rect


    def check_collision(self, player_rect):
        return self.__rect.colliderect(player_rect)