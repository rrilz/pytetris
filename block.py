from colors import Colors
from position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.row_offset = 0
        self.col_offset = 0
        self.colors = Colors.get_cell_color()

    def move(self, row, col):
        self.row_offset += row
        self.col_offset += col

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.col + self.col_offset)
            moved_tiles.append(position)
        return moved_tiles

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(tile.col * self.cell_size + offset_x, tile.row * self.cell_size + offset_y, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def draw_centered(self, screen, center_x, center_y):
        tiles = self.get_cell_positions()
        min_row = min(tile.row for tile in tiles)
        max_row = max(tile.row for tile in tiles)
        min_col = min(tile.col for tile in tiles)
        max_col = max(tile.col for tile in tiles)
        width = (max_col - min_col + 1) * self.cell_size
        height = (max_row - min_row + 1) * self.cell_size
        start_x = center_x - width // 2
        start_y = center_y - height // 2
        for tile in tiles:
            tile_rect = pygame.Rect((tile.col - min_col) * self.cell_size + start_x, (tile.row - min_row) * self.cell_size + start_y, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def rotate(self):
        self.rotation_state +=1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotate(self):
        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1
