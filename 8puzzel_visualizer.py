#===================================================================
#                 Visualizer BFS 8PUZZEL
# Link GitHub: https://github.com/NguyenTrungKien1805/8puzzel_visualizer
#===================================================================
import flet as ft
from collections import deque
import copy

# =========================
# START + GOAL
# =========================
START = [
    [1, 3, 0],
    [4, 2, 5],
    [7, 8, 6]
]

GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]


# =========================
# HELPER FUNCTIONS
# =========================
def to_tuple(state):
    return tuple(tuple(row) for row in state)

def state_to_string(state):
    return "\n".join(" ".join(str(x) for x in row) for row in state) + "\n"

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1


def next_states(state):
    x, y = find_zero(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            result.append(new_state)
    return result


def format_state(state):
    return "\n".join(" ".join(str(x) for x in row) for row in state)


# ===================================================
# HÀM 1: CHECK LÚC POP + ADD REACHED LÚC POP
# ===================================================
def bfs_check_on_pop(start, goal):
    queue = deque()
    queue.append((start, [start], 0))

    reached = set()
    explored_edges = []
    node_levels = {state_to_string(start): 0}
    bfs_log = "=== HÀM 1: CHECK ĐÍCH LÚC POP + ADD REACHED LÚC POP ===\n\n"
    step_count = 0

    while queue:
        current, path, level = queue.popleft()
        current_tuple = to_tuple(current)

        # Nhét vào reached khi POP
        reached.add(current_tuple)
        curr_str = state_to_string(current)
        step_count += 1

        # Check đích khi POP
        if current == goal:
            bfs_log += f"\nGOAL FOUND AT STEP {step_count}\n\n"
            return path, explored_edges, node_levels, bfs_log

        for nxt in next_states(current):
            nxt_tuple = to_tuple(nxt)
            nxt_str = state_to_string(nxt)
            explored_edges.append((curr_str, nxt_str))

            in_frontier = any(to_tuple(item[0]) == nxt_tuple for item in queue)

            if nxt_tuple not in reached and not in_frontier:
                node_levels[nxt_str] = level + 1
                queue.append((nxt, path + [nxt], level + 1))

        # --- IN LOG ---
        node_text = format_state(current)
        frontier_text = "".join(format_state(item[0]) + "\n---\n" for item in queue)
        reached_text = "".join(format_state([list(row) for row in r]) + "\n---\n" for r in reached)

        node_lines, frontier_lines, reached_lines = node_text.splitlines(), frontier_text.splitlines(), reached_text.splitlines()
        max_lines = max(len(node_lines), len(frontier_lines), len(reached_lines))
        while len(node_lines) < max_lines: node_lines.append("")
        while len(frontier_lines) < max_lines: frontier_lines.append("")
        while len(reached_lines) < max_lines: reached_lines.append("")

        bfs_log += f"\nSTEP {step_count}\nNODE".ljust(25) + "FRONTIER".ljust(35) + "REACHED\n" + "=" * 90 + "\n"
        for i in range(max_lines):
            bfs_log += node_lines[i].ljust(20) + frontier_lines[i].ljust(35) + reached_lines[i] + "\n"

    bfs_log += "\nFAILURE\n"
    return None, explored_edges, node_levels, bfs_log


# ===================================================
# HÀM 2: CHECK LÚC SINH (PUSH) + NHÉT THẲNG VÀO REACHED LUÔN
# ===================================================
def bfs_check_on_push_and_reached(start, goal):
    queue = deque()
    queue.append((start, [start], 0))

    reached = set()
    # Nhét luôn trạng thái start vào reached từ đầu
    reached.add(to_tuple(start))

    explored_edges = []
    node_levels = {state_to_string(start): 0}
    bfs_log = "=== HÀM 2: CHECK ĐÍCH LÚC SINH (PUSH)===\n\n"
    step_count = 0

    if start == goal:
        bfs_log += "GOAL FOUND AT START STEP\n"
        return [start], explored_edges, node_levels, bfs_log

    while queue:
        current, path, level = queue.popleft()
        curr_str = state_to_string(current)
        step_count += 1

        for nxt in next_states(current):
            nxt_tuple = to_tuple(nxt)
            nxt_str = state_to_string(nxt)
            explored_edges.append((curr_str, nxt_str))

            # Vì đã nhét thẳng vào reached khi sinh ra, ta KHÔNG CẦN check `in_frontier` nữa
            # Đã vào frontier là chắc chắn đã nằm trong reached!
            if nxt_tuple not in reached:

                # 1. NHÉT THẲNG VÀO REACHED LUÔN KHI VỪA SINH RA
                reached.add(nxt_tuple)
                node_levels[nxt_str] = level + 1
                new_path = path + [nxt]

                # 2. KIỂM TRA ĐÍCH NGAY LÚC SINH
                if nxt == goal:
                    bfs_log += f"\nSTEP {step_count}\nNODE".ljust(25) + "FRONTIER".ljust(
                        35) + "REACHED\n" + "=" * 90 + "\n"
                    bfs_log += format_state(current).splitlines()[0].ljust(
                        20) + "FOUND GOAL IN CURRENT PUSH TRÊN FRONTIER!\n"
                    bfs_log += f"\nGOAL FOUND AT STEP {step_count} (LÚC VỪA SINH RA CON ĐÍCH)\n\n"
                    return new_path, explored_edges, node_levels, bfs_log

                queue.append((nxt, new_path, level + 1))

        # --- IN LOG ---
        node_text = format_state(current)
        frontier_text = "".join(format_state(item[0]) + "\n---\n" for item in queue)
        reached_text = "".join(format_state([list(row) for row in r]) + "\n---\n" for r in reached)

        node_lines, frontier_lines, reached_lines = node_text.splitlines(), frontier_text.splitlines(), reached_text.splitlines()
        max_lines = max(len(node_lines), len(frontier_lines), len(reached_lines))
        while len(node_lines) < max_lines: node_lines.append("")
        while len(frontier_lines) < max_lines: frontier_lines.append("")
        while len(reached_lines) < max_lines: reached_lines.append("")

        bfs_log += f"\nSTEP {step_count}\nNODE".ljust(25) + "FRONTIER".ljust(35) + "REACHED\n" + "=" * 90 + "\n"
        for i in range(max_lines):
            bfs_log += node_lines[i].ljust(20) + frontier_lines[i].ljust(35) + reached_lines[i] + "\n"

    bfs_log += "\nFAILURE\n"
    return None, explored_edges, node_levels, bfs_log


# =========================
# MAIN UI APPLICATION
# =========================
def main(page: ft.Page):
    page.title = "8 Puzzle BFS Dual Mode (Strict Reached)"
    page.window_width = 1050
    page.window_height = 680
    page.theme_mode = ft.ThemeMode.DARK
    page.window_center()

    solution = [[]]
    current_step = [0]

    # --- KHỐI BÊN TRÁI: BÀN CỜ & ĐIỀU HƯỚNG ---
    title = ft.Text("8 Puzzle BFS Solver", size=26, weight=ft.FontWeight.BOLD, color="blue")
    info = ft.Text("Chọn hàm thuật toán và bấm 'Giải BFS'.", size=14, italic=True)
    grid = ft.Column(spacing=6, alignment=ft.MainAxisAlignment.CENTER)

    # Bộ điều hướng chọn Hàm bằng RadioGroup
    bfs_mode_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="pop", label="Hàm 1: Check khi POP + Add Reached khi POP"),
            ft.Radio(value="push", label="Hàm 2: Check khi SINH + Add Reached NGAY"),
        ], spacing=5),
        value="pop"
    )

    def draw_board(board):
        grid.controls.clear()
        for row in board:
            r = ft.Row(spacing=6, alignment=ft.MainAxisAlignment.CENTER)
            for num in row:
                is_zero = (num == 0)
                cell = ft.Container(
                    content=ft.Text(
                        "" if is_zero else str(num),
                        size=24,
                        color="white" if not is_zero else "transparent",
                        weight=ft.FontWeight.BOLD
                    ),
                    width=75,
                    height=75,
                    bgcolor="grey" if is_zero else "blue",
                    border_radius=10,
                    alignment=ft.alignment.center
                )
                r.controls.append(cell)
            grid.controls.append(r)

    draw_board(START)

    # --- KHỐI BÊN PHẢI: KHUNG HIỂN THỊ LOG ---
    path_output = ft.TextField(
        multiline=True,
        min_lines=22,
        max_lines=22,
        read_only=True,
        value="Nhật ký chạy của hàm được chọn sẽ hiển thị trực quan tại đây...",
        text_style=ft.TextStyle(font_family="monospace", size=13),
        expand=True
    )

    def solve_click(e):
        info.value = "Đang chạy thuật toán... Xin chờ!"
        path_output.value = "Hệ thống đang thực thi..."
        page.update()

        # Gọi hàm tương ứng dựa theo UI lựa chọn
        if bfs_mode_radio.value == "pop":
            path, explored_edges, node_levels, bfs_log = bfs_check_on_pop(START, GOAL)
        else:
            path, explored_edges, node_levels, bfs_log = bfs_check_on_push_and_reached(START, GOAL)

        path_output.value = bfs_log

        if path:
            solution[0] = path
            current_step[0] = 0
            draw_board(path[0])
            info.value = f"Hoàn thành! Số bước đường đi: {len(path) - 1} bước."
        else:
            info.value = "Không tìm thấy lời giải!"
        page.update()

    def next_click(e):
        if not solution[0] or current_step[0] >= len(solution[0]) - 1:
            return
        current_step[0] += 1
        draw_board(solution[0][current_step[0]])
        info.value = f"Bước: {current_step[0]} / {len(solution[0]) - 1}"
        page.update()

    def prev_click(e):
        if not solution[0] or current_step[0] <= 0:
            return
        current_step[0] -= 1
        draw_board(solution[0][current_step[0]])
        info.value = f"Bước: {current_step[0]} / {len(solution[0]) - 1}"
        page.update()

    solve_btn = ft.ElevatedButton("Giải BFS", on_click=solve_click, width=160, height=40,
                                  style=ft.ButtonStyle(color="white", bgcolor="green"))
    prev_btn = ft.ElevatedButton("Prev", on_click=prev_click, width=100)
    next_btn = ft.ElevatedButton("Next", on_click=next_click, width=100)

    left_column = ft.Column(
        [
            title,
            ft.Container(
                content=ft.Column([
                    ft.Text("Cấu hình phiên bản thuật toán:", weight=ft.FontWeight.BOLD, color="blue300"),
                    bfs_mode_radio
                ]),
                padding=10,
                border=ft.border.all(1, "grey700"),
                border_radius=8,
                margin=ft.margin.only(top=5, bottom=5)
            ),
            ft.Container(content=grid, margin=ft.margin.only(top=5, bottom=5)),
            ft.Row([prev_btn, next_btn], alignment=ft.MainAxisAlignment.CENTER),
            solve_btn,
            info
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=390,
        scroll=ft.ScrollMode.AUTO
    )

    right_column = ft.Column(
        [
            ft.Text("Cột hiển thị thông tin Node - Frontier - Reached", size=18, weight=ft.FontWeight.BOLD,
                    color="orange"),
            path_output
        ],
        expand=True
    )

    main_layout = ft.Row(
        [
            left_column,
            ft.VerticalDivider(width=20, color="grey700"),
            right_column
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    page.add(
        ft.Container(
            padding=20,
            content=main_layout,
            expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
