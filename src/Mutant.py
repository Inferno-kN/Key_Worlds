import pygame
import math
import random
from configs.config import *


class Mutant:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__speed = 1.5
        self.__size = 32
        self.__rect = pygame.Rect(x, y, self.__size, self.__size)

        self.__patrol_points = [
            (x + 200, y + 200),
            (x - 200, y + 300),
            (x - 300, y - 200),
            (x + 300, y - 300)
        ]
        self.__current_point = 0

        self.__state = "patrol"
        self.__sight_range = 250
        self.__last_seen = None
        self.__animation = 0
        self.__search_timer = 0
        self.__confused = False


    def __can_see_player(self, player_rect, walls):
        dx = player_rect.x - self.__x
        dy = player_rect.y - self.__y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist > self.__sight_range:
            return False

        steps = int(dist / 10)
        for i in range(1, steps):
            check_x = self.__x + (dx / steps) * i
            check_y = self.__y + (dy / steps) * i
            check_rect = pygame.Rect(check_x, check_y, 5, 5)

            for wall in walls:
                if check_rect.colliderect(wall):
                    return False
        return True


    def __move_towards(self, target_x, target_y, walls):
        dx = target_x - self.__x
        dy = target_y - self.__y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist < 10:
            return True

        new_x = self.__x + (dx / dist) * self.__speed
        new_y = self.__y + (dy / dist) * self.__speed

        new_rect = pygame.Rect(new_x, new_y, self.__size, self.__size)

        for wall in walls:
            if new_rect.colliderect(wall):
                self.__confused = True
                return False

        self.__x = new_x
        self.__y = new_y
        self.__rect.x = self.__x
        self.__rect.y = self.__y
        self.__confused = False
        return False


    def __patrol(self, walls):
        if not self.__patrol_points:
            return

        target = self.__patrol_points[self.__current_point]
        reached = self.__move_towards(target[0], target[1], walls)

        if reached or self.__confused:
            self.__current_point = (self.__current_point + 1) % len(self.__patrol_points)
            self.__confused = False


    def update(self, player_rect, walls):
        can_see = self.__can_see_player(player_rect, walls)

        if can_see:
            self.__state = "chase"
            self.__last_seen = (player_rect.x, player_rect.y)
            self.__search_timer = 120  # Ищет 2 секунды
        else:
            if self.__state == "chase":
                self.__search_timer -= 1
                if self.__search_timer <= 0:
                    self.__state = "patrol"

        if self.__state == "chase" and self.__last_seen:
            self.__move_towards(player_rect.x, player_rect.y, walls)
        else:
            self.__patrol(walls)

        self.__animation += 0.1


    def draw(self, screen):
        glow = int(50 + 50 * math.sin(self.__animation))

        if self.__state == "chase":
            color = (200, 0, 0)
        else:
            color = (0, glow, 0)

        pygame.draw.circle(screen, color,
                           (int(self.__x + self.__size // 2),
                            int(self.__y + self.__size // 2)),
                           self.__size // 2)

        pygame.draw.circle(screen, WHITE,
                           (int(self.__x + self.__size // 3),
                            int(self.__y + self.__size // 3)), 4)
        pygame.draw.circle(screen, WHITE,
                           (int(self.__x + 2 * self.__size // 3),
                            int(self.__y + self.__size // 3)), 4)
        pygame.draw.circle(screen, BLACK,
                           (int(self.__x + self.__size // 3),
                            int(self.__y + self.__size // 3)), 2)
        pygame.draw.circle(screen, BLACK,
                           (int(self.__x + 2 * self.__size // 3),
                            int(self.__y + self.__size // 3)), 2)


    def draw_with_offset(self, screen, rect):
        glow = int(50 + 50 * math.sin(self.__animation))

        if self.__state == "chase":
            color = (200, 0, 0)
        else:
            color = (0, glow, 0)

        pygame.draw.circle(screen, color,
                           (rect.x + self.__size // 2, rect.y + self.__size // 2),
                           self.__size // 2)

        pygame.draw.circle(screen, WHITE,
                           (rect.x + self.__size // 3, rect.y + self.__size // 3), 4)
        pygame.draw.circle(screen, WHITE,
                           (rect.x + 2 * self.__size // 3, rect.y + self.__size // 3), 4)
        pygame.draw.circle(screen, BLACK,
                           (rect.x + self.__size // 3, rect.y + self.__size // 3), 2)
        pygame.draw.circle(screen, BLACK,
                           (rect.x + 2 * self.__size // 3, rect.y + self.__size // 3), 2)


    def get_rect(self):
        return self.__rect


    def check_collision(self, player_rect):
        return self.__rect.colliderect(player_rect)