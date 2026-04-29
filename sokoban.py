import pygame

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
level_path = "levels/36.txt"
board = load_level(level_path)

# Palya meretek
board_height = len(board)
board_width = max(len(board_row) for board_row in board)

tile_size = 64
gray = pygame.Color("gray")  # fal
beige = pygame.Color("lightgray")  # padlo
red = pygame.Color("red")  # cel
brown = pygame.Color("peru")  # lada
blue = pygame.Color("blue")  # jatekos

# Billentyu -> iranyvektor
direction_by_key = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}

# Kezdo jatekos pozicio megkeresese
def find_player():
    for row_index, board_row in enumerate(board):
        for column_index, tile in enumerate(board_row):
            if tile in "@+":
                return column_index, row_index
    return 0, 0

player_x, player_y = find_player()

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
    if not (0 <= next_player_y < board_height and 0 <= next_player_x < len(board[next_player_y])):
        return

    next_tile = board[next_player_y][next_player_x]

    # Falba nem lehet lepni
    if next_tile == "#":
        return

    if next_tile in "$*":
        if not (0 <= pushed_box_y < board_height and 0 <= pushed_box_x < len(board[pushed_box_y])):
            return
        if board[pushed_box_y][pushed_box_x] not in " .":
            return

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

# A teljes palyat kirajzolja pygame-ben
def draw(screen):
    for row_index in range(board_height):
        for column_index in range(board_width):
            tile = board[row_index][column_index]
            rect = pygame.Rect(column_index * tile_size, row_index * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, gray if tile == "#" else beige, rect)
            if tile in "$*":
                pygame.draw.rect(screen, brown, rect)
            if tile in "@+":
                pygame.draw.circle(screen, blue, rect.center, tile_size // 3)
            if tile in ".+*":
                pygame.draw.circle(screen, red, rect.center, tile_size // 8)


def main():
    pygame.init()
    screen = pygame.display.set_mode((board_width * tile_size, board_height * tile_size))
    clock = pygame.time.Clock()

    solved_printed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key in direction_by_key and not win():
                move(direction_by_key[event.key][0], direction_by_key[event.key][1])
        if win() and not solved_printed:
            print("MEGOLDVA!")
            solved_printed = True
        draw(screen)
        pygame.display.flip()
        clock.tick(30)


main()
