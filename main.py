import pygame
from pygame import mixer
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 600  # Размеры окна
ROWS, COLS = 9, 9  # Количество строк и столбцов в Судоку
SQUARE_SIZE = WIDTH // COLS  # Размер одной клетки
GRID_COLOR = (0, 0, 0)  # Цвет сетки
SELECTED_COLOR = (100, 100, 255)  # Цвет выделенной клетки
WHITE = (255, 255, 255)  # Белый цвет
BLACK = (0, 0, 0)  # Черный цвет
FPS = 30  # Количество кадров в секунду

# Цвета для градиента
colors = [
    (255, 155, 170),  # Лососевый Крайола
    (255, 178, 139),  # Светлый желто-розовый
    (252, 232, 131),  # Желтый Крайола
    (190, 189, 127),  # Зелено-бежевый
    (198, 223, 144),  # Очень светлый желто-зеленый
    (153, 255, 153),  # Салатовый
    (175, 218, 252),  # Синий-синий иней
    (230, 230, 250)   # Лавандовый
]

# Пример заполненного поля Судоку
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 1, 6, 0],
    [8, 0, 0, 7, 6, 2, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 0, 0, 1],
    [7, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 6, 3, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 4, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0]
]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('СУДОКУ')

# Инициализация звукового модуля Pygame
mixer.init()

# Загрузка музыки
mixer.music.load('mp3.mp3')  # Укажите путь к вашему файлу с музыкой
mixer.music.play(-1)  # -1 для зацикливания музыки

# Шрифты
font = pygame.font.Font(None, 40)
fon = pygame.image.load('fon.jpg')
fon = pygame.transform.scale(fon, (WIDTH, HEIGHT))

# Функция для отрисовки градиента
def draw_gradient():
    num_colors = len(colors)
    stripe_height = HEIGHT // num_colors

    for i in range(num_colors):
        start_color = colors[i]
        end_color = colors[(i + 1) % num_colors]
        for y in range(stripe_height):
            ratio = y / stripe_height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, i * stripe_height + y), (WIDTH, i * stripe_height + y))

# Функция для отрисовки игрового поля
def draw_board():
    draw_gradient()
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, GRID_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if grid[row][col] != 0:
                text_surface = font.render(str(grid[row][col]), True, BLACK)
                text_rect = text_surface.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text_surface, text_rect)

# Функция для отрисовки выделенной клетки
def draw_selected(row, col):
    pygame.draw.rect(screen, SELECTED_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

# Функция для проверки ввода чисел от 1 до 9
def is_valid_input(key):
    return key.isdigit() and 1 <= int(key) <= 9

# Функция для проверки заполнения всех клеток
def is_board_full():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 0:
                return False
    return True

# Функция для проверки правильности заполнения судоку
def is_valid_move(row, col, num):
    # Проверка строки
    for x in range(COLS):
        if grid[row][x] == num:
            return False
    # Проверка колонки
    for x in range(ROWS):
        if grid[x][col] == num:
            return False
    # Проверка 3x3 блока
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

# Функция для отрисовки кнопок
def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    small_text = pygame.font.Font(None, 30)
    text_surf = small_text.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    screen.blit(text_surf, text_rect)

# Функция для выхода из игры
def quit_game():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

# Функция для перезапуска игры
def restart_game():
    pygame.mixer.music.stop()
    global grid, selected, game_over
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    selected = None
    game_over = False
    main_loop()

# Функция для основного меню
def main_menu():
    while True:
        screen.blit(fon, (0, 0))  # Отрисовка фона
        draw_button('СТАРТ', 200, 250, 200, 50, WHITE, SELECTED_COLOR, main_loop)  # Кнопка старта игры
        draw_button('ВЫХОД', 200, 350, 200, 50, WHITE, SELECTED_COLOR, quit_game)  # Кнопка выхода

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()

# Основная функция игры
def main_loop():
    global selected, game_over
    clock = pygame.time.Clock()
    selected = None
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                selected = (row, col)
            if not game_over and selected and event.type == pygame.KEYDOWN:
                if is_valid_input(event.unicode):
                    num = int(event.unicode)
                    if is_valid_move(selected[0], selected[1], num):
                        grid[selected[0]][selected[1]] = num
                    selected = None
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    grid[selected[0]][selected[1]] = 0
                    selected = None

        draw_board()
        if selected:
            draw_selected(selected[0], selected[1])

        if is_board_full():
            if all(is_valid_move(row, col, grid[row][col]) for row in range(ROWS) for col in range(COLS) if grid[row][col] != 0):
                pygame.mixer.music.stop()
                game_over = True
                text_surface = font.render('You Win!', True, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text_surface, text_rect)
            else:
                game_over = True
                text_surface = font.render('Invalid Solution!', True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text_surface, text_rect)
            draw_button('Restart', 200, 400, 200, 50, WHITE, SELECTED_COLOR, restart_game)
            draw_button('Quit', 200, 500, 200, 50, WHITE, SELECTED_COLOR, quit_game)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()
