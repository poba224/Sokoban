# Jelolesek
#   # fal
#   ' ' ures mezo
#   . celmezo
#   $ lada
#   * lada a celmezon
#   @ jatekos
#   + jatekos a celmezon

# Demo palya
board = [list(level_row_text) for level_row_text in [
    "######",
    "#  @.#",
    "#   $#",
    "# $  #",
    "#  . #",
    "######"
]]

# Palya meretek
board_height = len(board)
board_width = max(len(board_row) for board_row in board)

# Kezdo jatekos pozicio megkeresese
for row_index in range(board_height):
    for column_index in range(len(board[row_index])):
        if board[row_index][column_index] in "@+":
            player_x, player_y = column_index, row_index


# A teljes palyat kiirasa
def show():
    for board_row in board:
        print("".join(board_row))
    print()


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


# Billentyu -> iranyvektor
direction_by_key = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


while True:
    show()

    if win():
        print("Solved!")
        break

    pressed_key = input("w a s d: ")
    if pressed_key in direction_by_key:
        move(direction_by_key[pressed_key][0], direction_by_key[pressed_key][1])
