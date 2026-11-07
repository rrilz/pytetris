import sys
import pygame 
from game import Game
from colors import Colors
from menu import Menu

pygame.init()

title_font = pygame.font.SysFont("segoeui", 40, bold=True)
button_font = pygame.font.SysFont("segoeui", 25, bold=True)
label_font = pygame.font.SysFont("segoeui", 22, bold=True)

background = Colors.background
panel = Colors.panel
panel_light = Colors.panel_light
text_color = Colors.text
accent = Colors.accent

score_surface = label_font.render("Счёт", True, text_color)
next_surface = label_font.render("Следующий", True, text_color)
game_over_surface = title_font.render("Игра окончена", True, text_color)
restart_surface = button_font.render("Перезапустить", True, background)
menu_surface = button_font.render("В меню", True, background)

score_rect = pygame.Rect(330, 65, 155, 75)
next_rect = pygame.Rect(330, 230, 155, 190)
restart_rect = pygame.Rect(110, 330, 280, 60)
menu_rect = pygame.Rect(160, 410, 180, 60)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Тетрис на Питоне")
clock = pygame.time.Clock()

menu = Menu()
game = None

page = 'menu'
soft_drop = False

GAME_UPDATE = pygame.USEREVENT
MENU_UPDATE = pygame.USEREVENT + 1

pygame.time.set_timer(GAME_UPDATE, 200)
pygame.time.set_timer(MENU_UPDATE, 500)

last_fall_time = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MENU_UPDATE and page == 'menu':
            menu.update()   
        if page == 'menu' or page == 'settings':


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and page == 'settings':
                    page = 'menu'

                if event.key == pygame.K_RETURN and page == 'menu':
                    page = 'game'
                    game = Game(menu.music_volume > 0, menu.sound_volume > 0)
                    last_fall_time = pygame.time.get_ticks()
                    pygame.mixer.music.set_volume(menu.music_volume)
                    game.rotate_sound.set_volume(menu.sound_volume)
                    game.clear_row_sound.set_volume(menu.sound_volume)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = menu.click(event.pos, page)

                if action == 'game':
                    page = 'game'
                    game = Game(menu.music_volume > 0, menu.sound_volume > 0)
                    last_fall_time = pygame.time.get_ticks()
                    pygame.mixer.music.set_volume(menu.music_volume)
                    game.rotate_sound.set_volume(menu.sound_volume)
                    game.clear_row_sound.set_volume(menu.sound_volume)

                elif action == 'settings':
                    page = 'settings'

                elif action == 'menu':
                    page = 'menu'

                elif action == 'exit':
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and page == 'settings':
                    menu.change_volume(event.pos)           

            continue

        if page == 'game':

            if event.type == pygame.KEYDOWN:
                        
                if event.key == pygame.K_ESCAPE:
                    page = 'menu'
                    menu.play_music()
                    continue

                if event.key == pygame.K_r and game.game_over:
                    game.game_over = False
                    game.reset()

                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()

                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()

                if event.key == pygame.K_DOWN and not game.game_over:
                    soft_drop = True

                if event.key == pygame.K_SPACE and not game.game_over:
                    game.hard_drop()
                    last_fall_time = pygame.time.get_ticks()

                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate_block()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    soft_drop = False


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.game_over:

                    if restart_rect.collidepoint(event.pos):
                        game.game_over = False
                        game.reset()

                    if menu_rect.collidepoint(event.pos):
                        menu.play_music()
                        page = 'menu'

    if page == 'game' and game is not None and not game.game_over:

        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Скорость обычного и ускоренного падения
        fall_interval = 200

        if keys[pygame.K_DOWN]:
            fall_interval = 90

        if current_time - last_fall_time >= fall_interval:

            moved = game.move_down()

            if keys[pygame.K_DOWN] and moved:
                game.update_score(0, 1)

            last_fall_time = current_time

    
    if page == 'menu' or page == 'settings':
        menu.draw(screen, page)

        pygame.display.update()
        clock.tick(60)
        continue

    if page == 'game':
        score_value_surface = title_font.render(str(game.score), True, text_color)

        screen.fill(background)

        pygame.draw.rect(screen, panel, score_rect, border_radius=10)
        pygame.draw.rect(screen, panel, next_rect, border_radius=10)
        pygame.draw.rect(screen, (137, 180, 194), score_rect, width=1, border_radius=10)
        pygame.draw.rect(screen, (185, 165, 204), next_rect, width=1, border_radius=10)

        screen.blit(
            score_surface,
            score_surface.get_rect(
                centerx=score_rect.centerx, y=25
            )
        )

        screen.blit(
            next_surface,
            next_surface.get_rect(
                centerx=next_rect.centerx, y=190
            )
        )

        screen.blit(
            score_value_surface,
            score_value_surface.get_rect(
                center=score_rect.center
            )
        )

        game.draw(screen)

        if game.game_over:
            overlay = pygame.Surface((500, 620), pygame.SRCALPHA)
            overlay.fill((15, 18, 24, 180))
            screen.blit(overlay, (0, 0))

            screen.blit(game_over_surface, game_over_surface.get_rect(center=(250, 240)))
            if restart_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, accent, restart_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, panel_light, restart_rect, border_radius=8)
            screen.blit(restart_surface, restart_surface.get_rect(center=restart_rect.center))
            
            if menu_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, accent, menu_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, panel_light, menu_rect, border_radius=8)
            screen.blit(menu_surface, menu_surface.get_rect(center=menu_rect.center))

        pygame.display.update()
        clock.tick(60)