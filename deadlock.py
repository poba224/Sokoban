
directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def parse_board(board):
    walls = set()
    goals = set()
    boxes = set()
    player_x = 0
    player_y = 0

    height = len(board)
    width = 0
    for row in board:
        if len(row) > width:
            width = len(row)

    for y in range(height):
        for x in range(width):
            if x < len(board[y]):
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
            else:
                walls.add((x, y))

    return walls, goals, boxes, player_x, player_y


def compute_dead_squares(walls, goals, height, width):
    alive = set()

    for goal in goals:
        stack = []
        stack.append(goal)
        head = 0
        local_seen = set()
        local_seen.add(goal)
        alive.add(goal)

        while head < len(stack):
            px, py = stack[head]
            head += 1

            for dx, dy in directions:
                qx = px - dx
                qy = py - dy
                pusher_x = px - 2 * dx
                pusher_y = py - 2 * dy
                in_bounds_q = 0 <= qx < width and 0 <= qy < height
                in_bounds_pusher = 0 <= pusher_x < width and 0 <= pusher_y < height

                if in_bounds_q and in_bounds_pusher:
                    if (qx, qy) not in walls:
                        if (pusher_x, pusher_y) not in walls:
                            if (qx, qy) not in local_seen:
                                local_seen.add((qx, qy))
                                alive.add((qx, qy))
                                stack.append((qx, qy))

    dead = set()
    for y in range(height):
        for x in range(width):
            if (x, y) not in walls:
                if (x, y) not in alive:
                    dead.add((x, y))

    return dead


def is_dead_state(boxes, goals, dead_squares):
    for box in boxes:
        if box in dead_squares:
            if box not in goals:
                return True
    return False
