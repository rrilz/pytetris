import sys
import pygame 
from game import Game
from colors import Colors
from menu import Menu

pygame.init()

title_font = pygame.font.SysFont("segoeui,trebuchetms,verdana,arial", 40, bold=True)
button_font = pygame.font.SysFont("segoeui,trebuchetms,verdana,arial", 32, bold=True)
label_font = pygame.font.SysFont("segoeui,trebuchetms,verdana,arial", 28, bold=True)

score_surface = label_font.render("Счёт", True, Colors.white)
next_surface = label_font.render("Следующий", True, Colors.white)
game_over_surface = title_font.render("Игра окончена", True, Colors.white)
restart_surface = button_font.render("Перезапустить", True, Colors.white)
menu_surface = button_font.render("В меню", True, Colors.white)

score_rect = pygame.Rect(320, 65, 170, 60)
next_rect = pygame.Rect(320, 250, 170, 180)
restart_rect = pygame.Rect(110, 330, 280, 60)
menu_rect = pygame.Rect(160, 410, 180, 60)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Тетрис на Питоне")
clock = pygame.time.Clock()

menu = Menu()
game = None
in_menu = True

GAME_UPDATE = pygame.USEREVENT
MENU_UPDATE = pygame.USEREVENT + 1

pygame.time.set_timer(GAME_UPDATE, 200)
pygame.time.set_timer(MENU_UPDATE, 600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if in_menu == True:
            if event.type == MENU_UPDATE:
                menu.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game = Game(menu.music_on, menu.sound_on)
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                menu.click(event.pos)
                if menu.start_rect.collidepoint(event.pos):
                    game = Game(menu.music_on, menu.sound_on)
                    in_menu = False
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu.play_music()
                in_menu = True
                continue
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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game.game_over == True:
            if restart_rect.collidepoint(event.pos):
                game.game_over = False
                game.reset()
            if menu_rect.collidepoint(event.pos):
                menu.play_music()
                in_menu = True

    if in_menu == True:
        menu.draw(screen)
        pygame.display.update()
        clock.tick(60)
        continue

    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, score_surface.get_rect(centerx = score_rect.centerx, y = 10))
    screen.blit(next_surface, next_surface.get_rect(centerx = next_rect.centerx, y = 200))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    game.draw(screen)

    if game.game_over == True:
        overlay = pygame.Surface((500, 620), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        screen.blit(game_over_surface, game_over_surface.get_rect(center=(250, 240)))
        if restart_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, Colors.lavender, restart_rect, 0, 10)
        else:
            pygame.draw.rect(screen, Colors.light_blue, restart_rect, 0, 10)
        screen.blit(restart_surface, restart_surface.get_rect(center=restart_rect.center))
        if menu_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, Colors.lavender, menu_rect, 0, 10)
        else:
            pygame.draw.rect(screen, Colors.light_blue, menu_rect, 0, 10)
        screen.blit(menu_surface, menu_surface.get_rect(center=menu_rect.center))

    pygame.display.update()
    clock.tick(60)