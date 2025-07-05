import random
from queue import PriorityQueue, Queue

# Các ô mà ghost được phép di chuyển
VALID_TILES = [0, 1, 2, 9]

# Các hướng: Lên, Xuống, Trái, Phải (dy, dx)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_valid(game_map, pos):
    y, x = pos
    return (
        0 <= y < len(game_map) and
        0 <= x < len(game_map[0]) and
        game_map[y][x] in VALID_TILES
    )

def a_star(start, goal, game_map):
    queue = PriorityQueue()
    queue.put((0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while not queue.empty():
        _, current = queue.get()

        if current == goal:
            break

        for dy, dx in DIRECTIONS:
            next_pos = (current[0] + dy, current[1] + dx)
            if not is_valid(game_map, next_pos):
                continue

            new_cost = cost_so_far[current] + 1
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + manhattan(goal, next_pos)
                queue.put((priority, next_pos))
                came_from[next_pos] = current

    # Truy vết đường đi
    path = []
    current = goal
    while current != start:
        if current not in came_from:
            return []  # Không tìm thấy đường
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def bfs(start, goal, game_map):
    queue = Queue()
    queue.put(start)
    came_from = {start: None}

    while not queue.empty():
        current = queue.get()

        if current == goal:
            break

        for dy, dx in DIRECTIONS:
            next_pos = (current[0] + dy, current[1] + dx)
            if is_valid(game_map, next_pos) and next_pos not in came_from:
                queue.put(next_pos)
                came_from[next_pos] = current

    # Truy vết đường đi
    path = []
    current = goal
    while current != start:
        if current not in came_from:
            return []  # Không tìm thấy đường
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
