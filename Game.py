import math
import pygame
import random
from configs.config import *
from src.Player import Girl
from src.Wall import Wall
from src.Door import Door
from src.Firefly import Firefly
from src.Note import Note
from src.Mutant import Mutant
from src.Enemy import Enemy
from src.ShadowClone import ShadowClone


class Game:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Keys of the World")
        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__frame_count = 0
        self.__current_room = "hub"
        self.__keys_collected = []
        self.__collected_fireflies = 0
        self.__fireflies = []
        self.__notes = []
        self.__collected_notes = []
        self.__notes_collected_count = 0
        self.__terminal = None
        self.__terminal_active = False
        self.__player_input = []
        self.__lab_code = [2, 4, 1, 3]
        self.__memories = []
        self.__collected_memories = 0
        self.__music_notes = []
        self.__collected_notes_music = 0
        self.__melody = [1, 3, 5, 2, 4, 6, 7]
        self.__music_panel = None
        self.__music_panel_active = False
        self.__secret_wall = None
        self.__player = None
        self.__walls = []
        self.__doors = []
        self.__enemies = []
        self.__level_width = WIDTH
        self.__level_height = HEIGHT
        self.__camera_x = 0
        self.__camera_y = 0
        self.__show_hint = False
        self.__hint_timer = 0
        self.__particles = []
        self.__final_timer = 0
        self.load_room("hub")


    def load_room(self, room_name):
        self.__current_room = room_name
        if room_name == "hub":
            self.load_hub()
        elif room_name == "forest":
            self.load_forest()
        elif room_name == "lab":
            self.load_lab()
        elif room_name == "memory":
            self.load_memory()
        elif room_name == "music":
            self.load_music()
        elif room_name == "final":
            self.load_final()
        elif room_name == "secret":
            self.load_secret()


    def load_hub(self):
        self.__camera_x = 0
        self.__camera_y = 0
        self.__level_width = WIDTH
        self.__level_height = HEIGHT
        self.__walls = []
        self.__doors = []
        self.__enemies = []
        self.__fireflies = []
        self.__notes = []
        self.__memories = []
        self.__music_notes = []

        if not self.__player:
            self.__player = Girl(WIDTH // 2, HEIGHT // 2)
        else:
            self.__player.set_position(WIDTH // 2, HEIGHT // 2)

        self.__walls = [
            Wall(0, 0, WIDTH, 10),
            Wall(0, HEIGHT - 10, WIDTH, 10),
            Wall(0, 0, 10, HEIGHT),
            Wall(WIDTH - 10, 0, 10, HEIGHT),
        ]

        self.__doors = [
            Door(150, 250, 0, DOOR_COLORS["forest"], "forest"),
            Door(350, 250, 1, DOOR_COLORS["lab"], "lab"),
            Door(550, 250, 2, DOOR_COLORS["memory"], "memory"),
            Door(400, 450, 3, DOOR_COLORS["music"], "music"),
            Door(500, 350, 4, GOLD, "final"),
            Door(776, 300, 5, (139, 69, 19), "secret"),
        ]

        self.__secret_wall = pygame.Rect(800, 100, 32, 400)

        for door in self.__doors:
            if door.get_target_room() == "final":
                if len(self.__keys_collected) >= 4:
                    door.unlock()
                    print("🏆 Финальная дверь открыта!")
                else:
                    door.lock()
            elif door.get_target_room() in self.__keys_collected:
                door.lock()
            else:
                door.unlock()


    def load_final(self):
        self.__level_width = WIDTH
        self.__level_height = HEIGHT
        self.__camera_x = 0
        self.__camera_y = 0

        self.__walls = []
        self.__doors = []
        self.__enemies = []
        self.__fireflies = []
        self.__notes = []
        self.__memories = []
        self.__music_notes = []
        self.__particles = []

        for _ in range(50):
            self.__particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(1, 3),
                'color': (random.randint(200, 255),
                          random.randint(100, 200),
                          random.randint(100, 255))
            })

        self.__final_timer = 0
        self.__player.set_position(WIDTH // 2, HEIGHT // 2)
        self.__show_hint = True
        self.__hint_timer = 300


    def load_secret(self):
        self.__current_room = "secret"
        self.__level_width = WIDTH
        self.__level_height = HEIGHT
        self.__camera_x = 0
        self.__camera_y = 0

        self.__walls = []
        self.__doors = []
        self.__enemies = []

        self.__player.set_position(100, 100)
        self.__show_hint = True
        self.__hint_timer = 180


    def load_forest(self):
        self.__level_width = 2000
        self.__level_height = 2000
        self.__camera_x = 0
        self.__camera_y = 0

        self.__walls = [
            Wall(0, 0, self.__level_width, 10),
            Wall(0, self.__level_height - 10, self.__level_width, 10),
            Wall(0, 0, 10, self.__level_height),
            Wall(self.__level_width - 10, 0, 10, self.__level_height),
        ]

        tree_positions = [
            (300, 200), (600, 300), (900, 400), (1200, 300), (1500, 200),
            (200, 500), (500, 600), (800, 700), (1100, 600), (1400, 500),
            (400, 800), (700, 900), (1000, 1000), (1300, 900), (1600, 800),
            (300, 1100), (600, 1200), (900, 1300), (1200, 1200), (1500, 1100),
            (200, 1400), (500, 1500), (800, 1600), (1100, 1500), (1400, 1400),
            (400, 1700), (700, 1800), (1000, 1800), (1300, 1700), (1600, 1600),
        ]

        for x, y in tree_positions:
            self.__walls.append(Wall(x, y, 40, 40))

        self.__fireflies = []
        for _ in range(10):
            attempts = 0
            while attempts < 100:
                x = random.randint(100, self.__level_width - 100)
                y = random.randint(100, self.__level_height - 100)
                new_rect = pygame.Rect(x, y, 16, 16)
                collision = False
                for wall in self.__walls:
                    if new_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    self.__fireflies.append(Firefly(x, y))
                    break
                attempts += 1

        self.__enemies = []
        num_enemies = random.randint(2, 3)
        for _ in range(num_enemies):
            attempts = 0
            while attempts < 100:
                x = random.randint(200, self.__level_width - 200)
                y = random.randint(200, self.__level_height - 200)
                enemy_rect = pygame.Rect(x, y, 30, 30)
                collision = False
                for wall in self.__walls:
                    if enemy_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                player_start = (100, 100)
                dist_to_player = math.sqrt((x - player_start[0]) ** 2 + (y - player_start[1]) ** 2)
                if not collision and dist_to_player > 300:
                    self.__enemies.append(Enemy(x, y, 3, (100, 100, 100), 30))
                    break
                attempts += 1

        if len(self.__enemies) < 1:
            safe_spawns = [(500, 500), (1500, 1500), (800, 1200)]
            for spawn_x, spawn_y in safe_spawns:
                enemy_rect = pygame.Rect(spawn_x, spawn_y, 30, 30)
                collision = False
                for wall in self.__walls:
                    if enemy_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    self.__enemies.append(Enemy(spawn_x, spawn_y, 3, (100, 100, 100), 30))

        self.__collected_fireflies = 0
        self.__player.set_position(100, 100)
        self.__doors = []
        self.__show_hint = True
        self.__hint_timer = 180


    def load_lab(self):
        self.__level_width = 2000
        self.__level_height = 2000
        self.__camera_x = 0
        self.__camera_y = 0

        self.__walls = [
            Wall(0, 0, self.__level_width, 10),
            Wall(0, self.__level_height - 10, self.__level_width, 10),
            Wall(0, 0, 10, self.__level_height),
            Wall(self.__level_width - 10, 0, 10, self.__level_height),
        ]

        num_walls = random.randint(15, 20)
        for _ in range(num_walls):
            x = random.randint(200, self.__level_width - 200)
            y = random.randint(200, self.__level_height - 200)
            w = random.randint(100, 300)
            h = random.randint(20, 40)
            new_wall = Wall(x, y, w, h)
            collision = False
            for wall in self.__walls:
                if new_wall.get_rect().colliderect(wall.get_rect()):
                    collision = True
                    break
            if not collision:
                self.__walls.append(new_wall)

        self.__notes = []
        note_data = [
            (2, "Первая цифра - 2"),
            (4, "Вторая цифра - 4"),
            (1, "Третья цифра - 1"),
            (3, "Четвертая цифра - 3"),
            (5, "Код: 2,4,1,3"),
        ]
        for digit, text in note_data:
            attempts = 0
            while attempts < 100:
                x = random.randint(100, self.__level_width - 100)
                y = random.randint(100, self.__level_height - 100)
                new_rect = pygame.Rect(x, y, 25, 25)
                collision = False
                for wall in self.__walls:
                    if new_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    self.__notes.append(Note(x, y, text, digit))
                    break
                attempts += 1

        self.__enemies = []
        num_mutants = random.randint(2, 4)
        for _ in range(num_mutants):
            attempts = 0
            while attempts < 100:
                x = random.randint(200, self.__level_width - 200)
                y = random.randint(200, self.__level_height - 200)
                mutant_rect = pygame.Rect(x, y, 32, 32)
                collision = False
                for wall in self.__walls:
                    if mutant_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                too_close = False
                for enemy in self.__enemies:
                    ex, ey = enemy.get_rect().x, enemy.get_rect().y
                    if math.sqrt((x - ex) ** 2 + (y - ey) ** 2) < 200:
                        too_close = True
                        break
                if not collision and not too_close:
                    self.__enemies.append(Mutant(x, y))
                    break
                attempts += 1

        if len(self.__enemies) < 1:
            safe_spawns = [(500, 500), (1500, 1500), (1000, 1000)]
            for spawn_x, spawn_y in safe_spawns:
                mutant_rect = pygame.Rect(spawn_x, spawn_y, 32, 32)
                collision = False
                for wall in self.__walls:
                    if mutant_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    self.__enemies.append(Mutant(spawn_x, spawn_y))

        terminal_x = random.randint(800, 1200)
        terminal_y = random.randint(800, 1200)
        self.__terminal = pygame.Rect(terminal_x, terminal_y, 100, 80)
        self.__collected_notes = []
        self.__notes_collected_count = 0
        self.__player_input = []
        self.__terminal_active = False
        self.__player.set_position(100, 100)
        self.__doors = []
        self.__show_hint = True
        self.__hint_timer = 240


    def load_memory(self):
        self.__level_width = 2000
        self.__level_height = 2000
        self.__camera_x = 0
        self.__camera_y = 0

        self.__walls = [
            Wall(0, 0, self.__level_width, 10),
            Wall(0, self.__level_height - 10, self.__level_width, 10),
            Wall(0, 0, 10, self.__level_height),
            Wall(self.__level_width - 10, 0, 10, self.__level_height),
        ]

        for _ in range(20):
            x = random.randint(200, self.__level_width - 200)
            y = random.randint(200, self.__level_height - 200)
            self.__walls.append(Wall(x, y, 30, 30))

        self.__memories = []
        memory_positions = []
        for i in range(5):
            attempts = 0
            while attempts < 100:
                x = random.randint(100, self.__level_width - 100)
                y = random.randint(100, self.__level_height - 100)
                new_rect = pygame.Rect(x, y, 25, 25)
                collision = False
                for wall in self.__walls:
                    if new_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    memory_positions.append((x, y))
                    break
                attempts += 1

        from src.Firefly import Firefly
        self.__memories = []
        for x, y in memory_positions:
            memory = Firefly(x, y)
            memory.__color = (200, 150, 255)
            self.__memories.append(memory)

        self.__collected_memories = 0
        self.__enemies = []
        num_ghosts = random.randint(2, 3)
        for _ in range(num_ghosts):
            attempts = 0
            while attempts < 100:
                x = random.randint(200, self.__level_width - 200)
                y = random.randint(200, self.__level_height - 200)
                ghost_rect = pygame.Rect(x, y, 30, 30)
                collision = False
                for wall in self.__walls:
                    if ghost_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    self.__enemies.append(Enemy(x, y, 2.5, (200, 200, 255), 30))
                    break
                attempts += 1

        self.__player.set_position(100, 100)
        self.__doors = []
        self.__show_hint = True
        self.__hint_timer = 180


    def load_music(self):
        self.__level_width = 2000
        self.__level_height = 2000
        self.__camera_x = 0
        self.__camera_y = 0

        self.__walls = [
            Wall(0, 0, self.__level_width, 10),
            Wall(0, self.__level_height - 10, self.__level_width, 10),
            Wall(0, 0, 10, self.__level_height),
            Wall(self.__level_width - 10, 0, 10, self.__level_height),
        ]

        for _ in range(10):
            x = random.randint(200, self.__level_width - 200)
            y = random.randint(200, self.__level_height - 200)
            self.__walls.append(Wall(x, y, 30, 30))

        self.__music_notes = []
        for i in range(1, 8):
            attempts = 0
            while attempts < 100:
                x = random.randint(100, self.__level_width - 100)
                y = random.randint(100, self.__level_height - 100)
                new_rect = pygame.Rect(x, y, 25, 25)
                collision = False
                for wall in self.__walls:
                    if new_rect.colliderect(wall.get_rect()):
                        collision = True
                        break
                if not collision:
                    from src.Firefly import Firefly
                    note = Firefly(x, y)
                    note.__color = GOLD
                    note.__note_num = i
                    self.__music_notes.append(note)
                    break
                attempts += 1

        self.__enemies = []
        self.__enemies.append(ShadowClone(1000, 1000))
        self.__music_panel = pygame.Rect(900, 900, 150, 80)
        self.__music_panel_active = False
        self.__collected_notes_music = 0
        self.__player.set_position(100, 100)
        self.__doors = []
        self.__show_hint = True
        self.__hint_timer = 180


    def get_wall_rects(self):
        return [wall.get_rect() for wall in self.__walls]


    def update_camera(self):
        if self.__current_room in ["forest", "lab", "memory", "music"]:
            player_rect = self.__player.get_rect()
            self.__camera_x = player_rect.x - WIDTH // 2
            self.__camera_y = player_rect.y - HEIGHT // 2
            self.__camera_x = max(0, min(self.__camera_x, self.__level_width - WIDTH))
            self.__camera_y = max(0, min(self.__camera_y, self.__level_height - HEIGHT))


    def check_firefly_collection(self):
        player_rect = self.__player.get_rect()
        for firefly in self.__fireflies[:]:
            if not firefly.is_collected() and player_rect.colliderect(firefly.get_rect()):
                firefly.collect()
                self.__collected_fireflies += 1
                if self.__collected_fireflies >= 10:
                    if "forest" not in self.__keys_collected:
                        self.__keys_collected.append("forest")
                break


    def check_note_collection(self):
        player_rect = self.__player.get_rect()
        for note in self.__notes[:]:
            if not note.is_collected() and player_rect.colliderect(note.get_rect()):
                text = note.collect()
                self.__collected_notes.append(text)
                self.__notes_collected_count += 1
                break


    def check_terminal_interaction(self):
        player_rect = self.__player.get_rect()
        if player_rect.colliderect(self.__terminal):
            if self.__notes_collected_count >= 5:
                self.__terminal_active = True
                print("🔓 Терминал активирован! Введи код 2,4,1,3")
            else:
                print(f"🔒 Нужно найти все записки! ({self.__notes_collected_count}/5)")


    def check_memory_collection(self):
        player_rect = self.__player.get_rect()
        for memory in self.__memories[:]:
            if not memory.is_collected() and player_rect.colliderect(memory.get_rect()):
                memory.collect()
                self.__collected_memories += 1
                print(f"💜 Воспоминание {self.__collected_memories}/5")
                if self.__collected_memories >= 5:
                    print("🎉 Храм памяти пройден! Ключ получен!")
                    if "memory" not in self.__keys_collected:
                        self.__keys_collected.append("memory")
                break


    def check_music_note_collection(self):
        player_rect = self.__player.get_rect()
        for note in self.__music_notes[:]:
            if not note.is_collected() and player_rect.colliderect(note.get_rect()):
                note.collect()
                self.__collected_notes_music += 1
                print(f"🎵 Нота {note.__note_num} собрана ({self.__collected_notes_music}/7)")
                if self.__collected_notes_music >= 7:
                    print("🎵 Все ноты собраны! Иди к панели!")
                    self.__music_panel_active = True
                break


    def check_music_panel_interaction(self):
        player_rect = self.__player.get_rect()
        if player_rect.colliderect(self.__music_panel) and self.__music_panel_active:
            print("🎉 Музыкальная комната пройдена! Ключ получен!")
            if "music" not in self.__keys_collected:
                self.__keys_collected.append("music")
            self.__music_panel_active = False


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.__current_room != "hub":
                        self.load_room("hub")
                    else:
                        self.__running = False
                elif event.key == pygame.K_e:
                    if self.__current_room == "hub":
                        if hasattr(self, '__secret_wall'):
                            player_rect = self.__player.get_rect()
                            if player_rect.colliderect(self.__secret_wall):
                                self.load_secret()
                            else:
                                self.check_door_interaction()
                        else:
                            self.check_door_interaction()
                    elif self.__current_room == "forest":
                        self.check_firefly_collection()
                    elif self.__current_room == "lab":
                        self.check_note_collection()
                        self.check_terminal_interaction()
                    elif self.__current_room == "memory":
                        self.check_memory_collection()
                    elif self.__current_room == "music":
                        self.check_music_note_collection()
                        self.check_music_panel_interaction()
                    elif self.__current_room == "secret":
                        self.load_room("hub")
                elif self.__current_room == "lab" and self.__terminal_active:
                    if event.key == pygame.K_1:
                        self.__player_input.append(1)
                    elif event.key == pygame.K_2:
                        self.__player_input.append(2)
                    elif event.key == pygame.K_3:
                        self.__player_input.append(3)
                    elif event.key == pygame.K_4:
                        self.__player_input.append(4)

                    if len(self.__player_input) == 4:
                        if self.__player_input == self.__lab_code:
                            print("🎉 Код верный! Лаборатория пройдена!")
                            if "lab" not in self.__keys_collected:
                                self.__keys_collected.append("lab")
                            self.__terminal_active = False
                        else:
                            print("❌ Неверный код! Попробуй снова!")
                            self.__player_input = []

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.__player.get_speed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.__player.get_speed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.__player.get_speed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.__player.get_speed()
        self.__player.move(dx, dy, self.get_wall_rects())


    def check_door_interaction(self):
        player_rect = self.__player.get_rect()
        for door in self.__doors:
            if player_rect.colliderect(door.get_rect()):
                if not door.is_locked():
                    self.load_room(door.get_target_room())
                else:
                    print("Дверь заперта!")
                break


    def update(self):
        self.__frame_count += 1
        self.__player.update()
        self.update_camera()

        if self.__current_room == "forest":
            for firefly in self.__fireflies:
                firefly.update()
            for enemy in self.__enemies:
                enemy.update(self.__player.get_rect(), self.get_wall_rects())
                if enemy.check_collision(self.__player.get_rect()):
                    self.__player.set_position(100, 100)

        elif self.__current_room == "lab":
            for note in self.__notes:
                note.update()
            for enemy in self.__enemies:
                enemy.update(self.__player.get_rect(), self.get_wall_rects())
                if enemy.check_collision(self.__player.get_rect()):
                    self.__player.set_position(100, 100)
                    self.__notes_collected_count = 0
                    self.__collected_notes = []
                    self.load_lab()

        elif self.__current_room == "memory":
            for memory in self.__memories:
                memory.update()
            for enemy in self.__enemies:
                enemy.update(self.__player.get_rect(), self.get_wall_rects())
                if enemy.check_collision(self.__player.get_rect()):
                    self.__player.set_position(100, 100)

        elif self.__current_room == "music":
            for note in self.__music_notes:
                note.update()
            for enemy in self.__enemies:
                enemy.update(self.__player.get_rect(), self.get_wall_rects())
                if enemy.check_collision(self.__player.get_rect()):
                    self.__player.set_position(100, 100)
                    for note in self.__music_notes:
                        note.set_collected(False)
                    self.__collected_notes_music = 0
                    self.__music_panel_active = False


    def draw_final(self):
        for p in self.__particles:
            p['y'] += p['speed']
            if p['y'] > HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, WIDTH)
            pygame.draw.circle(self.__screen, p['color'],
                               (int(p['x']), int(p['y'])), p['size'])

        font_big = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)

        alpha = abs(math.sin(self.__final_timer * 0.05)) * 255

        title = font_big.render("ТЫ ПРОШЛА ВСЕ ИСПЫТАНИЯ", True, GOLD)
        title.set_alpha(alpha)
        self.__screen.blit(title, (WIDTH // 2 - 300, HEIGHT // 2 - 150))

        sub = font_medium.render("КЛЮЧИ МИРОВ ТЕПЕРЬ ТВОИ", True, WHITE)
        self.__screen.blit(sub, (WIDTH // 2 - 250, HEIGHT // 2 - 50))

        if self.__final_timer > 180:
            author1 = font_small.render("Поздравляю с концовкой,", True, NEON_PINK)
            author2 = font_small.render("надеюсь тебе игра понравилась, я очень старался :)", True, NEON_PINK)
            self.__screen.blit(author1, (WIDTH // 2 - 300, HEIGHT // 2 + 50))
            self.__screen.blit(author2, (WIDTH // 2 - 350, HEIGHT // 2 + 80))

        self.__final_timer += 1


    def draw_secret(self):
        self.__screen.fill((20, 0, 20))

        font_big = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)

        pulse = abs(math.sin(self.__frame_count * 0.05)) * 100 + 155

        title = font_big.render("ПОСВЯЩАЕТСЯ НАСТОЯЩЕМУ", True, (255, pulse, 0))
        self.__screen.blit(title, (WIDTH // 2 - 250, HEIGHT // 2 - 80))

        title2 = font_big.render("ДЕТЕКТИВУ ПАСХАЛОК В ИГРАХ!!!", True, (255, pulse, 0))
        self.__screen.blit(title2, (WIDTH // 2 - 280, HEIGHT // 2 - 30))

        congrats = font_medium.render("ПОЗДРАВЛЯЮ!!!", True, GOLD)
        self.__screen.blit(congrats, (WIDTH // 2 - 100, HEIGHT // 2 + 30))

        self.__player.draw_player(self.__screen)

        font_small = pygame.font.Font(None, 24)
        hint = font_small.render("ESC - выйти", True, WHITE)
        self.__screen.blit(hint, (WIDTH - 100, HEIGHT - 30))


    def draw(self):
        self.__screen.fill(BLACK)

        if self.__current_room == "final":
            self.draw_final()
            player_rect = self.__player.get_rect()
            self.__player.draw_player(self.__screen)
            pygame.display.flip()
            return
        elif self.__current_room == "secret":
            self.draw_secret()
            pygame.display.flip()
            return

        camera_offset = (self.__camera_x, self.__camera_y)

        for wall in self.__walls:
            wall_rect = wall.get_rect()
            shifted_rect = wall_rect.move(-camera_offset[0], -camera_offset[1])
            wall.draw_with_offset(self.__screen, shifted_rect)

        for door in self.__doors:
            door_rect = door.get_rect()
            shifted_rect = door_rect.move(-camera_offset[0], -camera_offset[1])
            door.draw_with_offset(self.__screen, shifted_rect)

        if self.__current_room == "forest":
            for firefly in self.__fireflies:
                firefly_rect = firefly.get_rect()
                shifted_rect = firefly_rect.move(-camera_offset[0], -camera_offset[1])
                firefly.draw_with_offset(self.__screen, shifted_rect)
            for enemy in self.__enemies:
                enemy_rect = enemy.get_rect()
                shifted_rect = enemy_rect.move(-camera_offset[0], -camera_offset[1])
                enemy.draw_with_offset(self.__screen, shifted_rect)
            font = pygame.font.Font(None, 24)
            counter = font.render(f"Светлячков: {self.__collected_fireflies}/10", True, YELLOW)
            self.__screen.blit(counter, (WIDTH - 150, 10))

        elif self.__current_room == "lab":
            for note in self.__notes:
                note_rect = note.get_rect()
                shifted_rect = note_rect.move(-camera_offset[0], -camera_offset[1])
                note.draw_with_offset(self.__screen, shifted_rect)
            for enemy in self.__enemies:
                enemy_rect = enemy.get_rect()
                shifted_rect = enemy_rect.move(-camera_offset[0], -camera_offset[1])
                enemy.draw_with_offset(self.__screen, shifted_rect)
            if self.__terminal:
                terminal_rect = self.__terminal.move(-camera_offset[0], -camera_offset[1])
                pygame.draw.rect(self.__screen, (80, 80, 120), terminal_rect)
                pygame.draw.rect(self.__screen, WHITE, terminal_rect, 3)
                font_small = pygame.font.Font(None, 20)
                if self.__terminal_active:
                    text = font_small.render("⚡ ВВЕДИ КОД ⚡", True, GREEN)
                else:
                    text = font_small.render("💻 ТЕРМИНАЛ", True, WHITE)
                self.__screen.blit(text, (terminal_rect.x + 15, terminal_rect.y + 30))
                if self.__terminal_active:
                    code_text = font_small.render(''.join(map(str, self.__player_input)), True, YELLOW)
                    self.__screen.blit(code_text, (terminal_rect.x + 35, terminal_rect.y + 50))

            ui_x = WIDTH - 240
            ui_y = 10
            ui_width = 220
            ui_height = 140
            pygame.draw.rect(self.__screen, (20, 20, 30), (ui_x, ui_y, ui_width, ui_height))
            pygame.draw.rect(self.__screen, (100, 100, 150), (ui_x, ui_y, ui_width, ui_height), 3)
            font_title = pygame.font.Font(None, 24)
            title = font_title.render("🧬 ЛАБОРАТОРИЯ", True, (0, 255, 0))
            self.__screen.blit(title, (ui_x + 40, ui_y + 5))
            collected = {}
            for note in self.__notes:
                if note.is_collected():
                    collected[note.get_digit()] = True
            code_order = [2, 4, 1, 3]
            code_display = ""
            for digit in code_order:
                if collected.get(digit, False):
                    code_display += f"[{digit}] "
                else:
                    code_display += "[ ] "
            font_code = pygame.font.Font(None, 32)
            code_text = font_code.render(code_display, True, YELLOW)
            self.__screen.blit(code_text, (ui_x + 20, ui_y + 40))
            notes_count = len([n for n in self.__notes if n.is_collected()])
            notes_text = font_title.render(f"📄 Записок: {notes_count}/5", True, WHITE)
            self.__screen.blit(notes_text, (ui_x + 20, ui_y + 75))
            if self.__terminal_active:
                status = "🔓 ВВЕДИ КОД 2-4-1-3"
                status_color = GREEN
            else:
                if notes_count >= 5:
                    status = "✅ Иди к терминалу"
                    status_color = YELLOW
                else:
                    status = f"🔒 Найди ещё {5 - notes_count}"
                    status_color = RED
            status_text = font_title.render(status, True, status_color)
            self.__screen.blit(status_text, (ui_x + 20, ui_y + 105))

        elif self.__current_room == "memory":
            for memory in self.__memories:
                memory_rect = memory.get_rect()
                shifted_rect = memory_rect.move(-camera_offset[0], -camera_offset[1])
                memory.draw_with_offset(self.__screen, shifted_rect)
            for enemy in self.__enemies:
                enemy_rect = enemy.get_rect()
                shifted_rect = enemy_rect.move(-camera_offset[0], -camera_offset[1])
                enemy.draw_with_offset(self.__screen, shifted_rect)
            font = pygame.font.Font(None, 24)
            counter = font.render(f"💜 Воспоминаний: {self.__collected_memories}/5", True, (200, 150, 255))
            self.__screen.blit(counter, (WIDTH - 180, 10))

        elif self.__current_room == "music":
            for note in self.__music_notes:
                if not note.is_collected():
                    note_rect = note.get_rect()
                    shifted_rect = note_rect.move(-camera_offset[0], -camera_offset[1])
                    note.draw_with_offset(self.__screen, shifted_rect)

            for enemy in self.__enemies:
                enemy_rect = enemy.get_rect()
                shifted_rect = enemy_rect.move(-camera_offset[0], -camera_offset[1])
                enemy.draw_with_offset(self.__screen, shifted_rect)

            if self.__music_panel:
                panel_rect = self.__music_panel.move(-camera_offset[0], -camera_offset[1])
                pygame.draw.rect(self.__screen, (80, 80, 80), panel_rect)
                pygame.draw.rect(self.__screen, GOLD, panel_rect, 3)
                font_small = pygame.font.Font(None, 20)
                if self.__music_panel_active:
                    text = font_small.render("✅ НАЖМИ E", True, GREEN)
                else:
                    text = font_small.render("🎵 ПАНЕЛЬ", True, WHITE)
                self.__screen.blit(text, (panel_rect.x + 30, panel_rect.y + 30))

            font = pygame.font.Font(None, 24)
            counter = font.render(f"🎵 Нот: {self.__collected_notes_music}/7", True, GOLD)
            self.__screen.blit(counter, (WIDTH - 150, 10))

        player_rect = self.__player.get_rect()
        shifted_player_rect = player_rect.move(-camera_offset[0], -camera_offset[1])
        self.__player.draw_with_offset(self.__screen, shifted_player_rect)

        if self.__show_hint:
            hint_surface = pygame.Surface((400, 120))
            hint_surface.set_alpha(200)
            hint_surface.fill((50, 50, 50))
            self.__screen.blit(hint_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 60))
            font = pygame.font.Font(None, 24)
            if self.__current_room == "forest":
                hint_lines = ["🌲 ЛЕС ВОСПОМИНАНИЙ 🌲", "Собери 10 светлячков", "Осторожно! В лесу бродит Тень...",
                              "Если коснётся - начнёшь сначала"]
            elif self.__current_room == "lab":
                hint_lines = ["🔬 ЗАБРОШЕННАЯ ЛАБОРАТОРИЯ 🔬", "Найди 5 записок с цифрами", "Цифры появятся на панели",
                              "Собери все и иди к терминалу"]
            elif self.__current_room == "memory":
                hint_lines = ["🏛️ ХРАМ ПАМЯТИ 🏛️", "Собери 5 фиолетовых воспоминаний",
                              "Осторожно! Призраки ищут тебя...", "Они проходят сквозь стены!"]
            elif self.__current_room == "music":
                hint_lines = ["🎵 МУЗЫКАЛЬНАЯ КОМНАТА 🎵", "Собери 7 золотых нот", "За тобой бежит КЛОН!",
                              "Собери все и беги к панели"]
            else:
                hint_lines = ["Добро пожаловать в игру!"]
            for i, line in enumerate(hint_lines):
                text = font.render(line, True, WHITE)
                self.__screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 40 + i * 20))
            self.__hint_timer -= 1
            if self.__hint_timer <= 0:
                self.__show_hint = False

        font = pygame.font.Font(None, 36)
        room_text = font.render(f"Комната: {self.__current_room}", True, WHITE)
        self.__screen.blit(room_text, (10, 10))
        keys_text = font.render(f"Ключей: {len(self.__keys_collected)}/4", True, YELLOW)
        self.__screen.blit(keys_text, (10, 50))
        hint = font.render("E - взаимодействовать | ESC - выход/назад", True, WHITE)
        self.__screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()


    def run(self):
        while self.__running:
            self.handle_events()
            self.update()
            self.draw()
            self.__clock.tick(FPS)
        pygame.quit()