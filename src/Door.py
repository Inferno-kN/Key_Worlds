import pygame
from configs.config import *


class Door:
    def __init__(self, x, y, door_id: int, color: tuple, target_room: str):
        self.__id = door_id
        self.__color = color
        self.__target_room = target_room
        self.__locked = False

        if color == (139, 69, 19):
            self.__width = 5
            self.__height = 32
        else:
            self.__width = TILE_SIZE
            self.__height = TILE_SIZE

        self.__rect = pygame.Rect(x, y, self.__width, self.__height)
        self.__sprite = self.__create_sprite()

    def __create_sprite(self):
        if self.__color == (139, 69, 19):
            surf = pygame.Surface((self.__width, self.__height))
            surf.fill((139, 69, 19))
            brick_w = 8
            brick_h = 8

            for y in range(0, self.__height, brick_h):
                offset = (y // brick_h % 2) * (brick_w // 2)
                for x in range(-offset, self.__width, brick_w):
                    brick_rect = pygame.Rect(x, y, brick_w - 2, brick_h - 2)
                    pygame.draw.rect(surf, (101, 67, 33), brick_rect, 1)
            return surf

        surf = pygame.Surface((self.__width, self.__height))
        surf.fill(self.__color)

        if self.__color == RED:
            handle_color = (200, 100, 100)
        elif self.__color == BLUE:
            handle_color = (100, 100, 200)
        elif self.__color == GREEN:
            handle_color = (100, 200, 100)
        elif self.__color == PURPLE:
            handle_color = (200, 100, 200)
        elif self.__color == GOLD:
            handle_color = (255, 215, 0)
        else:
            handle_color = (100, 100, 100)

        pygame.draw.circle(surf, handle_color, (self.__width // 2, self.__height // 2), 5)

        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)

        return surf


    def draw(self, screen):
        screen.blit(self.__sprite, self.__rect)
        if self.__locked:
            lock_x = self.__rect.x + self.__width // 2 - 8
            lock_y = self.__rect.y + self.__height - 16
            pygame.draw.rect(screen, (50, 50, 50), (lock_x, lock_y, 12, 8))
            pygame.draw.circle(screen, (100, 100, 100), (lock_x + 6, lock_y - 4), 4)


    def draw_with_offset(self, screen, rect):
        screen.blit(self.__sprite, rect)
        if self.__locked:
            lock_x = rect.x + self.__width // 2 - 8
            lock_y = rect.y + self.__height - 16
            pygame.draw.rect(screen, (50, 50, 50), (lock_x, lock_y, 12, 8))
            pygame.draw.circle(screen, (100, 100, 100), (lock_x + 6, lock_y - 4), 4)


    def get_rect(self):
        return self.__rect


    def get_target_room(self):
        return self.__target_room


    def get_id(self):
        return self.__id


    def is_locked(self):
        return self.__locked


    def lock(self):
        self.__locked = True


    def unlock(self):
        self.__locked = False