# ===================================================================
#                 Visualizer BFS/DFS/IDDFS/A* 8PUZZEL
# ===================================================================

from random import shuffle
import flet as ft
from collections import deque
import heapq
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

def find_goal_pos(val):
    for r in range(3):
        for c in range(3):
            if GOAL[r][c] == val:
                return r, c
    return -1, -1

def calculate_manhattan(board):
    """Tính khoảng cách Manhattan dựa trên ma trận GOAL toàn cục"""
    total_h = 0
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            if val != 0:  # Bỏ qua ô trống (số 0)
                goal_r, goal_c = find_goal_pos(val)
                total_h += abs(r - goal_r) + abs(c - goal_c)
    return total_h

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
    log_output = "=== IDDFS SEARCH LOG (TỐI ƯU GIAO DIỆN) ===\n"
    step_count = 0
    max_depth_limit = 50

    for depth in range(max_depth_limit):
        log_output += f"\n============================================================\n"
        log_output += f" ĐANG QUÉT Ở ĐỘ SÂU GIỚI HẠN (DEPTH LIMIT): {depth}\n"
        log_output += f"============================================================\n"

        # Stack lưu tuple dạng: (current_board, path, current_depth)
        stack = deque()
        stack.append((start, [start], 0))

        # Tập reached lưu các trạng thái ĐÃ POP RA XÉT ở lượt quét này
        reached = set()

        while stack:
            # 1. LẤY NODE RA KHỎI STACK ĐỂ XÉT (LIFO)
            current, path, current_depth = stack.pop()
            current_tuple = to_tuple(current)

            # Cơ chế chống lặp khi POP (Tránh xét lại cùng 1 độ sâu hoặc sâu hơn)
            if current_tuple in reached:
                continue

            step_count += 1
            # Thêm vào reached ngay khi lấy ra xét
            reached.add(current_tuple)

            # 2. IN NODE HIỆN TẠI LÊN ĐẦU STEP
            log_output += f"\n{'-' * 60}\n"
            log_output += f" STEP {step_count} | NODE HIỆN TẠI (Độ sâu nút: {current_depth} / Giới hạn: {depth})\n"
            log_output += f"{'-' * 60}\n"
            log_output += format_state(current) + "\n"
            log_output += f"{'-' * 60}\n"

            # Kiểm tra điều kiện Đích ngay khi POP
            if current == goal:
                log_output += f"\n🎉 TÌM THẤY ĐÍCH TẠI ĐỘ SÂU: {current_depth}!\n"
                log_output += f"- Tổng số lượt xét qua các tầng: {step_count}\n"
                log_output += f"- Số bước đi tối ưu: {len(path) - 1}\n\n"
                return path, log_output

            # 3. SINH CÁC TRẠNG THÁI CON (Nếu chưa vượt quá giới hạn độ sâu hiện tại)
            generated_children = []
            if current_depth < depth:
                # Với DFS/IDDFS, nếu muốn thứ tự duyệt nhánh giống như code cũ,
                # ta giữ nguyên hướng sinh con bình thường
                for nxt in next_states(current):
                    nxt_tuple = to_tuple(nxt)

                    if nxt_tuple not in reached:
                        stack.append((nxt, path + [nxt], current_depth + 1))

                        # Lưu log chuỗi 1 dòng cho node con
                        nxt_str = " ".join(" ".join(str(cell) for cell in row) for row in nxt)
                        generated_children.append(f"   + Sinh ra: [{nxt_str}] -> Depth: {current_depth + 1}")

            # In danh sách trạng thái con vừa sinh
            log_output += " CÁC TRẠNG THÁI CON VỪA SINH RA ĐƯỢC ĐẨY VÀO STACK:\n"
            if not generated_children:
                if current_depth >= depth:
                    log_output += "   (Không sinh thêm vì ĐÃ ĐẠT GIỚI HẠN ĐỘ SÂU của tầng này)\n"
                else:
                    log_output += "   (Không có node con nào hợp lệ / Tất cả đã nằm trong Reached)\n"
            else:
                for child in generated_children:
                    log_output += child + "\n"
            log_output += f"{'-' * 60}\n"

            # 4. ĐỊNH DẠNG FRONTIER (STACK - LIFO)
            log_output += " FRONTIER STACK (Các trạng thái chờ duyệt - Cuối Stack sẽ ra trước):\n"
            if not stack:
                log_output += "   (Trống)\n"
            else:
                # In từ cuối danh sách lên đầu để thể hiện đúng tính chất LIFO của Stack
                for item in reversed(stack):
                    st_board, _, st_depth = item
                    st_str = " ".join(" ".join(str(cell) for cell in row) for row in st_board)
                    log_output += f"   > [{st_str}] -> Depth: {st_depth}\n"
            log_output += f"{'-' * 60}\n"

            # 5. ĐỊNH DẠNG REACHED
            log_output += " REACHED (Các trạng thái đã POP ra xét ở tầng này):\n"
            for r_tuple in reached:
                r_str = " ".join(" ".join(str(cell) for cell in row) for row in r_tuple)
                log_output += f"   > [{r_str}]\n"
            log_output += f"{'=' * 60}\n"

        log_output += f"-> Không tìm thấy ở độ sâu {depth}. Tăng độ sâu lên...\n"

    log_output += "\nTHẤT BẠI: Vượt quá giới hạn độ sâu cho phép.\n"
    return None, log_output


# ===================================================
# HÀM 5: UCS
# ===================================================
def count_misplaced_tiles(current, goal):
    """Hàm đếm số ô sai vị trí so với trạng thái đích (không tính ô trống 0)"""
    count = 0
    for r in range(len(current)):
        for c in range(len(current[0])):
            if current[r][c] != 0 and current[r][c] != goal[r][c]:
                count += 1
    return count


def ucs(start, goal):
    log_output = "=== UCS SEARCH LOG (g = tổng số ô sai cộng dồn) ===\n"
    step_count = 0

    # Chi phí ban đầu tại nút gốc bằng số ô sai của chính nó
    g_start = count_misplaced_tiles(start, goal)

    frontier_heap = []
    # Heap: (g_cost_tich_luy, current_board, path)
    heapq.heappush(frontier_heap, (g_start, start, [start]))

    # Tập chứa các trạng thái đã POP ra xét kèm g_cost tối ưu nhất
    reached = {}

    while frontier_heap:
        # 1. LẤY NODE CÓ G_COST CỘNG DỒN NHỎ NHẤT RA ĐỂ XÉT
        g, current, path = heapq.heappop(frontier_heap)
        current_tuple = to_tuple(current)

        # Nếu node này trùng và có chi phí g_cost tích lũy tệ hơn thì bỏ qua
        if current_tuple in reached and reached[current_tuple] <= g:
            continue

        step_count += 1

        # CẬP NHẬT VÀO REACHED (Node này chính thức được chốt chi phí)
        reached[current_tuple] = g

        # 2. IN NODE HIỆN TẠI LÊN ĐẦU STEP
        log_output += f"\n{'=' * 60}\n"
        log_output += f" STEP {step_count} | NODE HIỆN TẠI (g_cost tích lũy: {g})\n"
        log_output += f"{'=' * 60}\n"
        log_output += format_state(current) + "\n"
        log_output += f"{'-' * 60}\n"

        # Kiểm tra điều kiện Đích ngay khi POP theo chuẩn UCS
        if current == goal:
            log_output += f"\n🎉 TÌM THẤY ĐÍCH!\n- Tổng số lượt xét: {step_count}\n- Tổng g_cost tích lũy tối ưu: {g}\n\n"
            return path, log_output

        # 3. SINH CÁC TRẠNG THÁI CON (CỘNG DỒN TỪ CHA)
        generated_children = []
        for nxt in next_states(current):
            nxt_tuple = to_tuple(nxt)

            # Tính số ô sai của riêng nút con này
            nxt_misplaced = count_misplaced_tiles(nxt, goal)

            # LOGIC CỦA BẠN: g_cost của con = g_cost của cha + số ô sai của con
            next_g = g + nxt_misplaced

            if nxt_tuple not in reached or next_g < reached[nxt_tuple]:
                heapq.heappush(frontier_heap, (next_g, nxt, path + [nxt]))

                nxt_str = " ".join(" ".join(str(cell) for cell in row) for row in nxt)
                generated_children.append(
                    f"   + Sinh ra: [{nxt_str}] -> Ô sai hiện tại: {nxt_misplaced} | g tích lũy (cha+con): {next_g}"
                )

        # In danh sách các node con vừa mới sinh ra ở bước này
        log_output += " CÁC TRẠNG THÁI CON VỪA SINH RA ĐƯỢC THÊM VÀO FRONTIER:\n"
        if not generated_children:
            log_output += "   (Không có node con nào hợp lệ hoặc tất cả đã nằm trong Reached với g tốt hơn)\n"
        else:
            for child in generated_children:
                log_output += child + "\n"
        log_output += f"{'-' * 60}\n"

        # 4. ĐỊNH DẠNG FRONTIER
        log_output += " FRONTIER HIỆN TẠI (Sắp xếp theo g tích lũy tăng dần):\n"

        sorted_frontier = sorted(list(frontier_heap), key=lambda x: x[0])
        if not sorted_frontier:
            log_output += "   (Trống)\n"
        else:
            for item in sorted_frontier:
                g_item, board_item, _ = item
                f_str = " ".join(" ".join(str(cell) for cell in row) for row in board_item)
                log_output += f"   > [{f_str}] -> g tích lũy: {g_item}\n"

        log_output += f"{'-' * 60}\n"

        # 5. ĐỊNH DẠNG REACHED
        log_output += " REACHED (Các trạng thái đã duyệt):\n"
        for r_tuple, g_cost in reached.items():
            r_str = " ".join(" ".join(str(cell) for cell in row) for row in r_tuple)
            log_output += f"   > [{r_str}] -> g tích lũy tốt nhất: {g_cost}\n"
        log_output += f"{'=' * 60}\n"

    log_output += "\nTHẤT BẠI: Không tìm được đường đi đến đích.\n"
    return None, log_output

# ===================================================
# HÀM 6: Greedy
# ===================================================
def greedy(start, goal):
    log_output = "=== GREEDY SEARCH LOG ===\n"

    step_count = 0
    counter = 0

    # =========================================================
    # FRONTIER = Heap ưu tiên node có h nhỏ nhất
    # Item trong heap:
    # (h_cost, counter, current_board, path)
    # =========================================================
    frontier_heap = []

    # Set dùng để tránh node bị thêm trùng vào frontier
    frontier_set = set()

    # Reached = các trạng thái đã được POP ra xét
    reached = set()

    # =========================================================
    # PUSH NODE START
    # =========================================================
    h_start = calculate_manhattan(start)

    heapq.heappush(
        frontier_heap,
        (h_start, counter, start, [start])
    )

    frontier_set.add(to_tuple(start))

    # =========================================================
    # MAIN LOOP
    # =========================================================
    while frontier_heap:

        # -----------------------------------------------------
        # LẤY NODE CÓ h NHỎ NHẤT
        # -----------------------------------------------------
        h, _, current, path = heapq.heappop(frontier_heap)

        current_tuple = to_tuple(current)

        # Xóa khỏi frontier_set vì đã bị pop
        frontier_set.remove(current_tuple)

        # Nếu đã duyệt rồi thì bỏ qua
        if current_tuple in reached:
            continue

        # Đánh dấu đã duyệt
        reached.add(current_tuple)

        step_count += 1
        g = len(path) - 1

        # =====================================================
        # LOG NODE HIỆN TẠI
        # =====================================================
        log_output += f"\n{'=' * 60}\n"
        log_output += f" STEP {step_count} | NODE HIỆN TẠI (Step: {g}, h: {h})\n"
        log_output += f"{'=' * 60}\n"

        log_output += format_state(current) + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # CHECK GOAL
        # =====================================================
        if current == goal:

            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"
            log_output += f"- Tổng số lượt xét: {step_count}\n"
            log_output += f"- Số bước đi tìm được: {g}\n"

            return path, log_output

        # =====================================================
        # SINH NODE CON
        # =====================================================
        generated_children = []

        for nxt in next_states(current):

            nxt_tuple = to_tuple(nxt)

            # -------------------------------------------------
            # Chỉ thêm nếu:
            # - chưa nằm trong reached
            # - chưa nằm trong frontier
            # -------------------------------------------------
            if (
                nxt_tuple not in reached
                and nxt_tuple not in frontier_set
            ):

                next_h = calculate_manhattan(nxt)
                next_g = g + 1

                counter += 1

                heapq.heappush(
                    frontier_heap,
                    (
                        next_h,
                        counter,
                        nxt,
                        path + [nxt]
                    )
                )

                frontier_set.add(nxt_tuple)

                nxt_str = " ".join(
                    " ".join(str(cell) for cell in row)
                    for row in nxt
                )

                generated_children.append(
                    f"   + Sinh ra: [{nxt_str}] -> Step: {next_g}, h: {next_h}"
                )

        # =====================================================
        # LOG NODE CON
        # =====================================================
        log_output += " CÁC TRẠNG THÁI CON VỪA SINH RA:\n"

        if not generated_children:
            log_output += "   (Không có node hợp lệ)\n"
        else:
            for child in generated_children:
                log_output += child + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG FRONTIER
        # =====================================================
        log_output += " FRONTIER HIỆN TẠI:\n"

        sorted_frontier = sorted(frontier_heap, key=lambda x: x[0])

        if not sorted_frontier:
            log_output += "   (Trống)\n"

        else:
            for item in sorted_frontier:

                h_item, _, board_item, path_item = item

                g_item = len(path_item) - 1

                board_str = " ".join(
                    " ".join(str(cell) for cell in row)
                    for row in board_item
                )

                log_output += (
                    f"   > [{board_str}] "
                    f"-> Step: {g_item}, h: {h_item}\n"
                )

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG REACHED
        # =====================================================
        log_output += " REACHED:\n"

        for r in reached:

            r_str = " ".join(
                " ".join(str(cell) for cell in row)
                for row in r
            )

            log_output += f"   > [{r_str}]\n"

        log_output += f"{'=' * 60}\n"

    # =========================================================
    # KHÔNG TÌM THẤY
    # =========================================================
    log_output += "\n❌ THẤT BẠI: Không tìm được đường đi.\n"

    return None, log_output

# ===================================================
# HÀM 7: A*
# ===================================================
def a_star(start, goal):

    log_output = "=== A* SEARCH LOG ===\n"

    step_count = 0
    counter = 0

    # =========================================================
    # FRONTIER = Priority Queue
    # Item:
    # (f, counter, g, h, board, path)
    # =========================================================
    frontier_heap = []

    frontier_set = set()

    # =========================================================
    # COST SO FAR
    # Lưu g nhỏ nhất của mỗi trạng thái
    # =========================================================
    cost_so_far = {}

    # =========================================================
    # START NODE
    # =========================================================
    start_h = calculate_manhattan(start)
    start_g = 0
    start_f = start_g + start_h

    heapq.heappush(
        frontier_heap,
        (
            start_f,
            counter,
            start_g,
            start_h,
            start,
            [start]
        )
    )

    frontier_set.add(to_tuple(start))

    cost_so_far[to_tuple(start)] = 0

    # =========================================================
    # MAIN LOOP
    # =========================================================
    while frontier_heap:

        # -----------------------------------------------------
        # POP NODE CÓ f NHỎ NHẤT
        # -----------------------------------------------------
        (
            f,
            _,
            g,
            h,
            current,
            path
        ) = heapq.heappop(frontier_heap)

        current_tuple = to_tuple(current)

        if current_tuple in frontier_set:
            frontier_set.remove(current_tuple)

        step_count += 1

        # =====================================================
        # LOG NODE HIỆN TẠI
        # =====================================================
        log_output += f"\n{'=' * 60}\n"

        log_output += (
            f" STEP {step_count} | "
            f"(g: {g}, h: {h}, f: {f})\n"
        )

        log_output += f"{'=' * 60}\n"

        log_output += format_state(current) + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # CHECK GOAL
        # =====================================================
        if current == goal:

            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"

            log_output += (
                f"- Tổng số lượt xét: {step_count}\n"
            )

            log_output += (
                f"- Số bước đi tìm được: {g}\n"
            )

            return path, log_output

        # =====================================================
        # SINH NODE CON
        # =====================================================
        generated_children = []

        children = next_states(current)

        # Sort theo f nhỏ trước cho đẹp log
        children.sort(
            key=lambda x:
            (g + 1) + calculate_manhattan(x)
        )

        for nxt in children:

            nxt_tuple = to_tuple(nxt)

            next_g = g + 1
            next_h = calculate_manhattan(nxt)
            next_f = next_g + next_h

            # -------------------------------------------------
            # Nếu tìm được đường đi tốt hơn
            # -------------------------------------------------
            if (
                nxt_tuple not in cost_so_far
                or next_g < cost_so_far[nxt_tuple]
            ):

                cost_so_far[nxt_tuple] = next_g

                counter += 1

                heapq.heappush(
                    frontier_heap,
                    (
                        next_f,
                        counter,
                        next_g,
                        next_h,
                        nxt,
                        path + [nxt]
                    )
                )

                frontier_set.add(nxt_tuple)

                nxt_str = " ".join(
                    " ".join(str(cell) for cell in row)
                    for row in nxt
                )

                generated_children.append(
                    f"   + Sinh ra: [{nxt_str}] "
                    f"-> g: {next_g}, "
                    f"h: {next_h}, "
                    f"f: {next_f}"
                )

        # =====================================================
        # LOG NODE CON
        # =====================================================
        log_output += " CÁC NODE CON:\n"

        if not generated_children:

            log_output += (
                "   (Không có node hợp lệ)\n"
            )

        else:
            for child in generated_children:
                log_output += child + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG FRONTIER
        # =====================================================
        log_output += " FRONTIER HIỆN TẠI:\n"

        sorted_frontier = sorted(
            frontier_heap,
            key=lambda x: x[0]
        )

        if not sorted_frontier:

            log_output += "   (Trống)\n"

        else:

            for item in sorted_frontier:

                (
                    f_item,
                    _,
                    g_item,
                    h_item,
                    board_item,
                    _
                ) = item

                board_str = " ".join(
                    " ".join(str(cell) for cell in row)
                    for row in board_item
                )

                log_output += (
                    f"   > [{board_str}] "
                    f"-> g: {g_item}, "
                    f"h: {h_item}, "
                    f"f: {f_item}\n"
                )

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG COST SO FAR
        # =====================================================
        log_output += " COST SO FAR:\n"

        for state, cost in cost_so_far.items():

            state_str = " ".join(
                " ".join(str(cell) for cell in row)
                for row in state
            )

            log_output += (
                f"   > [{state_str}] "
                f"-> g nhỏ nhất = {cost}\n"
            )

        log_output += f"{'=' * 60}\n"

    # =========================================================
    # KHÔNG TÌM THẤY
    # =========================================================
    log_output += (
        "\n❌ THẤT BẠI: "
        "Không tìm được đường đi.\n"
    )

    return None, log_output

# ===================================================
# HÀM 8: IDA*
# ===================================================
def ida_star(start, goal):

    log_output = "=== IDA* SEARCH LOG ===\n"

    step_count = 0

    # =========================================================
    # THRESHOLD BAN ĐẦU = heuristic(start)
    # =========================================================
    threshold = calculate_manhattan(start)

    log_output += (
        f"Ngưỡng ban đầu (threshold): {threshold}\n"
    )

    # =========================================================
    # DFS GIỚI HẠN THEO f = g + h
    # =========================================================
    def search(path, g, threshold, reached):

        nonlocal step_count
        nonlocal log_output

        current = path[-1]

        # -----------------------------------------------------
        # TÍNH h VÀ f
        # -----------------------------------------------------
        h = calculate_manhattan(current)
        f = g + h

        # -----------------------------------------------------
        # PRUNING / CUT-OFF
        # -----------------------------------------------------
        if f > threshold:

            log_output += (
                f"\n[CUT-OFF] "
                f"f = {f} vượt threshold = {threshold}\n"
            )

            return f

        step_count += 1

        # =====================================================
        # LOG NODE HIỆN TẠI
        # =====================================================
        log_output += f"\n{'=' * 60}\n"

        log_output += (
            f" STEP {step_count} | "
            f"(g: {g}, h: {h}, f: {f}, threshold: {threshold})\n"
        )

        log_output += f"{'=' * 60}\n"

        log_output += format_state(current) + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # CHECK GOAL
        # =====================================================
        if current == goal:

            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"

            log_output += (
                f"- Tổng số lượt xét: {step_count}\n"
            )

            log_output += (
                f"- Số bước đi tìm được: {g}\n"
            )

            return path

        # =====================================================
        # SINH NODE CON
        # =====================================================
        children = []

        for nxt in next_states(current):

            nxt_tuple = to_tuple(nxt)

            # Tránh lặp trong đường đi hiện tại
            if nxt_tuple not in reached:
                children.append(nxt)

        # =====================================================
        # SORT THEO h NHỎ NHẤT
        # =====================================================
        children.sort(key=calculate_manhattan)

        # =====================================================
        # LOG NODE CON
        # =====================================================
        generated_children = []

        for nxt in children:

            next_g = g + 1
            next_h = calculate_manhattan(nxt)
            next_f = next_g + next_h

            nxt_str = " ".join(
                " ".join(str(cell) for cell in row)
                for row in nxt
            )

            generated_children.append(
                f"   + Sinh ra: [{nxt_str}] "
                f"-> g: {next_g}, h: {next_h}, f: {next_f}"
            )

        log_output += " CÁC NODE CON:\n"

        if not generated_children:
            log_output += (
                "   (Không có node con hợp lệ)\n"
            )

        else:
            for child in generated_children:
                log_output += child + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # DFS TIẾP
        # =====================================================
        min_threshold = float("inf")

        for nxt in children:

            nxt_tuple = to_tuple(nxt)

            reached.add(nxt_tuple)

            result = search(
                path + [nxt],
                g + 1,
                threshold,
                reached
            )

            # -------------------------------------------------
            # TÌM THẤY ĐƯỜNG ĐI
            # -------------------------------------------------
            if isinstance(result, list):
                return result

            # -------------------------------------------------
            # CẬP NHẬT threshold NHỎ NHẤT BỊ VƯỢT
            # -------------------------------------------------
            if result < min_threshold:
                min_threshold = result

            # BACKTRACK
            reached.remove(nxt_tuple)

        return min_threshold

    # =========================================================
    # VÒNG LẶP TĂNG THRESHOLD
    # =========================================================
    while True:

        log_output += f"\n\n{'#' * 60}\n"

        log_output += (
            f" BẮT ĐẦU DFS VỚI THRESHOLD = {threshold}\n"
        )

        log_output += f"{'#' * 60}\n"

        reached = set()
        reached.add(to_tuple(start))

        result = search(
            [start],
            0,
            threshold,
            reached
        )

        # =====================================================
        # TÌM THẤY LỜI GIẢI
        # =====================================================
        if isinstance(result, list):
            return result, log_output

        # =====================================================
        # KHÔNG CÒN NODE ĐỂ MỞ RỘNG
        # =====================================================
        if result == float("inf"):

            log_output += (
                "\n❌ THẤT BẠI: "
                "Không tìm được đường đi đến đích.\n"
            )

            return None, log_output

        # =====================================================
        # TĂNG THRESHOLD
        # =====================================================
        log_output += (
            f"\n>>> TĂNG THRESHOLD: "
            f"{threshold} -> {result}\n"
        )

        threshold = result

def search_dfs(path, g, threshold):
    global log_output, step_count

    current = path[-1]
    h = calculate_manhattan(current)
    f = g + h
    current_tuple = to_tuple(current)

    step_count += 1

    # 1 & 2. IN NODE HIỆN TẠI LÊN ĐẦU STEP (Y hệt form Greedy)
    log_output += f"\n{'=' * 60}\n"
    log_output += f" STEP {step_count} | NODE HIỆN TẠI (Step/g: {g}, h: {h} -> f/Cost: {f} | Threshold: {threshold})\n"
    log_output += f"{'=' * 60}\n"
    log_output += format_state(current) + "\n"
    log_output += f"{'-' * 60}\n"

    # Kiểm tra điều kiện chặn Threshold
    if f > threshold:
        log_output += f"   (Node này bị CHẶN vì f = {f} > Threshold = {threshold})\n"
        log_output += f"{'-' * 60}\n"
        return f, None

    # Kiểm tra điều kiện Đích ngay khi POP
    if current == GOAL:
        return f, path

    min_val = float('inf')

    # Tạo danh sách mô phỏng Frontier cục bộ cho bước này và log sinh con
    generated_children = []
    simulated_frontier = []

    # 3. SINH CÁC TRẠNG THÁI CON
    for nxt in next_states(current):
        # Tránh trùng lặp ngược lại các node cha đang nằm trên cây đường đi hiện tại (Reached)
        if nxt not in path:
            next_g = g + 1
            next_h = calculate_manhattan(nxt)
            next_f = next_g + next_h

            nxt_str = " ".join(" ".join(str(cell) for cell in row) for row in nxt)
            generated_children.append(f"   + Sinh ra: [{nxt_str}] -> Step: {next_g}, h: {next_h} -> f/Cost: {next_f}")

            # Nếu thỏa mãn hạn mức thì đưa vào danh sách chờ đi tiếp (Frontier của nhánh)
            if next_f <= threshold:
                simulated_frontier.append((next_f, next_g, next_h, nxt))

    # In danh sách các node con vừa mới sinh ra ở bước này
    log_output += " CÁC TRẠNG THÁI CON VỪA SINH RA:\n"
    if not generated_children:
        log_output += "   (Không có node con nào hợp lệ hoặc tất cả tạo thành chu trình trùng lặp)\n"
    else:
        for child in generated_children:
            log_output += child + "\n"
    log_output += f"{'-' * 60}\n"

    # 4. ĐỊNH DẠNG FRONTIER HIỆN TẠI (Các node con hợp lệ sắp được chọn đi sâu xuống)
    log_output += " FRONTIER NHÁNH HIỆN TẠI (Các node con <= Threshold, xếp theo f nhỏ nhất):\n"

    # Sắp xếp các node con hợp lệ theo f_cost tăng dần để ưu tiên nhánh tốt trước
    sorted_frontier = sorted(simulated_frontier, key=lambda x: x[0])

    if not sorted_frontier:
        log_output += "   (Trống hoặc tất cả các con đều vượt ngưỡng Threshold)\n"
    else:
        for item in sorted_frontier:
            f_item, g_item, h_item, board_item = item
            f_str = " ".join(" ".join(str(cell) for cell in row) for row in board_item)
            log_output += f"   > [{f_str}] -> Step: {g_item}, h: {h_item} -> f/Cost: {f_item}\n"
    log_output += f"{'-' * 60}\n"

    # 5. ĐỊNH DẠNG REACHED (Chính là vết đường đi từ gốc đến nút cha hiện tại)
    log_output += " REACHED (Chuỗi lộ trình cây DFS đang đi tính đến bước này):\n"
    for node in path:
        r_str = " ".join(" ".join(str(cell) for cell in row) for row in to_tuple(node))
        log_output += f"   > [{r_str}]\n"
    log_output += f"{'=' * 60}\n"

    # TIẾN HÀNH DUYỆT ĐỆ QUY XUỐNG CÁC CON THEO THỨ TỰ ƯU TIÊN
    for item in sorted_frontier:
        _, next_g, _, nxt = item

        path.append(nxt)
        distance, result_path = search_dfs(path, next_g, threshold)

        if result_path is not None:
            return distance, result_path

        if distance < min_val:
            min_val = distance

        path.pop()  # Quay lui (Backtrack)

    return min_val, None

# ===================================================
# HÀM 9: CLIMING HILL - SIMPLE
# ===================================================
def simple_hill_climbing(start, goal):
    log_output = "=== SIMPLE HILL CLIMBING SEARCH LOG ===\n"

    step_count = 0

    # Trạng thái hiện tại và đường đi đến trạng thái đó
    current_board = start
    current_path = [start]

    # Reached = tập các trạng thái đã từng đi qua (tránh lặp vòng vô hạn nếu đồ thị có chu trình)
    reached = set()
    reached.add(to_tuple(start))

    # =========================================================
    # MAIN LOOP
    # =========================================================
    while True:
        step_count += 1
        current_tuple = to_tuple(current_board)

        # Tính h của node hiện tại
        h_current = calculate_manhattan(current_board)
        g = len(current_path) - 1

        # =====================================================
        # LOG NODE HIỆN TẠI
        # =====================================================
        log_output += f"\n{'=' * 60}\n"
        log_output += f" STEP {step_count} | NODE HIỆN TẠI (Step: {g}, h: {h_current})\n"
        log_output += f"{'=' * 60}\n"

        log_output += format_state(current_board) + "\n"
        log_output += f"{'-' * 60}\n"

        # =====================================================
        # CHECK GOAL
        # =====================================================
        if current_board == goal:
            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"
            log_output += f"- Tổng số lượt xét: {step_count}\n"
            log_output += f"- Số bước đi tìm được: {g}\n"
            return current_path, log_output

        # =====================================================
        # SINH NODE CON VÀ CHỌN BƯỚC ĐI TIẾP THEO
        # =====================================================
        generated_children = []
        next_board = None  # Lưu trạng thái tiếp theo được chọn

        # Duyệt qua từng trạng thái kế tiếp
        for nxt in next_states(current_board):
            nxt_tuple = to_tuple(nxt)

            # Bỏ qua nếu trạng thái này đã từng đi qua
            if nxt_tuple in reached:
                continue

            next_h = calculate_manhattan(nxt)
            next_g = g + 1

            nxt_str = " ".join(" ".join(str(cell) for cell in row) for row in nxt)
            generated_children.append(f"   + Sinh ra: [{nxt_str}] -> Step: {next_g}, h: {next_h}")

            # CHIẾN LƯỢC SIMPLE HILL CLIMBING:
            # Chọn NGAY node đầu tiên tốt hơn node hiện tại (h nhỏ hơn h_current)
            if next_board is None and next_h < h_current:
                next_board = nxt
                next_path = current_path + [nxt]
                # Log đánh dấu node này được chọn làm bước đi tiếp theo
                generated_children[-1] += " <--- CHỌN (Tốt hơn node hiện tại)"

        # =====================================================
        # LOG NODE CON
        # =====================================================
        log_output += " CÁC TRẠNG THÁI CON VỪA SINH RA:\n"
        if not generated_children:
            log_output += "   (Không có node hợp lệ)\n"
        else:
            for child in generated_children:
                log_output += child + "\n"
        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG FRONTIER (Hill Climbing không dùng Frontier như Greedy)
        # =====================================================
        log_output += " FRONTIER HIỆN TẠI:\n"
        if next_board is None:
            log_output += "   (Trống - Không tìm thấy bước đi tốt hơn)\n"
        else:
            # Biểu diễn node duy nhất được giữ lại cho bước sau
            next_board_str = " ".join(" ".join(str(cell) for cell in row) for row in next_board)
            log_output += f"   > Node kế tiếp sẽ nhảy tới: [{next_board_str}] -> Step: {g + 1}, h: {calculate_manhattan(next_board)}\n"
        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG REACHED
        # =====================================================
        log_output += " REACHED:\n"
        for r in reached:
            r_str = " ".join(" ".join(str(cell) for cell in row) for row in r)
            log_output += f"   > [{r_str}]\n"
        log_output += f"{'=' * 60}\n"

        # =====================================================
        # CHUYỂN TRẠNG THÁI HOẶC DỪNG THUẬT TOÁN
        # =====================================================
        if next_board is not None:
            # Nếu tìm được bước đi tốt hơn, cập nhật và tiếp tục vòng lặp
            current_board = next_board
            current_path = next_path
            reached.add(to_tuple(current_board))
        else:
            # Nếu KHÔNG tìm được node con nào tốt hơn -> Kẹt ở đỉnh cục bộ (Local Optimum)
            log_output += "\n❌ THẤT BẠI: Kẹt ở đỉnh cục bộ (Local Optimum). Không tìm được đường đi tốt hơn.\n"
            return None, log_output

# ===================================================
# HÀM 10: CLIMING HILL - STEEPEST
# ===================================================
def steepest_ascent_hill_climbing(start, goal):
    log_output = "=== STEEPEST-ASCENT HILL CLIMBING SEARCH LOG ===\n"

    step_count = 0

    # Trạng thái hiện tại và đường đi đến trạng thái đó
    current_board = start
    current_path = [start]

    # Reached = tập các trạng thái đã từng đi qua
    reached = set()
    reached.add(to_tuple(start))

    # =========================================================
    # MAIN LOOP
    # =========================================================
    while True:
        step_count += 1
        current_tuple = to_tuple(current_board)

        # Tính h của node hiện tại
        h_current = calculate_manhattan(current_board)
        g = len(current_path) - 1

        # =====================================================
        # LOG NODE HIỆN TẠI
        # =====================================================
        log_output += f"\n{'=' * 60}\n"
        log_output += f" STEP {step_count} | NODE HIỆN TẠI (Step: {g}, h: {h_current})\n"
        log_output += f"{'=' * 60}\n"

        log_output += format_state(current_board) + "\n"
        log_output += f"{'-' * 60}\n"

        # =====================================================
        # CHECK GOAL
        # =====================================================
        if current_board == goal:
            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"
            log_output += f"- Tổng số lượt xét: {step_count}\n"
            log_output += f"- Số bước đi tìm được: {g}\n"
            return current_path, log_output

        # =====================================================
        # SINH NODE CON VÀ CHỌN NODE TỐT NHẤT (BEST CHILD)
        # =====================================================
        generated_children = []

        best_child_board = None
        best_child_path = None
        best_child_h = float('inf')  # Khởi tạo h tốt nhất bằng vô cùng lớn

        # Duyệt QUA TẤT CẢ các trạng thái kế tiếp
        for nxt in next_states(current_board):
            nxt_tuple = to_tuple(nxt)

            # Bỏ qua nếu trạng thái này đã nằm trong reached
            if nxt_tuple in reached:
                continue

            next_h = calculate_manhattan(nxt)
            next_g = g + 1

            nxt_str = " ".join(" ".join(str(cell) for cell in row) for row in nxt)
            generated_children.append({
                'str_log': f"   + Sinh ra: [{nxt_str}] -> Step: {next_g}, h: {next_h}",
                'board': nxt,
                'path': current_path + [nxt],
                'h': next_h
            })

            # TÌM CON TỐT NHẤT: Cập nhật nếu tìm thấy con có h nhỏ hơn best_child_h hiện tại
            if next_h < best_child_h:
                best_child_h = next_h
                best_child_board = nxt
                best_child_path = current_path + [nxt]

        # =====================================================
        # LOG NODE CON
        # =====================================================
        log_output += " CÁC TRẠNG THÁI CON VỪA SINH RA:\n"
        if not generated_children:
            log_output += "   (Không có node hợp lệ)\n"
        else:
            for child in generated_children:
                # Nếu node con này trùng với node tốt nhất vừa tìm được, đánh dấu lại
                if child['board'] == best_child_board:
                    log_output += child['str_log'] + " <--- CON TỐT NHẤT\n"
                else:
                    log_output += child['str_log'] + "\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG FRONTIER (Thể hiện node tốt nhất được giữ lại)
        # =====================================================
        log_output += " FRONTIER HIỆN TẠI:\n"
        # Chỉ chuyển sang node con tốt nhất NẾU nó thực sự tốt hơn node hiện tại (best_child_h < h_current)
        if best_child_board is not None and best_child_h < h_current:
            best_board_str = " ".join(" ".join(str(cell) for cell in row) for row in best_child_board)
            log_output += f"   > Node tốt nhất được chọn: [{best_board_str}] -> Step: {g + 1}, h: {best_child_h}\n"
        else:
            log_output += "   (Trống - Các node con không có node nào tốt hơn node hiện tại)\n"

        log_output += f"{'-' * 60}\n"

        # =====================================================
        # LOG REACHED
        # =====================================================
        log_output += " REACHED:\n"
        for r in reached:
            r_str = " ".join(" ".join(str(cell) for cell in row) for row in r)
            log_output += f"   > [{r_str}]\n"
        log_output += f"{'=' * 60}\n"

        # =====================================================
        # ĐIỀU KIỆN DI CHUYỂN HOẶC DỪNG
        # =====================================================
        if best_child_board is not None and best_child_h < h_current:
            # Di chuyển sang node con tốt nhất đó
            current_board = best_child_board
            current_path = best_child_path
            reached.add(to_tuple(current_board))
        else:
            # Nếu node con tốt nhất cũng KHÔNG tốt hơn node hiện tại -> Bị kẹt đỉnh cục bộ
            log_output += "\n❌ THẤT BẠI: Kẹt ở đỉnh cục bộ (Local Optimum). Không có node con nào tốt hơn trạng thái hiện tại.\n"
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
        value="pop",
        options=[
            ft.dropdown.Option("pop", "Hàm 1: Check khi POP + Add Reached khi POP"),
            ft.dropdown.Option("push", "Hàm 2: Check khi SINH + Add Reached NGAY"),
            ft.dropdown.Option("dfs", "Hàm 3: DFS"),
            ft.dropdown.Option("iddfs", "Hàm 4: ITERATIVE-DFS"),
            ft.dropdown.Option("ucs", "Hàm 5: UCS"),
            ft.dropdown.Option("greedy", "Hàm 6: GREEDY"),
            ft.dropdown.Option("a_star", "Hàm 7: A*"),
            ft.dropdown.Option("ida_star", "Hàm 8: IDA*"),
            ft.dropdown.Option("hillcliming_simple", "HÀM 9: CLIMING HILL - SIMPLE  "),
            ft.dropdown.Option("hillcliming_steepest", "HÀM 10: CLIMING HILL - STEEPEST")
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
        elif mode_dropdown.value == "iddfs":
            path, bfs_log = iddfs(START, GOAL)
        elif mode_dropdown.value == "ucs":
            path, bfs_log = ucs(START, GOAL)
        elif mode_dropdown.value == "greedy":
            path, bfs_log = greedy(START, GOAL)
        elif mode_dropdown.value == "a_star":
            path, bfs_log = a_star(START, GOAL)
        elif mode_dropdown.value == "ida_star":
            path, bfs_log = ida_star(START, GOAL)
        elif mode_dropdown.value == "hillcliming_simple":
            path, bfs_log = simple_hill_climbing(START, GOAL)
        elif mode_dropdown.value == "hillcliming_steepest":
            path, bfs_log = steepest_ascent_hill_climbing(START, GOAL)

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
            ft.Container(content=steps_path_view, margin=ft.margin.only(top=5, bottom=5)),
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
