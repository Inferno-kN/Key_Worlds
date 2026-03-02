import pygame
import math
import random
from configs.config import *


class Enemy:
    def __init__(self, x, y, speed, color, size):
        self.__x = x
        self.__y = y
        self.__base_speed = speed
        self.__speed = speed
        self.__color = color
        self.__size = size
        self.__rect = pygame.Rect(x, y, size, size)

        self.__patrol_points = []
        for _ in range(4):
            px = x + random.randint(-300, 300)
            py = y + random.randint(-300, 300)
            px = max(50, min(px, 1950))
            py = max(50, min(py, 1950))
            self.__patrol_points.append((px, py))

        self.__current_point = 0
        self.__state = "patrol"
        self.__sight_range = 250
        self.__last_seen = None
        self.__animation = 0
        self.__wait_timer = 0
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

        current_speed = self.__speed

        new_x = self.__x + (dx / dist) * current_speed
        new_y = self.__y + (dy / dist) * current_speed

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
        self.__speed = self.__base_speed * 0.7  # Медленнее при патруле

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
            self.__wait_timer = 90  # Ищет 1.5 секунды
            self.__speed = self.__base_speed * 1.5  # БЫСТРЕЕ ИГРОКА!
        else:
            if self.__state == "chase":
                self.__wait_timer -= 1
                if self.__wait_timer <= 0:
                    self.__state = "search"
                    self.__search_timer = 60
            elif self.__state == "search":
                self.__search_timer -= 1
                if self.__search_timer <= 0:
                    self.__state = "patrol"

        if self.__state == "chase":
            self.__move_towards(player_rect.x, player_rect.y, walls)
        elif self.__state == "search" and self.__last_seen:
            self.__speed = self.__base_speed
            self.__move_towards(self.__last_seen[0], self.__last_seen[1], walls)
        else:
            self.__patrol(walls)

        self.__animation += 0.1


    def draw(self, screen):
        pulse = int(50 + 50 * math.sin(self.__animation))

        if self.__state == "chase":
            color = (200, 50, 50)
        elif self.__state == "search":
            color = (200, 150, 50)
        else:
            color = (self.__color[0], self.__color[1] + pulse // 5, self.__color[2])  # Обычный

        pygame.draw.circle(screen, color,
                           (int(self.__x + self.__size // 2),
                            int(self.__y + self.__size // 2)),
                           self.__size // 2)

        eye_color = RED if self.__state == "chase" else WHITE
        pygame.draw.circle(screen, eye_color,
                           (int(self.__x + self.__size // 3),
                            int(self.__y + self.__size // 3)), 3)
        pygame.draw.circle(screen, eye_color,
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

        if self.__state == "chase":
            color = (200, 50, 50)
        elif self.__state == "search":
            color = (200, 150, 50)
        else:
            color = self.__color

        pygame.draw.circle(screen, color,
                           (rect.x + self.__size // 2, rect.y + self.__size // 2),
                           self.__size // 2)

        eye_color = RED if self.__state == "chase" else WHITE
        pygame.draw.circle(screen, eye_color,
                           (rect.x + self.__size // 3, rect.y + self.__size // 3), 3)
        pygame.draw.circle(screen, eye_color,
                           (rect.x + 2 * self.__size // 3, rect.y + self.__size // 3), 3)
        pygame.draw.circle(screen, BLACK,
                           (rect.x + self.__size // 3, rect.y + self.__size // 3), 1)
        pygame.draw.circle(screen, BLACK,
                           (rect.x + 2 * self.__size // 3, rect.y + self.__size // 3), 1)


    def get_rect(self):
        return self.__rect


    def check_collision(self, player_rect):
        return self.__rect.colliderect(player_rect)