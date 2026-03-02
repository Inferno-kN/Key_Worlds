import pygame
from configs.config import *


class Girl:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__player_width = PLAYER_SIZE
        self.__player_height = PLAYER_SIZE
        self.__player_speed = PLAYER_SPEED
        self.__rect = pygame.Rect(x, y, self.__player_width, self.__player_height)
        self.__direction = "down"
        self.__is_moving = False
        self.__frame = 0
        self.__animation_speed = 0.2
        self.__sprites = None
        self.create_sprites()


    def create_sprites(self):
        self.__sprites = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        skin_color = (255, 220, 180)
        hair_color = (255, 200, 150)
        dress_color = (255, 150, 200)
        shoe_color = (80, 40, 20)

        for direction in self.__sprites.keys():
            for frame_num in range(4):
                surf = pygame.Surface((self.__player_width, self.__player_height))
                surf.fill(SKY_BLUE)
                surf.set_colorkey(SKY_BLUE)

                leg_offset = 0
                if frame_num == 1:
                    leg_offset = 2
                elif frame_num == 2:
                    leg_offset = 0
                elif frame_num == 3:
                    leg_offset = -2

                if direction == "down":
                    pygame.draw.rect(surf, dress_color, (10, 12, 12, 16))
                    pygame.draw.circle(surf, skin_color, (16, 8), 6)
                    pygame.draw.rect(surf, hair_color, (10, 2, 12, 6))
                    pygame.draw.circle(surf, BLACK, (12, 8), 2)
                    pygame.draw.circle(surf, BLACK, (20, 8), 2)
                    pygame.draw.arc(surf, RED, (12, 10, 8, 4), 0, 3.14, 2)
                    pygame.draw.rect(surf, shoe_color, (8, 28, 5, 4))
                    pygame.draw.rect(surf, shoe_color, (19, 28, 5, 4))
                    pygame.draw.line(surf, skin_color, (6, 18), (6, 24), 2)
                    pygame.draw.line(surf, skin_color, (26, 18), (26, 24), 2)

                elif direction == "up":
                    pygame.draw.rect(surf, dress_color, (10, 12, 12, 16))
                    pygame.draw.circle(surf, skin_color, (16, 8), 6)
                    pygame.draw.rect(surf, hair_color, (8, 2, 16, 8))
                    pygame.draw.rect(surf, shoe_color, (8, 28, 5, 4))
                    pygame.draw.rect(surf, shoe_color, (19, 28, 5, 4))
                    pygame.draw.line(surf, skin_color, (6, 18), (6, 22), 2)
                    pygame.draw.line(surf, skin_color, (26, 18), (26, 22), 2)

                elif direction == "left":
                    pygame.draw.rect(surf, dress_color, (10, 12, 8, 16))
                    pygame.draw.circle(surf, skin_color, (12, 8), 6)
                    pygame.draw.rect(surf, hair_color, (6, 2, 10, 6))
                    pygame.draw.circle(surf, BLACK, (10, 8), 2)
                    pygame.draw.rect(surf, shoe_color, (6 + leg_offset, 28, 5, 4))
                    pygame.draw.rect(surf, shoe_color, (16 - leg_offset, 28, 5, 4))
                    pygame.draw.line(surf, skin_color, (6, 18), (4, 24), 2)
                    pygame.draw.line(surf, skin_color, (18, 18), (20, 24), 2)

                else:
                    pygame.draw.rect(surf, dress_color, (14, 12, 8, 16))
                    pygame.draw.circle(surf, skin_color, (20, 8), 6)
                    pygame.draw.rect(surf, hair_color, (16, 2, 10, 6))
                    pygame.draw.circle(surf, BLACK, (22, 8), 2)
                    pygame.draw.rect(surf, shoe_color, (10 + leg_offset, 28, 5, 4))
                    pygame.draw.rect(surf, shoe_color, (20 - leg_offset, 28, 5, 4))
                    pygame.draw.line(surf, skin_color, (14, 18), (12, 24), 2)
                    pygame.draw.line(surf, skin_color, (26, 18), (28, 24), 2)

                self.__sprites[direction].append(surf)


    def move(self, dx, dy, walls):
        self.__is_moving = (dx != 0 or dy != 0)

        if dx > 0:
            self.__direction = "right"
        elif dx < 0:
            self.__direction = "left"
        elif dy > 0:
            self.__direction = "down"
        elif dy < 0:
            self.__direction = "up"

        self.__x += dx
        self.__rect.x = self.__x
        self.__y += dy
        self.__rect.y = self.__y

        for wall in walls:
            if self.__rect.colliderect(wall):
                if dx > 0:
                    self.__rect.right = wall.left
                elif dx < 0:
                    self.__rect.left = wall.right
                self.__x = self.__rect.x

        for wall in walls:
            if self.__rect.colliderect(wall):
                if dy > 0:
                    self.__rect.bottom = wall.top
                elif dy < 0:
                    self.__rect.top = wall.bottom
                self.__y = self.__rect.y


    def update(self):
        if self.__is_moving:
            self.__frame += self.__animation_speed
            if self.__frame >= 4:
                self.__frame = 0


    def draw_player(self, screen):
        frame_index = int(self.__frame)
        screen.blit(
            self.__sprites[self.__direction][frame_index],
            (self.__x, self.__y)
        )


    def draw_with_offset(self, screen, rect):
        frame_index = int(self.__frame)
        screen.blit(
            self.__sprites[self.__direction][frame_index],
            rect
        )


    def get_rect(self):
        return self.__rect


    def get_speed(self):
        return self.__player_speed


    def set_position(self, x, y):
        self.__x = x
        self.__y = y
        self.__rect.x = x
        self.__rect.y = y