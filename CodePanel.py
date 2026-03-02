import pygame
from configs.config import *


class CodePanel:
    def __init__(self, x, y, code):
        self.__rect = pygame.Rect(x, y, 200, 100)
        self.__code = code
        self.__input = []
        self.__solved = False
        self.__sprite = None
        self.__create_sprite()


    def __create_sprite(self):
        self.__sprite = pygame.Surface((200, 100))
        self.__sprite.set_colorkey(BLACK)


    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.__rect)
        pygame.draw.rect(screen, WHITE, self.__rect, 3)

        font = pygame.font.Font(None, 36)
        input_text = font.render(''.join(map(str, self.__input)), True, YELLOW)
        screen.blit(input_text, (self.__rect.x + 20, self.__rect.y + 30))

        hint_font = pygame.font.Font(None, 20)
        hint = hint_font.render("Нажми цифры 1-4", True, WHITE)
        screen.blit(hint, (self.__rect.x + 20, self.__rect.y + 70))

        if self.__solved:
            done_text = font.render("✅ КОД ПРИНЯТ", True, GREEN)
            screen.blit(done_text, (self.__rect.x + 20, self.__rect.y + 100))


    def draw_with_offset(self, screen, rect):
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 3)

        font = pygame.font.Font(None, 36)
        input_text = font.render(''.join(map(str, self.__input)), True, YELLOW)
        screen.blit(input_text, (rect.x + 20, rect.y + 30))

        hint_font = pygame.font.Font(None, 20)
        hint = hint_font.render("Нажми цифры 1-4", True, WHITE)
        screen.blit(hint, (rect.x + 20, rect.y + 70))

        if self.__solved:
            done_text = font.render("✅ КОД ПРИНЯТ", True, GREEN)
            screen.blit(done_text, (rect.x + 20, rect.y + 100))


    def add_digit(self, digit):
        if not self.__solved and len(self.__input) < 4:
            self.__input.append(digit)
            if len(self.__input) == 4:
                self.check_code()


    def check_code(self):
        if self.__input == self.__code:
            self.__solved = True
            return True
        else:
            self.__input = []
            return False


    def is_solved(self):
        return self.__solved


    def get_rect(self):
        return self.__rect