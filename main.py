import sys
import pygame 
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.SysFont("Arial", 40)
button_font = pygame.font.SysFont("Arial", 32)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("Game Over", True, Colors.white)
restart_surface = button_font.render("Restart", True, Colors.white)
score_rect = pygame.Rect(320, 65, 170, 60)
next_rect = pygame.Rect(320, 250, 170, 180)
restart_rect = pygame.Rect(160, 330, 180, 60)
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Тетрис на Питоне")
clock = pygame.time.Clock()

game = Game()
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate_block()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
        if event.type == pygame.MOUSEBUTTONDOWN and game.game_over == True:
            if restart_rect.collidepoint(event.pos):
                game.game_over = False
                game.reset()

    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (365, 200, 50, 50))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    game.draw(screen)

    if game.game_over == True:
        overlay = pygame.Surface((500, 620), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        screen.blit(game_over_surface, game_over_surface.get_rect(center=(250, 240)))
        pygame.draw.rect(screen, Colors.light_blue, restart_rect, 0, 10)
        screen.blit(restart_surface, restart_surface.get_rect(center=restart_rect.center))

    pygame.display.update()
    clock.tick(60)