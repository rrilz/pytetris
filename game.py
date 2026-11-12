import pygame

from grid import Grid
from blocks import IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, UBlock, ZBlock, XBlock
import random
from colors import Colors
from fonts import load_font

class Game:
    def __init__(self, audio):
        self.audio = audio
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

        self.particles = []
        self.particles_start = 0
        self.particles_duration = 450

        self.score_popup_text = ""
        self.score_popup_start = 0
        self.score_popup_y = 0
        self.score_popup_duration = 650

        self.line_message = ""
        self.line_message_start = 0
        self.line_message_duration = 650

        self.effect_font = load_font("NotoSans-Bold.ttf", 26)    

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
        self.lock_block(hard_drop=True)

    def lock_block(self, hard_drop=False):
        if hard_drop:
            self.audio.play_sfx("hard_drop")
        else:
            self.audio.play_sfx("lock")
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

            self.audio.play_sfx("clear")
            now = pygame.time.get_ticks()
            self.update_score(rows_cleared, 0)

            points = {1: 100, 2: 300, 3: 500, 4: 800}.get(rows_cleared, 800)

            self.score_popup_text = f"+{points}"
            self.score_popup_start = now
            self.score_popup_y = 11 + (sum(full_rows) / len(full_rows)) * 30

            line_labels = {
                1: "1 ЛИНИЯ",
                2: "2 ЛИНИИ",
                3: "3 ЛИНИИ",
                4: "4 ЛИНИИ"
            }

            self.line_message = line_labels.get(rows_cleared, f"{rows_cleared} ЛИНИЙ")
            self.line_message_start = now

            self.particles = []

            for row in full_rows:
                for _ in range(7):
                    self.particles.append({
                        "x": random.uniform(15, 307),
                        "y": 11 + row * 30 + 15,
                        "vx": random.uniform(-2.5, 2.5),
                        "vy": random.uniform(-3.8, -1.2),
                        "radius": random.randint(2, 4),
                        "color": random.choice(self.grid.colors[1:])
                    })

            self.particles_start = now

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
                self.audio.play_sfx("rotate")
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
        self.draw_feedback(screen)
        self.next_block.draw_centered(screen, 408, 365)

    def draw_feedback(self, screen):
        now = pygame.time.get_ticks()

        if self.particles:
            elapsed = now - self.particles_start

            if elapsed < self.particles_duration:
                progress = elapsed / self.particles_duration
                frames = elapsed / (1000 / 60)

                particle_layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

                for particle in self.particles:
                    x = particle["x"] + particle["vx"] * frames
                    y = (
                        particle["y"]
                        + particle["vy"] * frames
                        + 0.10 * frames ** 2
                    )

                    x = max(12, min(309, x))
                    y = max(12, min(610, y))

                    alpha = int(255 * (1 - progress))

                    color = (*particle["color"], alpha)

                    pygame.draw.circle(
                        particle_layer,
                        color,
                        (int(x), int(y)),
                        particle["radius"]
                    )

                screen.blit(particle_layer, (0, 0))
            else:
                self.particles = []

        if self.score_popup_text:
            elapsed = now - self.score_popup_start

            if elapsed < self.score_popup_duration:
                progress = elapsed / self.score_popup_duration
                alpha = int(255 * (1 - progress))

                score_surface = self.effect_font.render(self.score_popup_text, True, Colors.accent)
                score_surface.set_alpha(alpha)

                y = int(self.score_popup_y - 30 * progress)

                screen.blit(score_surface, score_surface.get_rect(center=(161, y)))
            else:
                self.score_popup_text = ""

        if self.line_message:
            elapsed = now - self.line_message_start

            if elapsed < self.line_message_duration:
                progress = elapsed / self.line_message_duration
                alpha = int(255 * (1 - progress))

                message_surface = self.effect_font.render(self.line_message, True, Colors.text)
                message_surface.set_alpha(alpha)

                y = int(270 - 25 * progress)

                screen.blit(message_surface, message_surface.get_rect(center=(161, y)))
            else:
                self.line_message = ""


    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), UBlock(), ZBlock(), XBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.lines_cleared = 0
        self.clear_effect_rows = []
        self.clear_effect_start = 0

        self.landing_effect_tiles = []
        self.landing_effect_start = 0

        self.drop_effect_start = 0
        self.score_effect_start = 0
        self.clear_effect_rows = []
        self.clear_effect_start = 0

        self.landing_effect_tiles = []
        self.landing_effect_start = 0

        self.drop_effect_start = 0
        self.score_effect_start = 0

        self.particles = []
        self.particles_start = 0

        self.score_popup_text = ""
        self.score_popup_start = 0

        self.line_message = ""
        self.line_message_start = 0