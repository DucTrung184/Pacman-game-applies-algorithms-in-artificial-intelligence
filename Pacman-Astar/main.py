import pygame
import time
from map_loader import load_map, draw_map, load_wall_images, TILE_SIZE
from pacman import Pacman
from ghost import Ghost
from menu import MENU, INSTRUCTION, PLAYING, show_menu, show_instruction, load_font, play_menu_music

MAP_WIDTH = 30
MAP_HEIGHT = 33
INFO_BAR_HEIGHT = TILE_SIZE * 2
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE + INFO_BAR_HEIGHT
BLACK = (0, 0, 0)

def play_ingame_music(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def show_end_screen(screen, bg_image, retro_font, screen_width, screen_height, music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    screen.blit(bg_image, (0, 0))
    draw_text = lambda text, y: screen.blit(retro_font.render(text, True, (255, 255, 255)),
                                            retro_font.render(text, True, (255, 255, 255)).get_rect(center=(screen_width // 2, y)))

    draw_text("Press R to Restart", screen_height - 160)
    draw_text("Press Q to Quit", screen_height - 120)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.stop()
                    return True  # restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
        pygame.time.delay(100)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman Game")
    clock = pygame.time.Clock()

    font_path = r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\PressStart2P-Regular.ttf"
    retro_font = load_font(font_path, 20)

    heart_img = pygame.image.load(r"C:\\VisualStudioCode\\Pacman-Astar\\picture\\Heart.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (24, 24))

    menu_bg = pygame.image.load(r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\MainMenu.png").convert()
    menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    instruction_bg = pygame.image.load(r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\Tutorial.png").convert()
    instruction_bg = pygame.transform.scale(instruction_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    victory_img = pygame.image.load(r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\Victory.png").convert()
    victory_img = pygame.transform.scale(victory_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    gameover_img = pygame.image.load(r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\GameOver.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    menu_music = r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\MenuSound.mp3"
    ingame_music = r"C:\\VisualStudioCode\\Pacman-Astar\\Menu\\IngameSound.mp3"
    play_menu_music(menu_music)

    game_state = MENU

    while True:
        map_data = load_map("map.txt")
        wall_images = load_wall_images()

        start_x, start_y = next(((x, y) for y, row in enumerate(map_data) for x, val in enumerate(row) if val == 1), (1, 1))
        pacman = Pacman(start_x, start_y, TILE_SIZE)

        ghosts = [
            Ghost(14, 15, TILE_SIZE, ghost_id=0),
            Ghost(15, 15, TILE_SIZE, ghost_id=1),
            Ghost(16, 15, TILE_SIZE, ghost_id=2)
        ]

        running = True
        while running:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if game_state == MENU and event.key == pygame.K_RETURN:
                        game_state = INSTRUCTION
                    elif game_state == INSTRUCTION and event.key == pygame.K_s:
                        game_state = PLAYING
                        pygame.mixer.music.stop()
                        play_ingame_music(ingame_music)
                    elif game_state == PLAYING:
                        if event.key == pygame.K_UP: pacman.set_direction((0, -1))
                        elif event.key == pygame.K_DOWN: pacman.set_direction((0, 1))
                        elif event.key == pygame.K_LEFT: pacman.set_direction((-1, 0))
                        elif event.key == pygame.K_RIGHT: pacman.set_direction((1, 0))

                elif event.type == pygame.KEYUP and game_state == PLAYING:
                    keys = pygame.key.get_pressed()
                    if not any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]]):
                        pacman.set_direction((0, 0))

            if game_state == MENU:
                show_menu(screen, retro_font, SCREEN_WIDTH, SCREEN_HEIGHT, menu_bg)

            elif game_state == INSTRUCTION:
                show_instruction(screen, font_path, SCREEN_WIDTH, SCREEN_HEIGHT, instruction_bg)

            elif game_state == PLAYING:
                draw_map(screen, map_data, wall_images)
                pacman.update(map_data)

                tile_x = int(pacman.x // pacman.tile_size)
                tile_y = int(pacman.y // pacman.tile_size)

                if 0 <= tile_y < len(map_data) and 0 <= tile_x < len(map_data[0]):
                    tile_value = map_data[tile_y][tile_x]
                    if tile_value == 1 or tile_value == 2:
                        map_data[tile_y][tile_x] = 0
                        if tile_value == 2:
                            pacman.activate_hunt()

                for ghost in ghosts:
                    ghost.update(map_data, pacman)
                    ghost.draw(screen)

                    pac_rect = pygame.Rect(pacman.x, pacman.y, TILE_SIZE, TILE_SIZE)
                    ghost_rect = pygame.Rect(ghost.x, ghost.y, TILE_SIZE, TILE_SIZE)

                    if pac_rect.colliderect(ghost_rect) and not ghost.respawning:
                        if pacman.hunt_mode:
                            ghost.x, ghost.y = ghost.start_pos[0] * TILE_SIZE, ghost.start_pos[1] * TILE_SIZE
                            ghost.path.clear()
                            ghost.respawning = True
                            ghost.respawn_timer = time.time()
                        elif not pacman.entering_hunt_animation and not pacman.exiting_hunt_animation:
                            pacman.hit_by_ghost()

                pacman.draw(screen)

                pygame.draw.rect(screen, (30, 30, 30), (0, MAP_HEIGHT * TILE_SIZE, SCREEN_WIDTH, INFO_BAR_HEIGHT))
                label = retro_font.render("LIVES:", True, (255, 255, 255))
                screen.blit(label, (10, MAP_HEIGHT * TILE_SIZE + 10))

                heart_start_x = label.get_width() + 40
                for i in range(pacman.lives):
                    screen.blit(heart_img, (heart_start_x + i * 30, MAP_HEIGHT * TILE_SIZE + 8))

                if pacman.lives <= 0:
                    restart = show_end_screen(screen, gameover_img, retro_font, SCREEN_WIDTH, SCREEN_HEIGHT, menu_music)
                    if restart:
                        play_ingame_music(ingame_music)
                        break
                    else:
                        return

                if all(val not in row for row in map_data for val in (1, 2)):
                    restart = show_end_screen(screen, victory_img, retro_font, SCREEN_WIDTH, SCREEN_HEIGHT, menu_music)
                    if restart:
                        play_ingame_music(ingame_music)
                        break
                    else:
                        return

            pygame.display.flip()
            clock.tick(60)

        if not running:
            break

    pygame.quit()

if __name__ == "__main__":
    main()