import time

directions = [
    ("L", -1, 0),
    ("U", 0, -1),
    ("R", 1, 0),
    ("D", 0, 1),
]


def load_level(file_path):
    f = open(file_path)
    text = f.read()
    f.close()
    lines = text.splitlines()
    board = []
    for line in lines:
        row = list(line)
        board.append(row)
    return board


def parse_board(board):
    walls = set()
    goals = set()
    boxes = set()
    player_x = 0
    player_y = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            tile = board[y][x]
            if tile == "#":
                walls.add((x, y))
            if tile in ".+*":
                goals.add((x, y))
            if tile in "$*":
                boxes.add((x, y))
            if tile in "@+":
                player_x = x
                player_y = y
    return walls, goals, boxes, player_x, player_y


def solved(boxes, goals):
    for box in boxes:
        if box not in goals:
            return False
    return True


def try_move(px, py, current_boxes, dx, dy, walls):
    nx = px + dx
    ny = py + dy
    if (nx, ny) in walls:
        return None
    if (nx, ny) not in current_boxes:
        return nx, ny, current_boxes
    bx = nx + dx
    by = ny + dy
    if (bx, by) in walls:
        return None
    if (bx, by) in current_boxes:
        return None
    new_boxes = set(current_boxes)
    new_boxes.remove((nx, ny))
    new_boxes.add((bx, by))
    return nx, ny, frozenset(new_boxes)


# BFS kereses
def solve(board):
    walls, goals, boxes, player_x, player_y = parse_board(board)

    start_boxes = frozenset(boxes)

    if solved(start_boxes, goals):
        return ""

    queue = []
    queue.append((player_x, player_y, start_boxes, ""))
    head = 0
    visited = set()
    visited.add(((player_x, player_y), start_boxes))

    # Sorban nezi a lehetseges allapotokat
    while head < len(queue):
        px, py, current_boxes, path = queue[head]
        head += 1

        for letter, dx, dy in directions:
            result = try_move(px, py, current_boxes, dx, dy, walls)
            if result is not None:
                nx, ny, new_boxes = result
                state = ((nx, ny), new_boxes)
                if state not in visited:
                    visited.add(state)
                    if solved(new_boxes, goals):
                        return path + letter
                    queue.append((nx, ny, new_boxes, path + letter))

    return None


def main():
    level_path = "levels/01.txt"
    board = load_level(level_path)
    start_time = time.time()
    solution = solve(board)
    elapsed = time.time() - start_time
    if solution is None:
        print("Nincs megoldas")
    else:
        print("Megoldas: " + solution)
        print("Hossz: " + str(len(solution)))
        print("Ido: " + str(round(elapsed, 4)) + "s")


if __name__ == "__main__":
    main()
