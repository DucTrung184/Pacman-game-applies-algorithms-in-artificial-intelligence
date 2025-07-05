import pygame

MENU = "menu"
INSTRUCTION = "instruction"
PLAYING = "playing"

def load_font(path, size):
    return pygame.font.Font(path, size)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def render_line(text, font, color, align, surface, screen_width, y, max_width):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == "center":
        text_rect.centerx = screen_width // 2
    elif align == "left":
        text_rect.x = 60
    elif align == "right":
        text_rect.right = screen_width - 60

    text_rect.y = y
    surface.blit(text_surface, text_rect)

def draw_paragraphs(paragraphs, font_path, surface, screen_width, start_y, max_width, line_spacing=10):
    y = start_y
    for para in paragraphs:
        font = pygame.font.Font(font_path, para["size"])
        words = para["text"].split(' ')
        line = ''
        line_height = font.get_linesize() + line_spacing

        for word in words:
            test_line = line + word + ' '
            if font.size(test_line)[0] > max_width:
                render_line(line.strip(), font, para["color"], para["align"], surface, screen_width, y, max_width)
                y += line_height
                line = word + ' '
            else:
                line = test_line

        if line:
            render_line(line.strip(), font, para["color"], para["align"], surface, screen_width, y, max_width)
            y += line_height + 5  # thêm khoảng cách giữa các đoạn

def show_menu(screen, font, screen_width, screen_height, bg_img):
    screen.blit(bg_img, (0, 0))
    draw_text("Press ENTER to continue", font, (255, 255, 255), screen, screen_width // 2, screen_height - 220)
    pygame.display.update()

def show_instruction(screen, font_path, screen_width, screen_height, bg_img):
    screen.blit(bg_img, (0, 0))

    tutorial_lines = [
        {"text": "Welcome to PACMAN!", "size": 22, "align": "center", "color": (255, 255, 0)},
        {"text": "", "size": 16, "align": "center", "color": (255, 255, 255)},

        {"text": "Your goal is to eat all the energy pellets on the map while avoiding being caught by the ghosts.",
         "size": 16, "align": "left", "color": (255, 255, 255)},
        {"text": "", "size": 16, "align": "center", "color": (255, 255, 255)},

        {"text": "If you eat a power pellet, Pacman will enter hunt mode and can defeat the ghosts for 8 seconds.",
         "size": 16, "align": "left", "color": (255, 255, 255)},
        {"text": "", "size": 16, "align": "center", "color": (255, 255, 255)},

        {"text": "Use the arrow keys to control Pacman. You only have 3 lives. Be careful!",
         "size": 16, "align": "left", "color": (255, 255, 255)},
        {"text": "", "size": 16, "align": "center", "color": (255, 255, 255)},  # dòng trống
        
        {"text": "Press 'S' to start the game. Good luck!", "size": 18, "align": "center", "color": (0, 255, 0)},
    ]

    draw_paragraphs(
        paragraphs=tutorial_lines,
        font_path=font_path,
        surface=screen,
        screen_width=screen_width,
        start_y=80,
        max_width=screen_width - 120
    )

    pygame.display.update()

def play_menu_music(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Lặp vô hạn
