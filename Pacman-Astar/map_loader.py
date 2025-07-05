import pygame
import os
import random

TILE_SIZE = 20  # Kích thước mỗi ô

# Đường dẫn thư mục chứa ảnh
ASSET_DIR = "C:/VisualStudioCode/Pacman-Astar/picture"

def load_wall_images():
    return {
        3: pygame.image.load(os.path.join(ASSET_DIR, "dọc.png")),
        4: pygame.image.load(os.path.join(ASSET_DIR, "Ngang.png")),
        5: pygame.image.load(os.path.join(ASSET_DIR, "Trên phải.png")),
        6: pygame.image.load(os.path.join(ASSET_DIR, "Trên trái.png")),
        7: pygame.image.load(os.path.join(ASSET_DIR, "Dưới trái.png")),
        8: pygame.image.load(os.path.join(ASSET_DIR, "Dưới phải.png")),
        9: pygame.image.load(os.path.join(ASSET_DIR, "Cửa.png")),
        10: pygame.image.load(os.path.join(ASSET_DIR, "TeleLeft.jpg")),
        11: pygame.image.load(os.path.join(ASSET_DIR, "TeleRight.jpg")),
    }

import random

def load_map(file_path, num_power_pellets=5):
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    game_map = [list(map(int, line.split(','))) for line in lines if line.strip()]

    # Tìm tất cả các vị trí có giá trị là 1 (chấm nhỏ)
    dot_positions = [(y, x) for y, row in enumerate(game_map) for x, val in enumerate(row) if val == 1]

    # Random chọn một số vị trí để thành chấm to (giá trị 2)
    power_pellets = random.sample(dot_positions, min(num_power_pellets, len(dot_positions)))
    for y, x in power_pellets:
        game_map[y][x] = 2

    return game_map


def draw_map(screen, game_map, wall_images):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            pos = (x * TILE_SIZE, y * TILE_SIZE)

            if tile == 1:
                pygame.draw.circle(screen, (255, 255, 255), (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2), 3)
            elif tile == 2:
                pygame.draw.circle(screen, (255, 255, 255), (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2), 6)
            elif tile in wall_images:
                image = pygame.transform.scale(wall_images[tile], (TILE_SIZE, TILE_SIZE))
                screen.blit(image, pos)
