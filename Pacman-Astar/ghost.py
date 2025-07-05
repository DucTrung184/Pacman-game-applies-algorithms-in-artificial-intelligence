import pygame
import os
import random
import time
from pathfinding import a_star, bfs

VALID_TILES = [0, 1, 2, 9]

class Ghost:
    def __init__(self, x, y, tile_size, ghost_id=0):
        self.tile_size = tile_size
        self.x = x * tile_size
        self.y = y * tile_size
        self.grid_x = x
        self.grid_y = y
        self.start_pos = (x, y)
        self.speed = 2
        self.respawning = False
        self.respawn_timer = 0
        self.path = []
        self.teleport_cooldown = 0
        self.ghost_id = ghost_id
        self.direction = (0, 0)

        ghost_names = ["Red", "Pink", "Orange"]
        ghost_name = ghost_names[ghost_id % len(ghost_names)]
        base_path = os.path.join("Ghost", ghost_name + ".png")
        happy_path = os.path.join("Ghost", ghost_name + "Happy.png")
        surprise_path = os.path.join("Ghost", ghost_name + "Surprise.png")

        base_img = pygame.image.load(base_path)
        happy_img = pygame.image.load(happy_path)
        surprise_img = pygame.image.load(surprise_path)

        size = tile_size + 2 if ghost_id == 2 else tile_size + 4
        self.image_base = pygame.transform.scale(base_img, (size, size))
        self.image_happy = pygame.transform.scale(happy_img, (size, size))
        self.image_surprise = pygame.transform.scale(surprise_img, (size, size))
        self.image = self.image_base

        self.random_target = None
        self.random_target_timer = 0
        self.transition_state = None
        self.transition_start_time = 0

    def update(self, game_map, pacman):
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1

        self.grid_x = int(self.x // self.tile_size)
        self.grid_y = int(self.y // self.tile_size)
        current_pos = (self.grid_y, self.grid_x)

        if self.respawning:
            if time.time() - self.respawn_timer >= 2:
                self.respawning = False
            return

        # Ghi nhận hoạt cảnh vào/ra hunt mode
        if pacman.entering_hunt_animation:
            if self.transition_state != 'into_hunt':
                self.transition_state = 'into_hunt'
                self.transition_start_time = pacman.hunt_anim_start_time

        elif pacman.exiting_hunt_animation:
            if self.transition_state != 'out_of_hunt':
                self.transition_state = 'out_of_hunt'
                self.transition_start_time = pacman.hunt_anim_start_time

        # Dừng di chuyển trong thời gian hoạt cảnh
        if pacman.entering_hunt_animation or pacman.exiting_hunt_animation:
            return

        # Ghost đang bị Pacman ăn -> chạy xa
        if pacman.hunt_mode:
            target = self._get_furthest_tile_from_pacman(game_map, pacman)
            if current_pos != target:
                self.path = bfs(current_pos, target, game_map)
            self._follow_path(game_map)

        # Nếu Pacman đang bất tử thì Ghost về điểm xuất phát
        elif pacman.invincible:
            target = (self.start_pos[1], self.start_pos[0])
            target = (target[1], target[0])
            if current_pos != target:
                self.path = bfs(current_pos, target, game_map)
            self._follow_path(game_map)

        # Ghost đỏ dùng A*
        elif self.ghost_id == 0:
            target = (int(pacman.y // self.tile_size), int(pacman.x // self.tile_size))
            if current_pos != target:
                self.path = a_star(current_pos, target, game_map)
            self._follow_path(game_map)

        # Ghost hồng dùng BFS
        elif self.ghost_id == 1:
            target = (int(pacman.y // self.tile_size), int(pacman.x // self.tile_size))
            if current_pos != target:
                self.path = bfs(current_pos, target, game_map)
            self._follow_path(game_map)

        # Ghost cam đi đến mục tiêu ngẫu nhiên bằng BFS
        elif self.ghost_id == 2:
            self.random_target_timer -= 1
            if self.random_target_timer <= 0 or self.random_target is None:
                self.random_target = self._get_random_valid_tile(game_map)
                self.random_target_timer = 90

            if current_pos != self.random_target:
                self.path = bfs(current_pos, self.random_target, game_map)
            self._follow_path(game_map)

        self._handle_teleport(game_map)

    def _get_furthest_tile_from_pacman(self, game_map, pacman):
        max_dist = -1
        best_tile = (self.grid_y, self.grid_x)
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x] in VALID_TILES:
                    dist = abs(pacman.x - x * self.tile_size) + abs(pacman.y - y * self.tile_size)
                    if dist > max_dist:
                        max_dist = dist
                        best_tile = (y, x)
        return best_tile

    def _get_random_valid_tile(self, game_map):
        height = len(game_map)
        width = len(game_map[0])
        while True:
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
            if game_map[y][x] in VALID_TILES:
                return (y, x)

    def _follow_path(self, game_map):
        if self.path and len(self.path) > 0:
            next_tile = self.path[0]
            if self.at_center_of_tile():
                dx = next_tile[1] - self.grid_x
                dy = next_tile[0] - self.grid_y
                self.direction = (dx, dy)
                if (self.grid_y, self.grid_x) == next_tile:
                    self.path.pop(0)
            self._move_by_direction(game_map)

    def _move_by_direction(self, game_map):
        dx, dy = self.direction
        step_x = self.speed if dx > 0 else -self.speed if dx < 0 else 0
        step_y = self.speed if dy > 0 else -self.speed if dy < 0 else 0

        if step_x != 0:
            for _ in range(abs(int(step_x))):
                new_x = self.x + (1 if step_x > 0 else -1)
                if self.can_move_pixel_based(new_x, self.y, game_map):
                    self.x = new_x
                else:
                    break

        if step_y != 0:
            for _ in range(abs(int(step_y))):
                new_y = self.y + (1 if step_y > 0 else -1)
                if self.can_move_pixel_based(self.x, new_y, game_map):
                    self.y = new_y
                else:
                    break

    def at_center_of_tile(self, tolerance=2):
        center_x = self.grid_x * self.tile_size + self.tile_size // 2
        center_y = self.grid_y * self.tile_size + self.tile_size // 2
        return abs(self.x + self.tile_size // 2 - center_x) <= tolerance and \
               abs(self.y + self.tile_size // 2 - center_y) <= tolerance

    def can_move_pixel_based(self, px, py, game_map):
        buffer = 4
        left = px + buffer
        right = px + self.tile_size - buffer
        top = py + buffer
        bottom = py + self.tile_size - buffer

        corners = [
            (int(left // self.tile_size), int(top // self.tile_size)),
            (int(right // self.tile_size), int(top // self.tile_size)),
            (int(left // self.tile_size), int(bottom // self.tile_size)),
            (int(right // self.tile_size), int(bottom // self.tile_size))
        ]

        for x, y in corners:
            if not (0 <= y < len(game_map) and 0 <= x < len(game_map[0])):
                return False
            if game_map[y][x] not in VALID_TILES:
                return False
        return True

    def _handle_teleport(self, game_map):
        if self.teleport_cooldown > 0:
            return
        row = int(self.y // self.tile_size)
        col = int(self.x // self.tile_size)
        num_cols = len(game_map[0])

        if game_map[row][col] == 10:
            for c in range(num_cols - 1, -1, -1):
                if game_map[row][c] == 11:
                    self.x = c * self.tile_size
                    self.teleport_cooldown = 20
                    return

        if game_map[row][col] == 11:
            for c in range(num_cols):
                if game_map[row][c] == 10:
                    self.x = c * self.tile_size
                    self.teleport_cooldown = 20
                    return

    def draw(self, screen):
        if self.respawning and int(time.time() * 5) % 2 == 0:
            return

        show = True
        if self.transition_state:
            elapsed = time.time() - self.transition_start_time
            if elapsed < 2:
                show = int(time.time() * 5) % 2 == 0
                if self.transition_state == 'into_hunt':
                    self.image = self.image_surprise
                elif self.transition_state == 'out_of_hunt':
                    self.image = self.image_happy
            else:
                self.transition_state = None
                self.image = self.image_base

        if show:
            offset = (self.image.get_width() - self.tile_size) // 2
            screen.blit(self.image, (self.x - offset, self.y - offset))
