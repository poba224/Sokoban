import heapq
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


# A palyabol kigyujti a falakat, celokat, ladakat es a jatekost
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


# Greedy modszerrel minden lada kap egy kozeli, meg szabad celt
def heuristic(boxes, goals):
    total = 0
    unused_goals = list(goals)

    for box_x, box_y in boxes:
        best_goal = None
        best_distance = None

        for goal in unused_goals:
            goal_x, goal_y = goal
            distance = abs(box_x - goal_x) + abs(box_y - goal_y)

            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_goal = goal

        if best_goal is not None:
            total += best_distance
            unused_goals.remove(best_goal)

    return 2 * total


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


# A* kereses
def solve(board, max_seconds=6):
    walls, goals, boxes, player_x, player_y = parse_board(board)
    start_time = time.time()

    start_boxes = frozenset(boxes)

    counter = 0
    heap = []
    start_priority = heuristic(start_boxes, goals)
    heapq.heappush(heap, (start_priority, 0, counter, player_x, player_y, start_boxes, ""))

    visited = set()

    # Mindig a legjobb becsult allapot jon elo
    while heap:
        if max_seconds is not None and time.time() - start_time > max_seconds:
            return None

        priority, cost, heap_order, px, py, current_boxes, path = heapq.heappop(heap)

        state = ((px, py), current_boxes)
        if state in visited:
            continue
        visited.add(state)

        if solved(current_boxes, goals):
            return path

        for letter, dx, dy in directions:
            result = try_move(px, py, current_boxes, dx, dy, walls)
            if result is not None:
                nx, ny, new_boxes = result
                new_state = ((nx, ny), new_boxes)
                if new_state not in visited:
                    new_cost = cost + 1
                    new_priority = new_cost + heuristic(new_boxes, goals)
                    counter += 1
                    heapq.heappush(heap, (new_priority, new_cost, counter, nx, ny, new_boxes, path + letter))

    return None


def main():
    level_path = "levels/38.txt"
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
