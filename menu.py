import random
import pygame
from colors import Colors
from blocks import IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, UBlock, ZBlock, XBlock
from fonts import load_font

class Menu:
    def __init__(self):
        self.music_volume = 0.3
        self.sound_volume = 0.7

        self.background = Colors.background
        self.panel = Colors.panel
        self.panel_light = Colors.panel_light
        self.text_color = Colors.text
        self.muted_text = Colors.muted_text
        self.accent = Colors.accent
        self.accent_hover = Colors.accent_hover

        self.title_font = load_font("NotoSansMono-Bold.ttf", 64)
        self.subtitle_font = load_font("NotoSans-Regular.ttf", 18)
        self.button_font = load_font("NotoSans-Bold.ttf", 25)
        self.text_font = load_font("NotoSans-Regular.ttf", 19)
        self.small_font = load_font("NotoSans-Regular.ttf", 15)

        self.play_rect = pygame.Rect(125, 340, 250, 55)
        self.settings_rect = pygame.Rect(125, 410, 250, 55)
        self.exit_rect = pygame.Rect(125, 480, 250, 55)
        self.back_rect = pygame.Rect(125, 500, 250, 50)

        self.music_slider = pygame.Rect(150, 250, 200, 8)
        self.sound_slider = pygame.Rect(150, 355, 200, 8)

        self.blocks = []
        self.rotations = 0
        self.change_blocks()


    def change_blocks(self):
        classes = random.sample(
            [IBlock, JBlock, LBlock, OBlock, SBlock,
             TBlock, UBlock, ZBlock, XBlock],
            3
        )
        self.blocks = [block_class() for block_class in classes]


    def set_music_volume(self, value):
        self.music_volume = max(0, min(1, value))

    def set_sound_volume(self, value):
        self.sound_volume = max(0, min(1, value))

    def change_volume(self, pos):
        if self.music_slider.inflate(0, 25).collidepoint(pos):
            value = (pos[0] - self.music_slider.x) / self.music_slider.width
            self.set_music_volume(value)

        if self.sound_slider.inflate(0, 25).collidepoint(pos):
            value = (pos[0] - self.sound_slider.x) / self.sound_slider.width
            self.set_sound_volume(value)

    def update(self):
        if random.random() < 0.5:
            block = random.choice(self.blocks)

            if random.choice([True, False]):
                block.rotate()
            else:
                block.undo_rotate()

        elif random.random() < 0.4:
            all_blocks = [
                IBlock, JBlock, LBlock, OBlock,
                SBlock, TBlock, UBlock, ZBlock, XBlock
            ]

            used = [type(block) for block in self.blocks]
            available = [cls for cls in all_blocks if cls not in used]

            if available:
                index = random.randrange(len(self.blocks))
                self.blocks[index] = random.choice(available)()

    def click(self, pos, page):
        if page == 'menu':
            if self.play_rect.collidepoint(pos):
                return 'game'

            if self.settings_rect.collidepoint(pos):
                return 'settings'

            if self.exit_rect.collidepoint(pos):
                return 'exit'

        elif page == 'settings':
            if self.back_rect.collidepoint(pos):
                return 'menu'

            self.change_volume(pos)

        return None

    def draw_button(self, screen, rect, text):
        if rect.collidepoint(pygame.mouse.get_pos()):
            color = self.accent_hover
        else:
            color = self.panel_light

        pygame.draw.rect(screen, color, rect, border_radius=8)

        surface = self.button_font.render(text, True, self.text_color)
        screen.blit(surface, surface.get_rect(center=rect.center))

    def draw_piece(self, screen, block, center_x, center_y):
        block.draw_centered(screen, center_x, center_y)

    def draw_slider(self, screen, rect, value, label):
        label_surface = self.text_font.render(label, True, self.text_color)
        screen.blit(label_surface, (rect.x, rect.y - 65))

        pygame.draw.rect(screen, self.panel_light, rect, border_radius=5)

        fill_rect = pygame.Rect(rect.x, rect.y, int(rect.width * value), rect.height)
        pygame.draw.rect(screen, self.accent, fill_rect, border_radius=5)

        knob_x = rect.x + int(rect.width * value)
        pygame.draw.circle(screen, self.text_color, (knob_x, rect.centery), 9)

        value_surface = self.small_font.render(str(int(value * 100)) + "%", True, self.muted_text)
        screen.blit(value_surface, (rect.right - 35, rect.y - 30))
    
    def draw_menu(self, screen):
        screen.fill(self.background)

        title = self.title_font.render("TETRIS", True, self.text_color)
        screen.blit(title, title.get_rect(center=(250, 105)))

        subtitle = self.subtitle_font.render("A little place for falling blocks", True, self.muted_text)
        screen.blit(subtitle, subtitle.get_rect(center=(250, 155))) 

        for i, block in enumerate(self.blocks):
            self.draw_piece(screen, block, 90 + i * 160, 250)

        self.draw_button(screen, self.play_rect, "Играть")
        self.draw_button(screen, self.settings_rect, "Настройки")
        self.draw_button(screen, self.exit_rect, "Выход")    

    def draw_settings(self, screen):
        screen.fill(self.background)

        title = self.title_font.render("НАСТРОЙКИ", True, self.text_color)
        screen.blit(title, title.get_rect(center=(250, 110)))

        self.draw_slider(screen, self.music_slider, self.music_volume, "Громкость музыки")
        self.draw_slider(screen, self.sound_slider, self.sound_volume, "Громкость звуков")
        self.draw_button(screen, self.back_rect, "Назад")

    def draw(self, screen, page):
        if page == "menu":
            self.draw_menu(screen)
        elif page == "settings":
            self.draw_settings(screen)
        