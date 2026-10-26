import pygame

from grid import Grid
from blocks import IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, UBlock, ZBlock, XBlock
import random


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), UBlock(), ZBlock(), XBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        pygame.mixer.music.load("Тетрис.mp3")
        pygame.mixer.music.play(-1)

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
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
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

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), UBlock(), ZBlock(), XBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0