# ===================================================================
#                 Visualizer BFS/DFS/IDDFS 8PUZZEL - FULL OPTIMIZED
# Link GitHub: https://github.com/NguyenTrungKien1805/8puzzel_visualizer
# ===================================================================

from random import shuffle
import flet as ft
from collections import deque
import copy
import asyncio

# =========================
# START + GOAL
# =========================
START = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
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
    shuffle(directions)
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


def get_move_direction(state_old, state_new):
    """Hàm xác định hướng di chuyển của ô trống từ trạng thái cũ sang mới"""
    r1, c1 = find_zero(state_old)
    r2, c2 = find_zero(state_new)
    dr, dc = r2 - r1, c2 - c1
    if dr == -1 and dc == 0: return "LÊN (UP)"
    if dr == 1 and dc == 0: return "XUỐNG (DOWN)"
    if dr == 0 and dc == -1: return "SANG TRÁI (LEFT)"
    if dr == 0 and dc == 1: return "SANG PHẢI (RIGHT)"
    return ""


# ===================================================
# HÀM 1: CHECK LÚC POP + ADD REACHED LÚC POP
# ===================================================
def bfs_check_on_pop(start, goal):
    queue = deque()
    queue.append((start, [start], 0))

    reached = set()
    bfs_log = "=== HÀM 1: CHECK ĐÍCH LÚC POP + ADD REACHED LÚC POP ===\n\n"
    step_count = 0

    while queue:
        current, path, level = queue.popleft()
        current_tuple = to_tuple(current)

        reached.add(current_tuple)
        step_count += 1

        if current == goal:
            bfs_log += f"\nGOAL FOUND AT STEP {step_count}\n\n"
            return path, bfs_log

        for nxt in next_states(current):
            nxt_tuple = to_tuple(nxt)

            in_frontier = any(to_tuple(item[0]) == nxt_tuple for item in queue)

            if nxt_tuple not in reached and not in_frontier:
                queue.append((nxt, path + [nxt], level + 1))

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
    return None, bfs_log


# ===================================================
# HÀM 2: CHECK LÚC SINH (PUSH) + NHÉT THẲNG VÀO REACHED LUÔN
# ===================================================
def bfs_check_on_push_and_reached(start, goal):
    queue = deque()
    queue.append((start, [start], 0))

    reached = set()
    reached.add(to_tuple(start))

    bfs_log = "=== HÀM 2: CHECK ĐÍCH LÚC SINH (PUSH)===\n\n"
    step_count = 0

    if start == goal:
        bfs_log += "GOAL FOUND AT START STEP\n"
        return [start], bfs_log

    while queue:
        current, path, level = queue.popleft()
        step_count += 1

        for nxt in next_states(current):
            nxt_tuple = to_tuple(nxt)

            if nxt_tuple not in reached:
                reached.add(nxt_tuple)
                new_path = path + [nxt]

                if nxt == goal:
                    bfs_log += f"\nSTEP {step_count}\nNODE".ljust(25) + "FRONTIER".ljust(
                        35) + "REACHED\n" + "=" * 90 + "\n"
                    bfs_log += format_state(current).splitlines()[0].ljust(
                        20) + "FOUND GOAL IN CURRENT PUSH TRÊN FRONTIER!\n"
                    bfs_log += f"\nGOAL FOUND AT STEP {step_count} (LÚC VỪA SINH RA CON ĐÍCH)\n\n"
                    return new_path, bfs_log

                queue.append((nxt, new_path, level + 1))

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
    return None, bfs_log


# ===================================================
# HÀM 3: DFS
# ===================================================
def dfs(start, goal):
    stack = deque()
    stack.append((start, [start], 0))

    reached = set()
    reached.add(to_tuple(start))

    dfs_log = "=== DFS VERSION ===\n\n"
    step_count = 0

    while stack:
        current, path, level = stack.pop()
        step_count += 1

        if current == goal:
            dfs_log += f"\nGOAL FOUND AT STEP {step_count}\n\n"
            return path, dfs_log

        for nxt in next_states(current):
            nxt_tuple = to_tuple(nxt)

            if nxt_tuple not in reached:
                reached.add(nxt_tuple)
                stack.append((nxt, path + [nxt], level + 1))

        node_text = format_state(current)
        frontier_text = "".join(format_state(item[0]) + "\n---\n" for item in stack)
        reached_text = "".join(format_state([list(row) for row in r]) + "\n---\n" for r in reached)

        node_lines = node_text.splitlines()
        frontier_lines = frontier_text.splitlines()
        reached_lines = reached_text.splitlines()

        max_lines = max(len(node_lines), len(frontier_lines), len(reached_lines))
        while len(node_lines) < max_lines: node_lines.append("")
        while len(frontier_lines) < max_lines: frontier_lines.append("")
        while len(reached_lines) < max_lines: reached_lines.append("")

        dfs_log += f"\nSTEP {step_count}\nNODE".ljust(25) + "FRONTIER(STACK)".ljust(35) + "REACHED\n" + "=" * 90 + "\n"
        for i in range(max_lines):
            dfs_log += node_lines[i].ljust(20) + frontier_lines[i].ljust(35) + reached_lines[i] + "\n"

    dfs_log += "\nFAILURE\n"
    return None, dfs_log


# ===================================================
# HÀM 4: IDDFS (Iterative Deepening DFS)
# ===================================================
def iddfs(start, goal):
    log_output = "=== IDDFS VERSION (TỐI ƯU BFS + DFS) ===\n\n"
    step_count = 0
    max_depth_limit = 50

    for depth in range(max_depth_limit):
        log_output += f"--- ĐANG QUÉT Ở ĐỘ SÂU (DEPTH LIMIT): {depth} ---\n"

        stack = deque()
        stack.append((start, [start], 0))

        reached = set()
        reached.add(to_tuple(start))

        while stack:
            current, path, current_depth = stack.pop()
            step_count += 1

            node_text = format_state(current)
            frontier_text = "".join(format_state(item[0]) + f"\n(D:{item[2]})\n---\n" for item in stack)
            reached_text = "".join(format_state([list(row) for row in r]) + "\n---\n" for r in reached)

            node_lines = node_text.splitlines()
            frontier_lines = frontier_text.splitlines()
            reached_lines = reached_text.splitlines()

            max_lines = max(len(node_lines), len(frontier_lines), len(reached_lines))
            while len(node_lines) < max_lines: node_lines.append("")
            while len(frontier_lines) < max_lines: frontier_lines.append("")
            while len(reached_lines) < max_lines: reached_lines.append("")

            log_output += f"\nSTEP {step_count} (Depth: {current_depth})\nNODE".ljust(25) + "FRONTIER(STACK)".ljust(
                35) + "REACHED\n" + "=" * 90 + "\n"
            for i in range(max_lines):
                log_output += node_lines[i].ljust(20) + frontier_lines[i].ljust(35) + reached_lines[i] + "\n"

            if current == goal:
                log_output += f"\n🎉 TÌM THẤY ĐÍCH TẠI ĐỘ SÂU: {current_depth} (TỔNG SỐ BƯỚC DUYỆT: {step_count})\n\n"
                return path, log_output

            if current_depth < depth:
                for nxt in next_states(current):
                    nxt_tuple = to_tuple(nxt)

                    if nxt_tuple not in reached:
                        reached.add(nxt_tuple)
                        stack.append((nxt, path + [nxt], current_depth + 1))

        log_output += f"-> Không tìm thấy ở độ sâu {depth}. Tăng độ sâu lên...\n\n"

    log_output += "\nTHẤT BẠI: Vượt quá giới hạn độ sâu cho phép.\n"
    return None, log_output


# =========================
# MAIN UI APPLICATION
# =========================
def main(page: ft.Page):
    page.title = "8 Puzzle Algorithm Visualizer"
    page.window_width = 1150
    page.window_height = 680
    page.theme_mode = ft.ThemeMode.DARK
    page.window_center()

    solution = [[]]
    current_step = [0]
    is_playing = [False]

    # --- KHỐI BÊN TRÁI ---
    info = ft.Text("Chọn hàm thuật toán và bấm 'Giải 8 - Puzzle'.", size=14, italic=True)
    grid = ft.Column(spacing=6, alignment=ft.MainAxisAlignment.CENTER)

    mode_dropdown = ft.Dropdown(
        value="pop",  # Giá trị mặc định ban đầu
        options=[
            ft.dropdown.Option("pop", "Hàm 1: Check khi POP + Add Reached khi POP"),
            ft.dropdown.Option("push", "Hàm 2: Check khi SINH + Add Reached NGAY"),
            ft.dropdown.Option("dfs", "Hàm 3: DFS"),
            ft.dropdown.Option("iddfs", "Hàm 4: ITERATIVE-DFS"),
        ],
        width=360,
    )

    steps_path_view = ft.TextField(
        label="Bước hiện tại",
        read_only=True,
        value="0 / 0",
        text_align=ft.TextAlign.CENTER,
        text_style=ft.TextStyle(font_family="monospace", size=18, weight=ft.FontWeight.BOLD, color="greenyellow")
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

    def update_path_display():
        """Hàm cập nhật text trong ô Path ngắn gọn dạng: Hiện tại / Tổng số bước"""
        if not solution[0]:
            steps_path_view.value = "0 / 0"
            return
        steps_path_view.value = f"{current_step[0]} / {len(solution[0]) - 1}"

    draw_board(START)

    # --- KHỐI BÊN PHẢI ---
    path_output = ft.TextField(
        label="Nhật ký cấu trúc dữ liệu (Logs)",
        multiline=True,
        min_lines=15,
        max_lines=15,
        read_only=True,
        value="Nhật ký chạy của hàm được chọn sẽ hiển thị trực quan tại đây...",
        text_style=ft.TextStyle(font_family="monospace", size=12),
    )

    visual_path_output = ft.TextField(
        label="Chi tiết ma trận đường đi & Hướng dịch chuyển ô trống",
        multiline=True,
        min_lines=15,
        max_lines=15,
        read_only=True,
        value="Sau khi giải xong, danh sách các ma trận dịch chuyển từ Trạng thái đầu -> Trạng thái đích kèm hướng đi qua Trái/Phải/Lên/Xuống của ô trống sẽ hiển thị chi tiết tại đây...",
        text_style=ft.TextStyle(font_family="monospace", size=12, color="orange"),
    )

    def generate_visual_path_text(path):
        if not path: return "Không tìm thấy đường đi."

        text = f"* TRẠNG THÁI BAN ĐẦU:\n{format_state(path[0])}\n"
        text += "=" * 25 + "\n"

        for i in range(1, len(path)):
            direction = get_move_direction(path[i - 1], path[i])
            text += f"* Bước {i} (Ô trống dịch chuyển {direction}):\n"
            text += f"{format_state(path[i])}\n"
            if i == len(path) - 1:
                text += "=" * 25 + "\n🎉 VỀ ĐÍCH THÀNH CÔNG! 🎉"
            else:
                text += "=" * 25 + "\n"
        return text

    def solve_click(e):
        is_playing[0] = False
        play_btn.text = "Play"
        play_btn.bgcolor = "orange"

        info.value = "Đang chạy thuật toán... Xin chờ!"
        path_output.value = "Hệ thống đang thực thi cấu trúc dữ liệu..."
        visual_path_output.value = "Đang dựng sơ đồ ma trận đường đi..."
        page.update()

        if mode_dropdown.value == "pop":
            path, bfs_log = bfs_check_on_pop(START, GOAL)
        elif mode_dropdown.value == "push":
            path, bfs_log = bfs_check_on_push_and_reached(START, GOAL)
        elif mode_dropdown.value == "dfs":
            path, bfs_log = dfs(START, GOAL)
        else:
            path, bfs_log = iddfs(START, GOAL)

        path_output.value = bfs_log

        if path:
            solution[0] = path
            current_step[0] = 0
            draw_board(path[0])
            info.value = f"Hoàn thành! Số bước đường đi: {len(path) - 1} bước."
            update_path_display()
            visual_path_output.value = generate_visual_path_text(path)
        else:
            info.value = "Không tìm thấy lời giải!"
            visual_path_output.value = "Không có đường đi."
        page.update()

    def next_click(e):
        if not solution[0] or current_step[0] >= len(solution[0]) - 1:
            return
        current_step[0] += 1
        draw_board(solution[0][current_step[0]])
        info.value = f"Bước: {current_step[0]} / {len(solution[0]) - 1}"
        update_path_display()
        page.update()

    def prev_click(e):
        if not solution[0] or current_step[0] <= 0:
            return
        current_step[0] -= 1
        draw_board(solution[0][current_step[0]])
        info.value = f"Bước: {current_step[0]} / {len(solution[0]) - 1}"
        update_path_display()
        page.update()

    async def play_click(e):
        if not solution[0]:
            info.value = "Vui lòng bấm nút Giải trước khi bấm chạy tự động!"
            page.update()
            return

        is_playing[0] = not is_playing[0]

        if is_playing[0]:
            play_btn.text = "Pause"
            play_btn.bgcolor = "red"
            page.update()

            while is_playing[0] and current_step[0] < len(solution[0]) - 1:
                current_step[0] += 1
                draw_board(solution[0][current_step[0]])
                info.value = f"Bước: {current_step[0]} / {len(solution[0]) - 1} (Đang chạy tự động...)"
                update_path_display()
                page.update()
                await asyncio.sleep(0.5)

            if current_step[0] == len(solution[0]) - 1:
                is_playing[0] = False
                play_btn.text = "Play"
                play_btn.bgcolor = "orange"
                info.value = f"Đã kết thúc chuỗi! Bước: {current_step[0]} / {len(solution[0]) - 1}"
                page.update()
        else:
            play_btn.text = "Play"
            play_btn.bgcolor = "orange"
            info.value = f"Đã tạm dừng ở bước: {current_step[0]} / {len(solution[0]) - 1}"
            page.update()

    solve_btn = ft.ElevatedButton("Giải 8 - Puzzle", on_click=solve_click, width=160, height=40,
                                  style=ft.ButtonStyle(color="white", bgcolor="green"))
    prev_btn = ft.ElevatedButton("Prev", on_click=prev_click, width=100)
    next_btn = ft.ElevatedButton("Next", on_click=next_click, width=100)
    play_btn = ft.ElevatedButton("Play", on_click=play_click, width=100,
                                 style=ft.ButtonStyle(color="white", bgcolor="orange"))

    left_column = ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    ft.Text("Cấu hình phiên bản thuật toán:", weight=ft.FontWeight.BOLD, color="blue300"),
                    mode_dropdown
                ]),
                padding=10,
                border=ft.border.all(1, "grey700"),
                border_radius=8,
                margin=ft.margin.only(top=5, bottom=5)
            ),
            ft.Container(content=grid, margin=ft.margin.only(top=5, bottom=5)),
            ft.Container(content=steps_path_view, margin=ft.margin.only(top=5, bottom=5)),  # Ô đếm bước phân số nằm đây
            ft.Row([prev_btn, play_btn, next_btn], alignment=ft.MainAxisAlignment.CENTER),
            solve_btn,
            info
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=390,
        scroll=ft.ScrollMode.AUTO
    )

    right_column = ft.Column(
        [
            ft.Text("Thông tin thực thi và Kết quả phân tích đường đi", size=18, weight=ft.FontWeight.BOLD,
                    color="orange"),
            path_output,
            visual_path_output
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
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
