import pygame

from grid import Grid
from blocks import IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, UBlock, ZBlock, XBlock
import random


class Game:
    def __init__(self, music_on, sound_on):
        self.sound_on = sound_on
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), UBlock(), ZBlock(), XBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False

        self.score = 0
        self.lines_cleared = 0

        self.clear_effect_rows = []
        self.clear_effect_start = 0
        self.clear_effect_duration = 220

        self.landing_effect_tiles = []
        self.landing_effect_start = 0
        self.landing_effect_duration = 130

        self.drop_effect_start = 0
        self.drop_effect_duration = 140
        self.score_effect_start = 0
        self.score_effect_duration = 220

        if music_on:
            pygame.mixer.music.load("Тетрис.mp3")
            pygame.mixer.music.play(-1)
        self.rotate_sound = pygame.mixer.Sound("rotate.ogg")
        self.clear_row_sound = pygame.mixer.Sound("clear.ogg")

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared >= 4:
            self.score += 800
        self.score += move_down_points
        if lines_cleared > 0:
            self.score_effect_start = pygame.time.get_ticks()

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), UBlock(), ZBlock(), XBlock()]

        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()
            return False
        return True
    def hard_drop(self):
        distance = 0

        while True:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1, 0)
                break
            distance += 1
        self.update_score(0, distance*2)
        self.drop_effect_start = pygame.time.get_ticks()
        self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        self.landing_effect_tiles = tiles.copy()
        self.landing_effect_start = pygame.time.get_ticks()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        full_rows = []

        for row in range(self.grid.num_rows):
            if self.grid.if_full(row):
                full_rows.append(row)

        rows_cleared = self.grid.clear_full_rows()

        if rows_cleared > 0:
            self.lines_cleared += rows_cleared
            self.clear_effect_rows = full_rows
            self.clear_effect_start = pygame.time.get_ticks()

            if self.sound_on:
                self.clear_row_sound.play()

            self.update_score(rows_cleared, 0)
        if not self.block_inside() or not self.block_fits():
            self.game_over = True

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.if_inside(tile.row, tile.col) == False:
                return False
        return True

    def rotate_block(self):
        self.current_block.rotate()
        kicks = [
            (0, 0),
            (0, -1), (0, 1), (0, -2), (0, 2),   
            (-1, 0), (-2, 0),                   
            (-1, -1), (-1, 1),                  
            (1, 0), (1, -1), (1, 1),           
        ]
       
        for dr, dc in kicks:
            self.current_block.move(dr, dc)
            if self.block_inside() and self.block_fits():
                if self.sound_on:
                    self.rotate_sound.play()
                return
            self.current_block.move(-dr, -dc)

        self.current_block.undo_rotate()

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.col) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)

        if not self.game_over:
            self.current_block.draw(screen, 11, 11)
        elapsed = pygame.time.get_ticks() - self.landing_effect_start

        if elapsed < self.landing_effect_duration:
            alpha = int(110 * (1 - elapsed / self.landing_effect_duration))

            for tile in self.landing_effect_tiles:
                effect = pygame.Surface((29, 29), pygame.SRCALPHA)
                effect.fill((255, 255, 255, alpha))
                screen.blit(
                    effect,
                    (11 + tile.col * 30, 11 + tile.row * 30)
                )
        else:
            self.landing_effect_tiles = []

        elapsed = pygame.time.get_ticks() - self.drop_effect_start

        if elapsed < self.drop_effect_duration and self.drop_effect_start > 0:
            alpha = int(100 * (1 - elapsed / self.drop_effect_duration))

            effect = pygame.Surface((302, 602), pygame.SRCALPHA)
            pygame.draw.rect(effect, (185, 165, 204, alpha), effect.get_rect(), width=2, border_radius=3)
            screen.blit(effect, (10, 10))
        if self.clear_effect_rows:
            elapsed = pygame.time.get_ticks() - self.clear_effect_start

            if elapsed < self.clear_effect_duration:
                alpha = int(200 * (1 - elapsed / self.clear_effect_duration))
                for row in self.clear_effect_rows:
                    effect = pygame.Surface((300, 30), pygame.SRCALPHA)
                    effect.fill((255, 255, 255, alpha))
                    screen.blit(effect, (11, 11 + row * 30))
            else:
                self.clear_effect_rows = []

        self.next_block.draw_centered(screen, 408, 365)

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), UBlock(), ZBlock(), XBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.lines_cleared = 0