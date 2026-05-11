import os
import pygame
import time
import astar


# Palya ervenyesseg ellenorzes kezzel keszitett palyakhoz csak
allowed_tiles = "# .$*@+"


def validate_level(board):
    if len(board) == 0:
        return False, "ures palya"

    players = []
    boxes = []
    goals = []

    for y in range(len(board)):
        for x in range(len(board[y])):
            tile = board[y][x]
            if tile not in allowed_tiles:
                row_text = str(y + 1)
                column_text = str(x + 1)
                return False, "tiltott karakter '" + tile + "' a (" + row_text + "," + column_text + ") helyen"
            if tile in "@+":
                players.append((x, y))
            if tile in "$*":
                boxes.append((x, y))
            if tile in ".+*":
                goals.append((x, y))

    if len(players) == 0:
        return False, "nincs jatekos"
    if len(players) > 1:
        return False, "tobb jatekos van"

    if len(boxes) == 0:
        return False, "nincs doboz a palyan"

    if len(boxes) != len(goals):
        box_text = str(len(boxes))
        goal_text = str(len(goals))
        return False, "dobozok szama (" + box_text + ") nem egyezik a celok szamaval (" + goal_text + ")"

    return True, "OK"


# Itt allithato, hova mentsen az editor
level_path = "levels/sajat_01.txt"
solved_path = "levels/solved.txt"
level_prefix = "sajat_"
editor_width = 15
editor_height = 10
tile_size = 48
info_height = 150

images = {}
selected_index = 0
help_text = "S uj fajlba ment+A* | A A* | V valid | N uj | bal katt lerak | jobb katt torol"
status_text = "Kesz"

tiles = [
    ("#", "fal"),
    (" ", "padlo"),
    (".", "cel"),
    ("$", "lada"),
    ("@", "jatekos"),
    ("*", "lada celon"),
    ("+", "jatekos celon"),
]


def load_images():
    image_paths = {
        "#": "png/wall.png",
        " ": "png/floor.png",
        ".": "png/target.png",
        "$": "png/box.png",
        "*": "png/box_on_target.png",
        "@": "png/player.png",
        "+": "png/player.png",
    }

    for tile in image_paths:
        path = image_paths[tile]
        img = pygame.image.load(path).convert_alpha()
        images[tile] = pygame.transform.scale(img, (tile_size, tile_size))


def make_empty_board(width, height):
    new_board = []
    for y in range(height):
        row = []
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                row.append("#")
            else:
                row.append(" ")
        new_board.append(row)
    return new_board


def load_level(file_path):
    f = open(file_path)
    text = f.read()
    f.close()
    lines = text.splitlines()
    board = []
    for line in lines:
        board.append(list(line))
    return board


def normalize_board(board):
    width = 0
    for row in board:
        if len(row) > width:
            width = len(row)

    for row in board:
        while len(row) < width:
            row.append(" ")

    return board


def load_or_make_board():
    if os.path.exists(level_path):
        loaded_board = load_level(level_path)
        return normalize_board(loaded_board)
    return make_empty_board(editor_width, editor_height)


def board_to_text(board):
    lines = []
    for row in board:
        lines.append("".join(row))
    return "\n".join(lines) + "\n"


def save_board(board):
    os.makedirs("levels", exist_ok=True)
    f = open(level_path, "w")
    f.write(board_to_text(board))
    f.close()


def make_level_path(number):
    number_text = str(number).zfill(2)
    return "levels/" + level_prefix + number_text + ".txt"


def next_level_path():
    number = 1
    path = make_level_path(number)

    while os.path.exists(path):
        number += 1
        path = make_level_path(number)

    return path


def read_solved_lines():
    lines = []
    if os.path.exists(solved_path):
        f = open(solved_path, encoding="utf-8")
        text = f.read()
        f.close()
        lines = text.splitlines()
    return lines


def write_solved_lines(lines):
    os.makedirs("levels", exist_ok=True)
    f = open(solved_path, "w", encoding="utf-8")
    for line in lines:
        f.write(line + "\n")
    f.close()


def make_solved_line(level_name, ido, hossz, megoldas):
    return level_name + "," + str(ido) + "," + str(hossz) + "," + megoldas + ",,"


def update_solved_file(level_name, ido, solution):
    header = "level,ido,hossz,megoldas,probalkozasok,probalkozas_ido"
    lines = read_solved_lines()
    if len(lines) == 0:
        lines.append(header)

    new_line = make_solved_line(level_name, ido, len(solution), solution)
    new_lines = [lines[0]]
    found = False

    for i in range(1, len(lines)):
        line = lines[i]
        parts = line.split(",")
        if len(parts) > 0 and parts[0] == level_name:
            new_lines.append(new_line)
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(new_line)

    write_solved_lines(new_lines)


def solve_board_with_astar(board):
    start_time = time.time()
    solution = astar.solve(board, None)
    elapsed = time.time() - start_time
    return solution, elapsed


def remove_player(board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == "@":
                board[y][x] = " "
            if board[y][x] == "+":
                board[y][x] = "."


def place_tile(board, x, y, tile):
    if 0 <= y < len(board):
        if 0 <= x < len(board[y]):
            if tile in "@+":
                remove_player(board)
            board[y][x] = tile


def draw_tile(screen, tile, rect):
    screen.blit(images[" "], rect)

    if tile == "#":
        screen.blit(images["#"], rect)

    if tile != "#":
        if tile in ".+*":
            screen.blit(images["."], rect)
        if tile == "$":
            screen.blit(images["$"], rect)
        if tile == "*":
            screen.blit(images["*"], rect)
        if tile in "@+":
            screen.blit(images["@"], rect)


def draw_small_tile(screen, tile, rect):
    small = pygame.transform.scale(images[" "], (rect.width, rect.height))
    screen.blit(small, rect)

    if tile == "#":
        small = pygame.transform.scale(images["#"], (rect.width, rect.height))
        screen.blit(small, rect)

    if tile != "#":
        if tile in ".+*":
            small = pygame.transform.scale(images["."], (rect.width, rect.height))
            screen.blit(small, rect)
        if tile == "$":
            small = pygame.transform.scale(images["$"], (rect.width, rect.height))
            screen.blit(small, rect)
        if tile == "*":
            small = pygame.transform.scale(images["*"], (rect.width, rect.height))
            screen.blit(small, rect)
        if tile in "@+":
            small = pygame.transform.scale(images["@"], (rect.width, rect.height))
            screen.blit(small, rect)


def draw_board(screen, board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            draw_tile(screen, board[y][x], rect)


def draw_info(screen, board, font):
    top = len(board) * tile_size
    width = len(board[0]) * tile_size
    pygame.draw.rect(screen, pygame.Color("black"), (0, top, width, info_height))

    help_surface = font.render(help_text, True, pygame.Color("antiquewhite"))
    screen.blit(help_surface, (10, top + 8))

    text = font.render(status_text, True, pygame.Color("white"))
    screen.blit(text, (10, top + 30))

    x = 10
    y = top + 60
    for index in range(len(tiles)):
        tile = tiles[index][0]
        name = tiles[index][1]
        rect = pygame.Rect(x, y, 28, 28)
        draw_small_tile(screen, tile, rect)
        if index == selected_index:
            pygame.draw.rect(screen, pygame.Color("yellow"), rect, 3)
        label = font.render(str(index + 1) + " " + name, True, pygame.Color("white"))
        screen.blit(label, (x + 34, y + 7))
        x += 120
        if x + 120 > width:
            x = 10
            y += 34


def validate_and_set_status(board):
    global status_text
    ervenyes, uzenet = validate_level(board)
    if ervenyes:
        status_text = "Ervenyes palya"
    else:
        status_text = "Ervenytelen palya: " + uzenet
    return ervenyes


def astar_and_set_status(board):
    global status_text
    status_text = "A* ellenorzes fut ido korlat nelkul..."
    solution, elapsed = solve_board_with_astar(board)
    if solution is None:
        status_text = "Nincs A* megoldas, nincs mentve"
        return None
    status_text = "A* OK: " + str(len(solution)) + " lepes, " + str(round(elapsed, 4)) + "s"
    return solution, elapsed


def validate_and_astar(board):
    ervenyes = validate_and_set_status(board)
    if ervenyes:
        return astar_and_set_status(board)
    return None


def save_if_valid(board):
    global status_text, level_path
    result = validate_and_astar(board)
    if result is not None:
        solution = result[0]
        elapsed = result[1]
        level_path = next_level_path()
        save_board(board)
        saved_path = level_path
        level_name = os.path.basename(saved_path)
        update_solved_file(level_name, round(elapsed, 4), solution)
        level_path = next_level_path()
        pygame.display.set_caption("Sokoban palya editor - kovetkezo: " + level_path)
        status_text = "Mentve uj fajlba: " + saved_path + ", " + str(len(solution)) + " lepes"


def handle_key(event, board):
    global selected_index, status_text, level_path

    if event.key == pygame.K_1:
        selected_index = 0
    if event.key == pygame.K_2:
        selected_index = 1
    if event.key == pygame.K_3:
        selected_index = 2
    if event.key == pygame.K_4:
        selected_index = 3
    if event.key == pygame.K_5:
        selected_index = 4
    if event.key == pygame.K_6:
        selected_index = 5
    if event.key == pygame.K_7:
        selected_index = 6

    if event.key == pygame.K_s:
        save_if_valid(board)
    if event.key == pygame.K_a:
        validate_and_astar(board)
    if event.key == pygame.K_v:
        validate_and_set_status(board)
    if event.key == pygame.K_n:
        new_board = make_empty_board(editor_width, editor_height)
        board.clear()
        for row in new_board:
            board.append(row)
        level_path = next_level_path()
        pygame.display.set_caption("Sokoban palya editor - kovetkezo: " + level_path)
        status_text = "Uj palya: " + level_path


def handle_mouse(event, board):
    x = event.pos[0] // tile_size
    y = event.pos[1] // tile_size
    if 0 <= y < len(board):
        if 0 <= x < len(board[y]):
            if event.button == 1:
                tile = tiles[selected_index][0]
                place_tile(board, x, y, tile)
            if event.button == 3:
                place_tile(board, x, y, " ")


def main():
    global level_path
    pygame.init()
    level_path = next_level_path()
    board = load_or_make_board()
    width = len(board[0]) * tile_size
    height = len(board) * tile_size + info_height
    screen = pygame.display.set_mode((width, height))
    load_images()
    pygame.display.set_caption("Sokoban palya editor - kovetkezo: " + level_path)
    font = pygame.font.SysFont(None, 20)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                handle_key(event, board)
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse(event, board)

        draw_board(screen, board)
        draw_info(screen, board, font)
        pygame.display.flip()
        clock.tick(30)


main()
