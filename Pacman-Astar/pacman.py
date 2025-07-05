import pygame
import os
import time

class Pacman:
    def __init__(self, x, y, tile_size):
        self.tile_size = tile_size
        self.x = x * tile_size
        self.y = y * tile_size
        self.speed = 2.5
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.score = 0
        self.teleport_cooldown = 0

        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0

        # Hunt mode
        self.hunt_mode = False
        self.hunt_start_time = 0
        self.entering_hunt_animation = False
        self.exiting_hunt_animation = False
        self.hunt_anim_start_time = 0

        scale_size = tile_size + 4
        base_path = "C:/VisualStudioCode/Pacman-Astar/Pacman"

        # Ảnh thường
        self.images_base = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Pacman_open.png")), (scale_size, scale_size)),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Pacman_closed.png")), (scale_size, scale_size))
        ]

        # Ảnh hunt mode (happy)
        self.images_happy = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "PacmanHappy_open.png")), (scale_size, scale_size)),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "PacmanHappy_closed.png")), (scale_size, scale_size))
        ]

        # Ảnh hoạt cảnh đặc biệt
        self.image_surprise = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "PacmanSurprise.png")), (scale_size, scale_size))

        self.current_image_index = 0
        self.animation_counter = 0
        self.animation_delay = 10

    def update(self, game_map):
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1

        # Hoạt cảnh vào hunt mode
        if self.entering_hunt_animation:
            if time.time() - self.hunt_anim_start_time >= 2:
                self.entering_hunt_animation = False
                self.hunt_mode = True
                self.hunt_start_time = time.time()
            self.animation_counter += 1
            return

        # Hoạt cảnh thoát hunt mode
        if self.exiting_hunt_animation:
            if time.time() - self.hunt_anim_start_time >= 2:
                self.exiting_hunt_animation = False
            self.animation_counter += 1
            return

        steps = int(self.speed)
        remainder = self.speed - steps

        moved = False
        for _ in range(steps):
            if self._try_move(1, game_map):
                moved = True
        if remainder > 0:
            moved |= self._try_move(remainder, game_map)

        self._handle_teleport(game_map)

        if moved:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delay:
                self.animation_counter = 0
                self.current_image_index = 1 - self.current_image_index
        elif self.hunt_mode or self.entering_hunt_animation or self.exiting_hunt_animation:
            self.animation_counter += 1

        # Tắt trạng thái bất tử sau 3 giây
        if self.invincible and time.time() - self.invincible_timer > 3:
            self.invincible = False

        # Tắt trạng thái hunt sau 8 giây
        if self.hunt_mode and time.time() - self.hunt_start_time > 8:
            self.hunt_mode = False
            self.exiting_hunt_animation = True
            self.hunt_anim_start_time = time.time()

    def draw(self, screen):
        if self.invincible and (self.animation_counter // 4) % 2 == 0:
            return

        # Chọn ảnh theo trạng thái
        if self.entering_hunt_animation:
            image = self.images_happy[0]
        elif self.exiting_hunt_animation:
            image = self.image_surprise
        elif self.hunt_mode:
            image = self.images_happy[self.current_image_index]
        else:
            image = self.images_base[self.current_image_index]

        angle = self._get_rotation_angle()
        rotated_image = pygame.transform.rotate(image, angle)
        offset = (rotated_image.get_width() - self.tile_size) // 2

        # Vẽ vòng sáng xanh khi vào hunt
        if self.hunt_mode or self.entering_hunt_animation:
            glow_radius = self.tile_size // 2 + 6
            glow_center = (int(self.x + self.tile_size / 2), int(self.y + self.tile_size / 2))
            pygame.draw.circle(screen, (0, 255, 255), glow_center, glow_radius, 4)

        # Nhấp nháy trong hoạt cảnh
        if (self.entering_hunt_animation or self.exiting_hunt_animation) and (self.animation_counter // 4) % 2 == 0:
            return

        screen.blit(rotated_image, (self.x - offset, self.y - offset))

    def _try_move(self, step, game_map):
        epsilon = 0.1
        aligned_x = abs(self.x % self.tile_size) < epsilon
        aligned_y = abs(self.y % self.tile_size) < epsilon

        if aligned_x and aligned_y:
            if self.can_move(self.next_direction, game_map):
                self.direction = self.next_direction

        next_x = self.x + self.direction[0] * step
        next_y = self.y + self.direction[1] * step

        if self.can_move_pixel_based(next_x, next_y, game_map):
            self.x = next_x
            self.y = next_y
            return True
        else:
            if self.direction[0] != 0:
                self.x = round(self.x / self.tile_size) * self.tile_size
            if self.direction[1] != 0:
                self.y = round(self.y / self.tile_size) * self.tile_size
            return False

    def can_move(self, direction, game_map):
        dx, dy = direction
        x = int((self.x + dx * self.tile_size) // self.tile_size)
        y = int((self.y + dy * self.tile_size) // self.tile_size)
        return 0 <= y < len(game_map) and 0 <= x < len(game_map[0]) and game_map[y][x] in [0, 1, 2, 9, 10, 11]

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
            if game_map[y][x] not in [0, 1, 2, 9, 10, 11]:
                return False
        return True

    def _handle_teleport(self, game_map):
        if self.teleport_cooldown > 0:
            return

        col = int(self.x // self.tile_size)
        row = int(self.y // self.tile_size)
        num_cols = len(game_map[0])

        if game_map[row][col] == 10:
            for target_col in range(num_cols - 1, -1, -1):
                if game_map[row][target_col] == 11:
                    self.x = target_col * self.tile_size
                    self.teleport_cooldown = 20
                    return

        elif game_map[row][col] == 11:
            for target_col in range(num_cols):
                if game_map[row][target_col] == 10:
                    self.x = target_col * self.tile_size
                    self.teleport_cooldown = 20
                    return

    def set_direction(self, direction):
        self.next_direction = direction

    def _get_rotation_angle(self):
        dx, dy = self.direction
        if dx == 1: return 0
        if dx == -1: return 180
        if dy == -1: return 90
        if dy == 1: return 270
        return 0

    def hit_by_ghost(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = time.time()

    def activate_hunt(self):
        if not self.hunt_mode and not self.entering_hunt_animation:
            self.entering_hunt_animation = True
            self.hunt_anim_start_time = time.time()
        elif self.hunt_mode:
            self.hunt_start_time = time.time()
            self.exiting_hunt_animation = False
