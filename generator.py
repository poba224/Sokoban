import random
import os
import time
import astar

# meret, darab, min_fal, max_fal, min_lada, max_lada
level_settings = [
    (10, 20, 6, 10, 1, 2),
    (11, 15, 8, 14, 1, 4),
    (12, 10, 10, 18, 2, 5),
]
max_attempts = 100
solver_timeout = 6


# Random palya generalas adott meretre
def random_level(size, min_walls, max_walls, min_boxes, max_boxes):
    board = []
    for y in range(size):
        row = []
        for x in range(size):
            if x == 0 or y == 0 or x == size - 1 or y == size - 1:
                row.append("#")
            else:
                row.append(" ")
        board.append(row)

    inner_cells = []
    for y in range(1, size - 1):
        for x in range(1, size - 1):
            inner_cells.append((x, y))

    wall_count = random.randint(min_walls, max_walls)
    wall_positions = random.sample(inner_cells, wall_count)
    for wx, wy in wall_positions:
        board[wy][wx] = "#"

    free_cells = []
    for y in range(1, size - 1):
        for x in range(1, size - 1):
            if board[y][x] == " ":
                free_cells.append((x, y))

    box_count = random.randint(min_boxes, max_boxes)
    needed = 1 + box_count
    if needed > len(free_cells):
        return None
    placed = random.sample(free_cells, needed)
    player_pos = placed[0]
    box_positions = placed[1:]

    goal_positions = random.sample(free_cells, box_count)

    for gx, gy in goal_positions:
        board[gy][gx] = "."

    for bx, by in box_positions:
        if board[by][bx] == ".":
            board[by][bx] = "*"
        else:
            board[by][bx] = "$"

    px, py = player_pos
    if board[py][px] == ".":
        board[py][px] = "+"
    else:
        board[py][px] = "@"

    return board


def board_to_text(board):
    lines = []
    for row in board:
        lines.append("".join(row))
    return "\n".join(lines) + "\n"


def save_solved(levels_dir, solved_lines):
    solved_path = os.path.join(levels_dir, "solved.txt")
    f = open(solved_path, "w")
    f.write("\n".join(solved_lines) + "\n")
    f.close()


def main():
    levels_dir = "levels"
    os.makedirs(levels_dir, exist_ok=True)

    solved_lines = ["level,ido,hossz,megoldas,probalkozasok,probalkozas_ido"]
    level_index = 1

    for size, count, min_walls, max_walls, min_boxes, max_boxes in level_settings:
        made = 0
        while made < count:
            attempts = 0
            generation_start = time.time()
            board = None
            solution = None
            solver_elapsed = 0.0

            while solution is None or len(solution) == 0:
                if attempts >= max_attempts:
                    save_solved(levels_dir, solved_lines)
                    print("Nem sikerult a " + str(level_index).zfill(2) + ". palyat generalni.")
                    print("Max probalkozas: " + str(max_attempts))
                    return
                attempts += 1
                board = random_level(size, min_walls, max_walls, min_boxes, max_boxes)
                if board is not None:
                    solver_start = time.time()
                    solution = astar.solve(board, solver_timeout)
                    solver_elapsed = time.time() - solver_start
            generation_time = time.time() - generation_start

            # Palya mentese
            file_name = str(level_index).zfill(2) + ".txt"
            file_path = os.path.join(levels_dir, file_name)
            f = open(file_path, "w")
            f.write(board_to_text(board))
            f.close()

            # Eredmenysor solved.txt-hez
            solver_time_text = str(round(solver_elapsed, 4))
            solution_length_text = str(len(solution))
            attempts_text = str(attempts)
            generation_time_text = str(round(generation_time, 4))
            line = file_name + "," + solver_time_text + "," + solution_length_text
            line = line + "," + solution + "," + attempts_text + "," + generation_time_text
            solved_lines.append(line)
            print("Kesz: " + line)

            level_index += 1
            made += 1

    save_solved(levels_dir, solved_lines)
    print("Osszes palya kesz, solved.txt elmentve.")


main()
