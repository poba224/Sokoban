import os
import pygame
import bfs
import astar

# Jelolesek
#   # fal
#   ' ' ures mezo
#   . celmezo
#   $ lada
#   * lada a celmezon
#   @ jatekos
#   + jatekos a celmezon


# Palya betoltese fajlbol
def load_level(file_path):
    f = open(file_path)
    text = f.read()
    f.close()
    lines = text.splitlines()
    return [list(line) for line in lines]


# Palya kivalasztasa itt
level_path = "levels/01.txt"

board = []
player_x = 0
player_y = 0
history = []
screen = None

tile_size = 64
info_height = 90
images = {}

# Billentyu -> iranyvektor
direction_by_key = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}

direction_by_letter = {
    "L": (-1, 0),
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
}


# PNG kepek betoltese
def load_images():
    image_paths = {
        "wall": "png/wall.png",
        "floor": "png/floor.png",
        "target": "png/target.png",
        "box": "png/box.png",
        "box_on_target": "png/box_on_target.png",
        "player": "png/player.png",
    }

    for name in image_paths:
        path = image_paths[name]
        img = pygame.image.load(path).convert_alpha()
        images[name] = pygame.transform.scale(img, (tile_size, tile_size))


# Kezdo jatekos pozicio megkeresese
def find_player():
    for row_index, board_row in enumerate(board):
        for column_index, tile in enumerate(board_row):
            if tile in "@+":
                return column_index, row_index
    return 0, 0


def get_height():
    return len(board)


def get_width():
    return max(len(row) for row in board)


def load_and_init(path):
    global level_path, board, player_x, player_y, history, screen
    level_path = path
    board = load_level(level_path)
    player_x, player_y = find_player()
    history = []
    screen = pygame.display.set_mode((get_width() * tile_size, get_height() * tile_size + info_height))
    pygame.display.set_caption("Sokoban-" + os.path.basename(level_path))


def list_levels():
    names = []
    for name in sorted(os.listdir("levels")):
        if name.endswith(".txt") and name != "solved.txt":
            names.append(name)
    return names


def next_level():
    names = list_levels()
    current_name = os.path.basename(level_path)
    found_index = -1
    for i in range(len(names)):
        if names[i] == current_name:
            found_index = i
    if 0 <= found_index < len(names) - 1:
        load_and_init("levels/" + names[found_index + 1])


# Akkor nyertunk ha mar nincs sima lada $ a palyan
def win():
    for board_row in board:
        if "$" in board_row:
            return False
    return True


def move(delta_x, delta_y):
    global player_x, player_y

    # Kovetkezo poziciok kiszamitasa
    next_player_x = player_x + delta_x
    next_player_y = player_y + delta_y
    pushed_box_x = player_x + 2 * delta_x
    pushed_box_y = player_y + 2 * delta_y

    # Lepes ervenyessegenek ellenorzese
    if not (0 <= next_player_y < get_height() and 0 <= next_player_x < len(board[next_player_y])):
        return

    next_tile = board[next_player_y][next_player_x]

    # Falba nem lehet lepni
    if next_tile == "#":
        return

    if next_tile in "$*":
        if not (0 <= pushed_box_y < get_height() and 0 <= pushed_box_x < len(board[pushed_box_y])):
            return
        if board[pushed_box_y][pushed_box_x] not in " .":
            return

    # Az undo-hoz
    history.append(([row[:] for row in board], player_x, player_y))

    # Aktualis mezo visszaallitasa
    if board[player_y][player_x] == "+":
        board[player_y][player_x] = "."
    else:
        board[player_y][player_x] = " "

    # Lada mozgatasa
    if next_tile in "$*":
        box_destination_tile = board[pushed_box_y][pushed_box_x]
        if box_destination_tile == ".":
            board[pushed_box_y][pushed_box_x] = "*"
        else:
            board[pushed_box_y][pushed_box_x] = "$"

    # Jatekos uj mezore helyezese
    if next_tile in ".*":
        board[next_player_y][next_player_x] = "+"
    else:
        board[next_player_y][next_player_x] = "@"

    player_x, player_y = next_player_x, next_player_y


# Egy lepes visszavonasa
def undo():
    global player_x, player_y
    if len(history) > 0:
        old_board, old_x, old_y = history.pop()
        for y in range(len(board)):
            for x in range(len(board[y])):
                board[y][x] = old_board[y][x]
        player_x = old_x
        player_y = old_y


# Vissza a palya kezdo allapotara
def reset():
    load_and_init(level_path)


# Solver megoldas lejatszasa lepesenkent
def play_solution(solution):
    if solution is None:
        return
    for letter in solution:
        delta = direction_by_letter[letter]
        move(delta[0], delta[1])
        draw(screen)
        pygame.display.flip()
        pygame.time.delay(150)


# A teljes palyat kirajzolja pygame-ben
def draw(screen):
    for row_index in range(get_height()):
        for column_index in range(get_width()):
            tile = board[row_index][column_index]
            rect = pygame.Rect(column_index * tile_size, row_index * tile_size, tile_size, tile_size)

            if tile == "#":
                screen.blit(images["wall"], rect)
            else:
                screen.blit(images["floor"], rect)

            if tile in ".+*":
                target_rect = images["target"].get_rect(center=rect.center)
                screen.blit(images["target"], target_rect)

            if tile == "$":
                screen.blit(images["box"], rect)

            if tile == "*":
                screen.blit(images["box_on_target"], rect)

            if tile in "@+":
                player_rect = images["player"].get_rect(center=rect.center)
                screen.blit(images["player"], player_rect)


# Sugo sav
def draw_help(screen, font):
    top = get_height() * tile_size
    width = get_width() * tile_size
    pygame.draw.rect(screen, pygame.Color("black"), (0, top, width, info_height))
    line1 = "Nyilak: mozgas    Z: undo    R: reset"
    line2 = "A: A* megoldas    B: BFS megoldas"
    if win():
        line3 = "MEGOLDVA!    Space: kovetkezo palya"
    else:
        line3 = "Space: kovetkezo palya (ha megoldott)"
    text1 = font.render(line1, True, pygame.Color("antiquewhite"))
    text2 = font.render(line2, True, pygame.Color("antiquewhite"))
    text3 = font.render(line3, True, pygame.Color("antiquewhite"))
    screen.blit(text1, (10, top + 8))
    screen.blit(text2, (10, top + 30))
    screen.blit(text3, (10, top + 52))


def main():
    pygame.init()
    load_and_init(level_path)
    load_images()
    font = pygame.font.SysFont(None, 18)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key in direction_by_key and not win():
                move(direction_by_key[event.key][0], direction_by_key[event.key][1])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z and not win():
                undo()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and win():
                next_level()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and not win():
                play_solution(astar.solve(board))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b and not win():
                play_solution(bfs.solve(board))
        draw(screen)
        draw_help(screen, font)
        pygame.display.flip()
        clock.tick(30)


main()
