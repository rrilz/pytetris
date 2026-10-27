import random
import pygame
from colors import Colors
from blocks import IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, UBlock, ZBlock, XBlock

class Menu:
    def __init__(self):
        self.music_on = True
        self.sound_on = True
        self.rotations = 0
        self.blocks = []
        self.change_blocks()

        title_font = pygame.font.SysFont("segoeui,trebuchetms,verdana,arial", 80, bold=True)
        text_font = pygame.font.SysFont("segoeui,trebuchetms,verdana,arial", 32, bold=True)
        title_colors = [Colors.red, Colors.orange, Colors.yellow, Colors.green, Colors.cyan, Colors.purple]
        self.title_surfaces = []
        for i, letter in enumerate("ТЕТРИС"):
            self.title_surfaces.append(title_font.render(letter, True, title_colors[i]))
        self.start_surface = text_font.render("Начать игру", True, Colors.white)
        self.music_surface = text_font.render("Включить музыку", True, Colors.white)
        self.sound_surface = text_font.render("Включить звуки", True, Colors.white)

        self.start_rect = pygame.Rect(130, 330, 240, 70)
        self.music_rect = pygame.Rect(70, 450, 32, 32)
        self.sound_rect = pygame.Rect(70, 505, 32, 32)

        self.play_music()

    def change_blocks(self):
        classes = random.sample([IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, UBlock, ZBlock, XBlock], 3)
        self.blocks = [block_class() for block_class in classes]

    def play_music(self):
        pygame.mixer.music.stop()
        if self.music_on == True:
            pygame.mixer.music.load("Меню.mp3")
            pygame.mixer.music.play(-1)

    def update(self):
        self.rotations += 1
        if self.rotations == 4:
            self.rotations = 0
            self.change_blocks()
        else:
            for block in self.blocks:
                block.rotate()

    def click(self, pos):
        if self.music_rect.collidepoint(pos):
            self.music_on = not self.music_on
            self.play_music()

    def draw_checkbox(self, screen, rect, checked, surface):
        pygame.draw.rect(screen, Colors.light_blue, rect, 0, 6)
        pygame.draw.rect(screen, Colors.white, rect, 2, 6)
        if checked == True:
            points = [(rect.x + 7, rect.y + 17), (rect.x + 14, rect.y + 24), (rect.x + 26, rect.y + 9)]
            pygame.draw.lines(screen, Colors.mint, False, points, 4)
        screen.blit(surface, (rect.x + 46, rect.y))

    def draw(self, screen):
        screen.fill(Colors.dark_blue)

        x = 250 - sum(surface.get_width() for surface in self.title_surfaces) // 2
        for surface in self.title_surfaces:
            screen.blit(surface, (x, 40))
            x += surface.get_width()

        for i, block in enumerate(self.blocks):
            block.draw_centered(screen, 90 + i * 160, 230)

        if self.start_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, Colors.lavender, self.start_rect, 0, 10)
        else:
            pygame.draw.rect(screen, Colors.light_blue, self.start_rect, 0, 10)
        screen.blit(self.start_surface, self.start_surface.get_rect(center = self.start_rect.center))

        self.draw_checkbox(screen, self.music_rect, self.music_on, self.music_surface)
        self.draw_checkbox(screen, self.sound_rect, self.sound_on, self.sound_surface)