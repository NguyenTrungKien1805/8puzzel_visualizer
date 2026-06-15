# ===================================================================
#                 Visualizer BFS/DFS/IDDFS/A* 8PUZZEL
# LINK GITHUB:https://github.com/NguyenTrungKien1805/8puzzel_visualizer
# ===================================================================

import copy
import heapq
import itertools
import math
import random
from collections import deque
from random import shuffle

import flet as ft

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

# 1. Mẫu khuyết START
START_KHUYET = [
    [1, 2, 3],
    [4, 0, 6],
    [7, "?", "?"]
]

# 2. Mẫu khuyết GOAL
GOAL_KHUYET = [
    [1, 2, 3],
    [4, "?", "?"],
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


# Hàm sinh ra các BS
def generate_belief_state(matrix):
    """Sinh ra tập hợp niềm tin (Belief State) chứa các ma trận khả dĩ từ dấu '?'"""
    flat_list = [cell for row in matrix for cell in row]
    existing_nums = {cell for cell in flat_list if cell != "?"}
    missing_nums = list(set(range(9)) - existing_nums)

    question_positions = []
    for r in range(3):
        for c in range(3):
            if matrix[r][c] == "?":
                question_positions.append((r, c))

    if not question_positions:
        return [matrix]

    belief_set = []
    for perm in itertools.permutations(missing_nums):
        new_matrix = [row[:] for row in matrix]
        for (r, c), num in zip(question_positions, perm):
            new_matrix[r][c] = num
        belief_set.append(new_matrix)
    return belief_set


def extract_real_path_from_belief(belief_path, goal_matrix):
    """Hàm phụ giúp lọc ra đúng 1 chuỗi ma trận đơn lẻ từ chuỗi tập hợp niềm tin để vẽ lên UI"""
    # Đi ngược từ goal_matrix về đầu để tìm các ma trận cha hợp lệ trong từng tập hợp niềm tin
    real_path = [goal_matrix]
    current_matrix = goal_matrix

    for i in range(len(belief_path) - 2, -1, -1):
        belief_set = belief_path[i]
        # Tìm xem trong tập niềm tin này, ma trận nào có thể đi tới current_matrix bằng 1 bước
        found_parent = False
        for state_tuple in belief_set:
            matrix_form = [list(row) for row in state_tuple]
            if current_matrix in next_states(matrix_form):
                real_path.append(matrix_form)
                current_matrix = matrix_form
                found_parent = True
                break
        if not found_parent:
            # Nếu không tìm thấy (do thuật toán nhảy cóc), lấy đại phần tử đầu tiên của tập niềm tin đó để không lỗi UI
            first_state = list(belief_set)[0]
            current_matrix = [list(row) for row in first_state]
            real_path.append(current_matrix)

    return real_path[::-1]  # Đảo ngược lại để có chuỗi từ START -> GOAL


def count_inversions(matrix):
    """Đếm số nghịch thế của một ma trận (bỏ qua số 0 và dấu '?')"""
    flatten = []
    for r in range(3):
        for c in range(3):
            if matrix[r][c] != 0 and matrix[r][c] != "?":
                flatten.append(matrix[r][c])
    inversions = 0
    for i in range(len(flatten)):
        for j in range(i + 1, len(flatten)):
            if flatten[i] > flatten[j]:
                inversions += 1
    return inversions


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


# ===================================================
# HÀM 11: CLIMING HILL - RANDOM
# ===================================================
def random_hill_climbing(start, goal):
    log_output = "=== RANDOM HILL CLIMBING SEARCH LOG ===\n"

    step_count = 0

    current_board = start
    current_path = [start]

    reached = set()
    reached.add(to_tuple(start))

    while True:

        step_count += 1

        h_current = calculate_manhattan(current_board)
        g = len(current_path) - 1

        log_output += f"\n{'=' * 60}\n"
        log_output += f" STEP {step_count} | NODE HIỆN TẠI (Step: {g}, h: {h_current})\n"
        log_output += f"{'=' * 60}\n"

        log_output += format_state(current_board) + "\n"

        if current_board == goal:
            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"
            return current_path, log_output

        better_children = []

        log_output += "\n CÁC TRẠNG THÁI CON:\n"

        for nxt in next_states(current_board):

            nxt_tuple = to_tuple(nxt)

            if nxt_tuple in reached:
                continue

            h = calculate_manhattan(nxt)

            log_output += (
                f"   + Sinh ra: "
                f"[{' '.join(' '.join(map(str, row)) for row in nxt)}]"
                f" -> h={h}\n"
            )

            if h < h_current:
                better_children.append(nxt)

        if not better_children:
            log_output += "\n❌ THẤT BẠI: Local Optimum\n"
            return None, log_output

        chosen = random.choice(better_children)

        log_output += "\n RANDOM CHỌN:\n"
        log_output += (
            f"   > [{' '.join(' '.join(map(str, row)) for row in chosen)}]\n"
        )

        current_board = chosen
        current_path.append(chosen)

        reached.add(to_tuple(chosen))


def random_state(num_moves=30):
    state = copy.deepcopy(GOAL)

    for _ in range(num_moves):
        state = random.choice(next_states(state))

    return state


# ===================================================
# HÀM 12: CLIMING HILL - RESTART
# ===================================================
def random_restart_hill_climbing(start, goal, max_restart=10):
    log_output = "=== RANDOM RESTART HILL CLIMBING ===\n"
    total_steps = 0

    for restart in range(max_restart):
        log_output += f"\n\n{'#' * 70}\n"
        log_output += f" RESTART LẦN THỨ {restart + 1}\n"
        log_output += f"{'#' * 70}\n"

        # LUÔN LUÔN BẮT ĐẦU TỪ TRẠNG THÁI 'START' CỦA NGƯỜI DÙNG
        current = start
        path = [current]

        # Để tránh việc lặp lại chính xác các bước đi cũ của lần restart trước,
        # ta có thể dùng tập set để lưu các trạng thái đã đi qua TRONG LẦN RESTART NÀY
        visited = set()
        visited.add(to_tuple(current))

        while True:
            total_steps += 1
            h_current = calculate_manhattan(current)

            # In trạng thái hiện tại ra log cho đẹp
            log_output += f"Bước {total_steps} | Trạng thái hiện tại có h(x) = {h_current}\n"

            if current == goal:
                log_output += f"\n🎉 TÌM THẤY ĐÍCH THÀNH CÔNG!\n"
                log_output += f"Tìm thấy ở lượt Restart thứ: {restart + 1}\n"
                log_output += f"Tổng số bước đã duyệt qua tất cả lượt: {total_steps}\n"
                return path, log_output

            better_children = []
            for nxt in next_states(current):
                # Kiểm tra xem trạng thái kế tiếp có tốt hơn và chưa từng đi qua trong lượt này không
                if to_tuple(nxt) not in visited:
                    h = calculate_manhattan(nxt)
                    if h < h_current:
                        better_children.append(nxt)

            # Nếu không tìm được hàng xóm nào tốt hơn -> Bị kẹt đỉnh cục bộ (Local Optimum)
            if not better_children:
                log_output += f"\n⚠️ Gặp đỉnh cục bộ (Local Optimum) tại h = {h_current}!\n"
                log_output += "👉 Thực hiện RESTART (Quay lại trạng thái xuất phát ban đầu để tìm hướng đi mới...)\n"
                break  # Thoát vòng lặp while để nhảy lên vòng lặp for (Restart)

            # Chọn ngẫu nhiên ĐƯỜNG ĐI MỚI trong số các con tốt hơn để tạo sự khác biệt giữa các lần Restart
            current = random.choice(better_children)
            path.append(current)
            visited.add(to_tuple(current))

    log_output += f"\n❌ THẤT BẠI: Đã thử tối đa {max_restart} lần restart nhưng không tìm thấy lời giải."
    return None, log_output


# ===================================================
# HÀM 13: BEAM - SEARCH
# ===================================================
def beam_search(start, goal, beam_width=3):
    log_output = "=== BEAM SEARCH LOG ===\n"

    frontier = [(start, [start])]

    reached = set()
    reached.add(to_tuple(start))

    level = 0

    while frontier:

        level += 1

        log_output += f"\n{'=' * 60}\n"
        log_output += f" LEVEL {level}\n"
        log_output += f"{'=' * 60}\n"

        candidates = []

        for board, path in frontier:

            h = calculate_manhattan(board)

            log_output += (
                f"\nNode h={h}\n"
            )

            if board == goal:
                log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"

                return path, log_output

            for nxt in next_states(board):

                t = to_tuple(nxt)

                if t in reached:
                    continue

                reached.add(t)

                nxt_h = calculate_manhattan(nxt)

                candidates.append(
                    (nxt_h, nxt, path + [nxt])
                )

                log_output += (
                    f"   + h={nxt_h}\n"
                )

        candidates.sort(key=lambda x: x[0])

        frontier = []

        log_output += "\nGIỮ LẠI:\n"

        for h, board, path in candidates[:beam_width]:
            frontier.append((board, path))

            log_output += (
                f"   > h={h}\n"
            )

    log_output += "\n❌ KHÔNG TÌM THẤY ĐƯỜNG ĐI\n"

    return None, log_output


# ===================================================
# HÀM 14: SIMULATED - ANNEALING
# ===================================================
def simulated_annealing(start, goal, initial_temp=100.0, cooling_rate=0.95, max_steps=1000):
    """
    Thuật toán Simulated Annealing cho bài toán tìm kiếm đồ thị (ví dụ: 8-puzzle).
    - initial_temp: Nhiệt độ ban đầu (T)
    - cooling_rate: Tốc độ giảm nhiệt (alpha), T = T * cooling_rate
    - max_steps: Số bước lặp tối đa để tránh vòng lặp vô hạn
    """

    log_output = "=== SIMULATED ANNEALING LOG ===\n"

    # Khởi tạo trạng thái hiện tại
    current_board = start
    current_path = [start]
    current_h = calculate_manhattan(current_board)

    T = initial_temp
    step = 0

    while step < max_steps and T > 0.01:
        step += 1

        log_output += f"\n{'=' * 60}\n"
        log_output += f" BƯỚC {step} | Nhiệt độ T = {T:.4f}\n"
        log_output += f"{'=' * 60}\n"
        log_output += f"Trạng thái hiện tại có h = {current_h}\n"

        # Kiểm tra nếu trạng thái hiện tại đã là đích
        if current_board == goal:
            log_output += "\n🎉 TÌM THẤY ĐÍCH!\n"
            return current_path, log_output

        # Lấy tất cả các trạng thái kế tiếp (hàng xóm)
        neighbors = next_states(current_board)
        if not neighbors:
            log_output += "❌ Cụt đường (Không có trạng thái kế tiếp)\n"
            break

        # Simulated Annealing CHỌN NGẪU NHIÊN một trạng thái hàng xóm
        nxt = random.choice(neighbors)
        nxt_h = calculate_manhattan(nxt)

        log_output += f"👉 Chọn ngẫu nhiên hàng xóm có h_mới = {nxt_h}\n"

        # Vì ta đang TỐI ƯU HÓA (tìm h nhỏ nhất, h=0 là đích):
        # Delta_E = h_hiện_tại - h_mới (Nếu h_mới nhỏ hơn h_hiện_tại thì Delta_E > 0, tức là tốt hơn)
        delta_e = current_h - nxt_h

        if delta_e > 0:
            # Trạng thái mới tốt hơn -> Chấp nhận ngay lập tức
            current_board = nxt
            current_h = nxt_h
            current_path.append(nxt)
            log_output += "   ✅ [TỐT HƠN] Chấp nhận trạng thái mới này.\n"
        else:
            # Trạng thái mới tệ hơn hoặc bằng -> Chấp nhận dựa trên xác suất Boltzmann
            # P = e^(delta_e / T)
            probability = math.exp(delta_e / T)
            rand_val = random.random()

            log_output += f"   ⚠️ [TỆ HƠN] Delta E = {delta_e} | Xác suất chấp nhận P = {probability:.4f} | Khảo sát: {rand_val:.4f}\n"

            if rand_val < probability:
                current_board = nxt
                current_h = nxt_h
                current_path.append(nxt)
                log_output += "   🎲 [MAY MẮN] Vẫn chấp nhận trạng thái tệ hơn này để thoát bẫy cực tiểu cục bộ!\n"
            else:
                log_output += "   ❌ [TỪ CHỐI] Giữ nguyên trạng thái cũ.\n"

        # Giảm nhiệt độ theo lịch trình (Cooling schedule)
        T *= cooling_rate

    # Nếu chạy hết số bước hoặc nhiệt độ quá lạnh mà chưa tới đích
    if current_board == goal:
        log_output += "\n🎉 TÌM THẤY ĐÍCH Ở BƯỚC CUỐI CÙNG!\n"
        return current_path, log_output

    log_output += "\n❌ KHÔNG TÌM THẤY ĐƯỜNG ĐI (Hết thời gian hoặc nhiệt độ quá thấp)\n"
    return None, log_output


# ===================================================
# HÀM 15: A* giải với Belief Start
# ===================================================
def solve_missing_start(custom_start, custom_goal):
    log_output = "=== HÀM 15: A* KHÔNG GIAN NIỀM TIN (TỐI ƯU HÓA TỐC ĐỘ) ===\n"

    # 1. Sinh tập hợp niềm tin ban đầu (các cấu hình ma trận điền số khả dĩ)
    initial_matrices = generate_belief_state(custom_start)

    log_output += f"Khởi tạo tập trạng thái niềm tin gồm {len(initial_matrices)} ma trận.\n"
    log_output += "Hệ thống đang giải mã độc lập từng thế giới song hành để chống quá tải bộ nhớ...\n\n"

    paths_list = []
    total_nodes_expanded = 0

    # Hàm A* chuẩn dùng để giải nhanh cho từng ma trận riêng lẻ
    def single_astar(start_mat):
        # Bản đồ tọa độ đích dùng để tính khoảng cách Manhattan
        goal_pos = {}
        for r in range(3):
            for c in range(3):
                goal_pos[custom_goal[r][c]] = (r, c)

        def get_h(mat):
            h = 0
            for r in range(3):
                for c in range(3):
                    val = mat[r][c]
                    if val != 0 and val != "?":
                        tr, tc = goal_pos[val]
                        h += abs(r - tr) + abs(c - tc)
            return h

        start_tup = to_tuple(start_mat)
        open_set = []
        counter = 0
        heapq.heappush(open_set, (get_h(start_mat), 0, counter, start_tup, [start_mat]))
        g_score = {start_tup: 0}
        nodes = 0

        while open_set:
            f, g, _, curr_tup, path = heapq.heappop(open_set)
            nodes += 1
            curr_mat = [list(row) for row in curr_tup]

            # Chạm đích thành công
            if curr_mat == custom_goal:
                return path, nodes

            # Sinh trạng thái kế tiếp
            for nxt_mat in next_states(curr_mat):
                nxt_tup = to_tuple(nxt_mat)
                tentative_g = g + 1
                if nxt_tup not in g_score or tentative_g < g_score[nxt_tup]:
                    g_score[nxt_tup] = tentative_g
                    counter += 1
                    f_nxt = tentative_g + get_h(nxt_mat)
                    heapq.heappush(open_set, (f_nxt, tentative_g, counter, nxt_tup, path + [nxt_mat]))

        return None, nodes  # Không tìm thấy đường đi (Ma trận vô nghiệm)

    # 2. Duyệt qua từng ma trận trong tập niềm tin để giải độc lập
    for idx, start_matrix in enumerate(initial_matrices):
        path, nodes = single_astar(start_matrix)
        total_nodes_expanded += nodes

        if path:
            paths_list.append(path)
            log_output += f"-> Cấu hình {idx + 1} giải THÀNH CÔNG (Mất {len(path) - 1} bước).\n"
        else:
            log_output += f"-> Cấu hình {idx + 1} LỖI VÔ NGHIỆM (Loại bỏ theo luật nghịch thế).\n"

    # 3. Kết luận
    if not paths_list:
        log_output += "\n❌ Thất bại: Tất cả các thế giới khả dĩ đều rơi vào trạng thái vô nghiệm!"
        return None, log_output, []

    log_output += f"\n🎉 HOÀN TẤT! Đã giải quyết xong tập hợp niềm tin.\n"
    log_output += f"Tổng số nút đã mở rộng trên toàn hệ thống: {total_nodes_expanded}\n"

    # Trả về: (Đường đi của cấu hình đầu tiên giải được, Nhật ký log, Danh sách toàn bộ các đường đi)
    return paths_list[0], log_output, paths_list


# ===================================================
# HÀM 16: A* giải với Belief Goal
# ===================================================
def solve_missing_goal(custom_start, custom_goal):
    # Tìm các ô chứa dấu '?' và các số đã có trong GOAL
    positions = []
    present_nums = set()
    for r in range(3):
        for c in range(3):
            if custom_goal[r][c] == "?":
                positions.append((r, c))
            else:
                present_nums.add(custom_goal[r][c])

    # Xác định danh sách các số còn thiếu từ 0 đến 8
    missing_nums = list(set(range(9)) - present_nums)

    # Hoán vị để sinh ra toàn bộ ma trận đích khả dĩ
    possible_goals = []
    for perm in itertools.permutations(missing_nums):
        temp_goal = copy.deepcopy(custom_goal)
        for (r, c), num in zip(positions, perm):
            temp_goal[r][c] = num
        possible_goals.append(temp_goal)

    paths_list = []
    log_output = f"📋 Khởi tạo tập trạng thái ĐÍCH gồm {len(possible_goals)} ma trận khả dĩ.\n"

    # Tính tính chẵn lẻ của START (vì start cố định)
    start_parity = count_inversions(custom_start) % 2

    # Thử giải từng ma trận đích
    for idx, goal_matrix in enumerate(possible_goals):
        # 🔥 CẢI TIẾN: Lọc toán học - Nếu tính chẵn lẻ lệch nhau -> Chắc chắn vô nghiệm!
        if (count_inversions(goal_matrix) % 2) != start_parity:
            log_output += f"-> Cấu hình Đích {idx + 1} Loại bỏ ngay (Vô nghiệm do lệch cấu trúc nghịch thế).\n"
            continue

        # Gọi hàm A* mặc định của bạn để giải thử
        path, _ = a_star(custom_start, goal_matrix)
        if path:
            paths_list.append(path)
            log_output += f"-> Cấu hình Đích {idx + 1} GIẢI THÀNH CÔNG (Mất {len(path) - 1} bước).\n"

    log_output += f"\n🎉 HOÀN TẤT! Tìm thấy {len(paths_list)} cấu hình đích có lời giải hợp lệ."
    primary_path = paths_list[0] if paths_list else None

    return primary_path, log_output, paths_list


# ===================================================
# HÀM 17: A* giải với Belief Start - Goal
# ===================================================
def solve_missing_both(custom_start, custom_goal):
    # 1. Sinh tập ma trận START khả dĩ
    start_positions = []
    start_present = set()
    for r in range(3):
        for c in range(3):
            if custom_start[r][c] == "?":
                start_positions.append((r, c))
            else:
                start_present.add(custom_start[r][c])
    missing_starts = list(set(range(9)) - start_present)

    possible_starts = []
    for perm in itertools.permutations(missing_starts):
        temp_start = copy.deepcopy(custom_start)
        for (r, c), num in zip(start_positions, perm):
            temp_start[r][c] = num
        possible_starts.append(temp_start)

    # 2. Sinh tập ma trận GOAL khả dĩ
    goal_positions = []
    goal_present = set()
    for r in range(3):
        for c in range(3):
            if custom_goal[r][c] == "?":
                goal_positions.append((r, c))
            else:
                goal_present.add(custom_goal[r][c])
    missing_goals = list(set(range(9)) - goal_present)

    possible_goals = []
    for perm in itertools.permutations(missing_goals):
        temp_goal = copy.deepcopy(custom_goal)
        for (r, c), num in zip(goal_positions, perm):
            temp_goal[r][c] = num
        possible_goals.append(temp_goal)

    paths_list = []
    total_pairs = len(possible_starts) * len(possible_goals)
    log_output = f"📋 Tổng số cặp tổ hợp lý thuyết giữa (Start × Goal): {total_pairs} cặp.\n"

    pair_idx = 1
    # Duyệt bắt cặp song song
    for start_matrix in possible_starts:
        start_parity = count_inversions(start_matrix) % 2
        for goal_matrix in possible_goals:

            # 🔥 CẢI TIẾN: Bỏ qua ngay lập tức nếu cặp này không đồng nhất tính chẵn lẻ
            if (count_inversions(goal_matrix) % 2) != start_parity:
                pair_idx += 1
                continue

            # Chỉ chạy A* thực sự cho những cặp có khả năng sinh nghiệm
            path, _ = a_star(start_matrix, goal_matrix)
            if path:
                paths_list.append(path)
                f_start = [n for row in start_matrix for n in row]
                f_goal = [n for row in goal_matrix for n in row]
                log_output += f"-> Cặp {pair_idx}: {f_start} ➔ {f_goal} GIẢI THÀNH CÔNG ({len(path) - 1} bước).\n"
            pair_idx += 1

    log_output += f"\n🎉 HOÀN TẤT! Đã quét xong, hệ thống tìm thấy {len(paths_list)} cặp thế giới tương thích."
    primary_path = paths_list[0] if paths_list else None

    return primary_path, log_output, paths_list

# ===================================================
# HÀM 18: AND-OR GRAPH SEARCH
# ===================================================

def and_or_graph_search(start, goal):

    logs = []

    logs.append("=== AND-OR GRAPH SEARCH LOG ===\n")

    start_tuple = tuple(tuple(row) for row in start)
    goal_tuple = tuple(tuple(row) for row in goal)

    logs.append(
        "\nSTART STATE:\n"
        f"{format_state(start)}\n"
    )

    result_plan = or_search(
        start_tuple,
        goal_tuple,
        [],
        logs
    )

    if result_plan == "failure":

        logs.append(
            "\n❌ NO SOLUTION FOUND\n"
        )

        return None, "".join(logs)

    final_path = []

    for state_tuple in result_plan:

        matrix = [list(row) for row in state_tuple]

        if not final_path or matrix != final_path[-1]:
            final_path.append(matrix)

    logs.append(
        f"\n🎉 SOLUTION FOUND\n"
        f"PATH LENGTH = {len(final_path) - 1}\n"
    )

    return final_path, "".join(logs)


# ===================================================
# OR SEARCH
# ===================================================

def or_search(state, goal, path, logs):

    logs.append(
        "\n====================================\n"
        "OR NODE\n"
        f"{format_state([list(row) for row in state])}\n"
    )

    # Goal Test
    if state == goal:

        logs.append(
            "\n🎯 GOAL FOUND\n"
        )

        return [state]

    # Cycle Detection
    if state in path:

        logs.append(
            "\n🔄 CYCLE DETECTED\n"
        )

        return "failure"

    successors = get_puzzle_successors(state)

    logs.append(
        f"SUCCESSORS = {len(successors)}\n"
    )

    for i, next_state in enumerate(successors, 1):

        logs.append(
            f"\nTRY SUCCESSOR {i}\n"
            f"{format_state([list(row) for row in next_state])}\n"
        )

        # RESULTS(action)
        plan = and_search(
            [next_state],
            goal,
            [state] + path,
            logs
        )

        if plan != "failure":

            logs.append(
                "\n✅ SUCCESS PATH FOUND\n"
            )

            return [state] + plan

    logs.append(
        "\n❌ ALL SUCCESSORS FAILED\n"
    )

    return "failure"


# ===================================================
# AND SEARCH
# ===================================================

def and_search(states, goal, path, logs):

    logs.append(
        f"\nAND NODE ({len(states)} STATES)\n"
    )

    combined_plan = []

    for s in states:

        logs.append(
            "\nPROCESS STATE IN AND NODE\n"
            f"{format_state([list(row) for row in s])}\n"
        )

        plan_i = or_search(
            s,
            goal,
            path,
            logs
        )

        if plan_i == "failure":

            logs.append(
                "\n❌ AND NODE FAILED\n"
            )

            return "failure"

        combined_plan.extend(plan_i)

    logs.append(
        "\n✅ AND NODE SUCCESS\n"
    )

    return combined_plan


# ===================================================
# SUCCESSOR GENERATOR
# ===================================================

def get_puzzle_successors(state):

    r_zero = 0
    c_zero = 0

    for r in range(3):
        for c in range(3):

            if state[r][c] == 0:

                r_zero = r
                c_zero = c
                break

    successors = []

    directions = [
        (-1, 0),  # UP
        (1, 0),   # DOWN
        (0, -1),  # LEFT
        (0, 1)    # RIGHT
    ]

    for dr, dc in directions:

        nr = r_zero + dr
        nc = c_zero + dc

        if 0 <= nr < 3 and 0 <= nc < 3:

            next_state = [list(row) for row in state]

            next_state[r_zero][c_zero] = next_state[nr][nc]
            next_state[nr][nc] = 0

            successors.append(
                tuple(tuple(row) for row in next_state)
            )

    return successors


# ===================================================
# HÀM 19: BACKTRACKING SEARCH (CSP)
# ===================================================
def backtracking_search(start, goal):
    log_output = "=== BACKTRACKING SEARCH LOG ===\n"
    visited = set()

    def backtrack(current, path):

        log_output_local = ""

        current_tuple = to_tuple(current)

        if current_tuple in visited:
            return None, log_output_local

        visited.add(current_tuple)

        log_output_local += (
            f"\nĐANG XÉT:\n"
            f"{format_state(current)}\n"
        )

        # Goal Test
        if current == goal:
            log_output_local += "\n🎉 TÌM THẤY ĐÍCH!\n"
            return path, log_output_local

        # ORDER-DOMAIN-VALUES
        children = next_states(current)

        # Sắp xếp theo heuristic Manhattan
        children.sort(key=calculate_manhattan)

        for child in children:

            log_output_local += (
                f"\nTHỬ NODE CON h={calculate_manhattan(child)}\n"
            )

            result, child_log = backtrack(
                child,
                path + [child]
            )

            log_output_local += child_log

            if result is not None:
                return result, log_output_local

        log_output_local += "\n↩ BACKTRACK\n"

        visited.remove(current_tuple)

        return None, log_output_local

    path, log = backtrack(start, [start])

    log_output += log

    if path is None:
        log_output += "\n❌ KHÔNG TÌM THẤY ĐƯỜNG ĐI\n"

    return path, log_output


# ===================================================
# HÀM 20: CSP WITH DOMAIN SEARCH
# ===================================================
def csp_domain_search(start, goal):
    log_output = "=== CSP DOMAIN SEARCH LOG ===\n"

    visited = set()

    # Variable
    def select_variable(state):
        return state

    # Domain
    def get_domain(state):
        return next_states(state)

    # Constraint
    def consistent(candidate):
        return to_tuple(candidate) not in visited

    def backtrack(state, path):

        nonlocal log_output

        if state == goal:
            log_output += "\nGOAL FOUND!\n"
            return path

        visited.add(to_tuple(state))

        variable = select_variable(state)

        domain = get_domain(variable)

        log_output += (
            f"\nCURRENT STATE:\n"
            f"{format_state(state)}\n"
            f"DOMAIN SIZE = {len(domain)}\n"
        )

        # ưu tiên trạng thái gần đích hơn
        domain.sort(key=calculate_manhattan)

        for value in domain:

            if consistent(value):

                log_output += (
                    f"\nTRY DOMAIN VALUE "
                    f"(h={calculate_manhattan(value)})\n"
                )

                result = backtrack(
                    value,
                    path + [value]
                )

                if result:
                    return result

        visited.remove(to_tuple(state))

        log_output += "\nBACKTRACK\n"

        return None

    result = backtrack(start, [start])

    return result, log_output

# ===================================================================
# MAIN UI APPLICATION
# ===================================================================
def main(page: ft.Page):
    page.title = "8 Puzzle Algorithm Visualizer"
    page.window_width = 1150
    page.window_height = 680
    page.theme_mode = ft.ThemeMode.DARK
    page.window_center()

    solution = [[]]
    current_step = [0]
    running = [False]
    board_tiles = {}

    # Biến cục bộ để theo dõi ô nào đang được focus
    current_focused_control = [None]

    # --- Lưu trữ tham chiếu các ô nhập liệu TextField (3x3) ---
    start_inputs = [[None for _ in range(3)] for _ in range(3)]
    goal_inputs = [[None for _ in range(3)] for _ in range(3)]

    # --- KHỐI BÊN TRÁI ---
    info = ft.Text("Chọn hàm thuật toán và bấm 'Giải 8 - Puzzle'.", size=14, italic=True)
    grid = ft.Stack(controls=[], width=250, height=250)

    # --- CẤU HÌNH THÔNG SỐ CHO BEAM SEARCH ---
    beam_width_input = ft.TextField(label="Độ rộng Beam (k)", value="3", width=260,
                                    keyboard_type=ft.KeyboardType.NUMBER)
    beam_config_container = ft.Row(controls=[beam_width_input], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    # --- CẤU HÌNH THÔNG SỐ CHO RANDOM RESTART HILL CLIMBING ---
    restart_max_input = ft.TextField(label="Số lần Restart tối đa", value="10", width=260,
                                     keyboard_type=ft.KeyboardType.NUMBER)
    restart_config_container = ft.Row(controls=[restart_max_input], alignment=ft.MainAxisAlignment.CENTER,
                                      visible=False)

    # --- CẤU HÌNH THÔNG SỐ CHO SIMULATED ANNEALING ---
    sa_temp_input = ft.TextField(label="Nhiệt độ", value="100.0", width=130,
                                 keyboard_type=ft.KeyboardType.NUMBER)
    sa_cooling_input = ft.TextField(label="Cooling", value="0.95", width=130,
                                    keyboard_type=ft.KeyboardType.NUMBER)
    sa_config_container = ft.Row(controls=[sa_temp_input, sa_cooling_input], alignment=ft.MainAxisAlignment.CENTER,
                                 visible=False)

    # 1. Danh sách đầy đủ cho môi trường Fully Observable
    FULL_ALGO_OPTIONS = [
        ft.dropdown.Option("pop", "Hàm 1: Check khi POP + Add Reached khi POP"),
        ft.dropdown.Option("push", "Hàm 2: Check khi SINH + Add Reached NGAY"),
        ft.dropdown.Option("dfs", "Hàm 3: DFS"),
        ft.dropdown.Option("iddfs", "Hàm 4: ITERATIVE-DFS"),
        ft.dropdown.Option("ucs", "Hàm 5: UCS"),
        ft.dropdown.Option("greedy", "Hàm 6: GREEDY"),
        ft.dropdown.Option("a_star", "Hàm 7: A*"),
        ft.dropdown.Option("ida_star", "Hàm 8: IDA*"),
        ft.dropdown.Option("hillcliming_simple", "Hàm 9: HILL CLIMBING - SIMPLE"),
        ft.dropdown.Option("hillcliming_steepest", "Hàm 10: HILL CLIMBING - STEEPEST"),
        ft.dropdown.Option("hillcliming_random", "Hàm 11: HILL CLIMBING - RANDOM"),
        ft.dropdown.Option("hillcliming_restart", "Hàm 12: RANDOM RESTART HILL CLIMBING"),
        ft.dropdown.Option("beam_search", "Hàm 13: BEAM SEARCH"),
        ft.dropdown.Option("simulated_annealing", "Hàm 14: SIMULATED ANNEALING"),
        ft.dropdown.Option("and_or", "Hàm 18: AND OR SEARCH"),
        ft.dropdown.Option("backtracking", "Hàm 19: BACKTRACKING SEARCH"),
        ft.dropdown.Option("csp_domain", "Hàm 20: CSP WITH DOMAIN SEARCH")
    ]

    # 2. Danh sách cho môi trường Partially Observable
    HIDDEN_ALGO_OPTIONS = [
        ft.dropdown.Option("solve_missing_start", "Hàm 15: A* giải với Belief Start"),
        ft.dropdown.Option("solve_missing_goal", "Hàm 16: A* giải với Belief Goal"),
        ft.dropdown.Option("solve_missing_both", "Hàm 17: A* giải với Belief Start - Goal"),
    ]

    # Hàm xử lý ẩn hiện khi người dùng đổi thuật toán trong dropdown
    # Hàm xử lý ẩn hiện khi người dùng đổi thuật toán trong dropdown
    def on_algo_change(e):
        # 1. Trước tiên, mặc định ẩn tất cả các khối cấu hình đi (Giữ nguyên code cũ)
        sa_config_container.visible = False
        beam_config_container.visible = False
        restart_config_container.visible = False

        # 2. Quét giá trị hiện tại của dropdown để bật khối tương ứng lên
        if mode_dropdown.value == "simulated_annealing":
            sa_config_container.visible = True
        elif mode_dropdown.value == "beam_search":
            beam_config_container.visible = True
        elif mode_dropdown.value == "hillcliming_restart":
            restart_config_container.visible = True

        # --- PHẦN CẬP NHẬT ĐỒNG BỘ MA TRẬN VÀ VẼ LẠI NGAY LÚC CHUYỂN ĐỔI ---
        if env_radio.value == "fully_observable":
            # Khi ở môi trường đầy đủ, nạp lại ma trận số sạch
            reload_input_matrix_ui(START, start_inputs)
            reload_input_matrix_ui(GOAL, goal_inputs)
        else:
            # Khi ở môi trường ẩn, nạp ma trận khuyết tùy theo thuật toán được chọn
            if mode_dropdown.value == "solve_missing_start":
                reload_input_matrix_ui(START_KHUYET, start_inputs)
                reload_input_matrix_ui(GOAL, goal_inputs)
            elif mode_dropdown.value == "solve_missing_goal":
                reload_input_matrix_ui(START, start_inputs)
                reload_input_matrix_ui(GOAL_KHUYET, goal_inputs)
            elif mode_dropdown.value == "solve_missing_both":
                reload_input_matrix_ui(START_KHUYET, start_inputs)
                reload_input_matrix_ui(GOAL_KHUYET, goal_inputs)

        # Khởi tạo vẽ lại bàn cờ lớn dựa theo cấu hình ô nhập liệu mới nạp
        try:
            current_start = parse_input_matrix(start_inputs)
            draw_board(current_start)
        except ValueError:
            draw_board(START)

        # 3. Yêu cầu Flet render vẽ lại giao diện
        page.update()

    # Hàm phụ hỗ trợ ghi đè dữ liệu mảng lên các ô TextField UI đang hiển thị
    def reload_input_matrix_ui(matrix_data, storage_grid):
        for r in range(3):
            for c in range(3):
                storage_grid[r][c].value = str(matrix_data[r][c])
                storage_grid[r][c].update()

    mode_dropdown = ft.Dropdown(
        value="pop",
        options=FULL_ALGO_OPTIONS,
        width=360,
        on_change=on_algo_change
    )

    steps_path_view = ft.TextField(
        label="Bước hiện tại",
        read_only=True,
        value="0 / 0",
        text_align=ft.TextAlign.CENTER,
        text_style=ft.TextStyle(font_family="monospace", size=18, weight=ft.FontWeight.BOLD, color="greenyellow")
    )

    # --- HÀM TẠO MA TRẬN NHẬP LIỆU ---
    def create_input_matrix(matrix_data, storage_grid, matrix_name):
        rows_controls = []
        for r in range(3):
            row_controls = []
            for c in range(3):
                val = str(matrix_data[r][c])

                def make_on_change(current_r, current_c):
                    def on_change(e):
                        text = e.control.value

                        if len(text) > 1:
                            e.control.value = text[-1]
                            e.control.update()

                        try:
                            update_board_from_inputs(None)
                            page.update()
                        except Exception as ex:
                            print("Update error:", ex)

                    return on_change

                def make_on_focus():
                    def on_focus(e):
                        current_focused_control[0] = e.control

                    return on_focus

                tf = ft.TextField(
                    value=val,
                    width=45,
                    height=45,
                    content_padding=4,
                    text_align=ft.TextAlign.CENTER,
                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                    border_color="blue400" if matrix_name == "START" else "orange400",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    on_change=make_on_change(r, c),  # Gắn sự kiện lắng nghe thay đổi số
                    on_focus=make_on_focus()
                )

                tf.data = {"row": r, "col": c, "matrix": matrix_name}
                storage_grid[r][c] = tf
                row_controls.append(tf)
            rows_controls.append(ft.Row(row_controls, spacing=5, alignment=ft.MainAxisAlignment.CENTER))
        return ft.Column(rows_controls, spacing=5)

    def on_environment_change(e):
        belief_select_container.visible = False
        # 1. Thay đổi danh sách thuật toán hiển thị theo môi trường (Giữ nguyên logic của bạn)
        if env_radio.value == "partially_observable":
            mode_dropdown.options = HIDDEN_ALGO_OPTIONS
            mode_dropdown.value = "solve_missing_start"
        else:
            mode_dropdown.options = FULL_ALGO_OPTIONS
            mode_dropdown.value = "pop"

        on_algo_change(None)  # Đồng bộ nạp lại ma trận mẫu khuyết/đầy đủ vào ô nhập liệu

        # 2. XỬ LÝ ÉP VẼ LẠI BÀN CỜ ĐỂ CẬP NHẬT GIAO DIỆN XUỐNG GRID MÔ PHỎNG
        # Nếu người dùng đã bấm Giải và đang ở một bước nào đó trong tiến trình nghiệm
        if solution[0] and current_step[0] < len(solution[0]):
            # Vẽ lại chính xác ma trận trạng thái của bước đó
            draw_board(solution[0][current_step[0]])
        else:
            # Nếu chưa bấm Giải, lấy dữ liệu thô đang nằm trong các ô TextField để vẽ mẫu
            try:
                current_start = parse_input_matrix(start_inputs)
                draw_board(current_start)
            except ValueError:
                # Nếu ô nhập liệu lỗi hoặc trống, vẽ mảng gốc START mặc định làm nền
                draw_board(START)

        page.update()  # Đẩy cập nhật lên màn hình Flet

    env_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="fully_observable", label="Môi trường thấy (Đầy đủ)"),
            ft.Radio(value="partially_observable", label="Môi trường ẩn (Khuyết ô ?)")
        ], alignment=ft.MainAxisAlignment.CENTER),
        value="fully_observable",
        on_change=on_environment_change
    )

    # --- BỘ XỬ LÝ SỰ KIỆN BÀN PHÍM AN TOÀN CHO FLET ---
    def on_keyboard(e: ft.KeyboardEvent):
        active_control = current_focused_control[0]
        if not active_control or not hasattr(active_control, "data") or active_control.data is None:
            return

        info_data = active_control.data
        r = info_data["row"]
        c = info_data["col"]
        m_name = info_data["matrix"]

        target_r, target_c, target_m = r, c, m_name

        if e.key == "Enter" or e.key == "Arrow Right":
            target_c = c + 1
            if target_c > 2:
                target_c = 0
                target_r = r + 1
            if target_r > 2:
                if m_name == "START":
                    target_r, target_c, target_m = 0, 0, "GOAL"
                else:
                    target_r, target_c, target_m = 2, 2, "GOAL"
        elif e.key == "Arrow Left":
            target_c = c - 1
            if target_c < 0:
                target_c = 2
                target_r = r - 1
            if target_r < 0:
                if m_name == "GOAL":
                    target_r, target_c, target_m = 2, 2, "START"
                else:
                    target_r, target_c, target_m = 0, 0, "START"
        elif e.key == "Arrow Down":
            target_r = r + 1
            if target_r > 2:
                if m_name == "START":
                    target_r, target_m = 0, "GOAL"
                else:
                    target_r = 2
        elif e.key == "Arrow Up":
            target_r = r - 1
            if target_r < 0:
                if m_name == "GOAL":
                    target_r, target_m = 2, "START"
                else:
                    target_r = 0

        if target_m == "START":
            start_inputs[target_r][target_c].focus()
        else:
            goal_inputs[target_r][target_c].focus()
        page.update()

    page.on_keyboard_event = on_keyboard

    def parse_input_matrix(storage_grid):
        matrix = []
        flat_list = []
        for r in range(3):
            row = []
            for c in range(3):
                val_str = storage_grid[r][c].value.strip()
                if not val_str:
                    raise ValueError("Không được để trống ô số.")

                # NẾU LÀ DẤU KHUYẾT: Giữ nguyên là chuỗi "?"
                if val_str == "?":
                    row.append("?")
                    flat_list.append("?")
                else:
                    # NẾU LÀ SỐ: Ép kiểu sang int bình thường
                    val = int(val_str)
                    if val < 0 or val > 8:
                        raise ValueError("Giá trị các ô phải từ 0 đến 8.")
                    row.append(val)
                    flat_list.append(val)
            matrix.append(row)

        # Kiểm tra tính hợp lệ: Tập hợp các số (không tính "?") không được trùng nhau
        numbers_only = [x for x in flat_list if x != "?"]
        if len(numbers_only) != len(set(numbers_only)):
            raise ValueError("Các con số từ 0 đến 8 trong ma trận không được trùng lặp nhau!")

        return matrix

    def draw_board(board):
        TILE_SIZE = 75  # Kích thước 1 ô
        TILE_SPACING = 6  # Khoảng cách giữa các ô

        # Bọc lót lấy biến giao diện an toàn lúc app vừa khởi động
        try:
            current_env = env_radio.value
        except Exception:
            current_env = "fully_observable"

        # 1. PHÂN TÍCH BÀN CỜ MỚI: Xem nó đang chứa những "chìa khóa" (số/dấu ?) nào
        new_keys = set()
        for r in range(3):
            for c in range(3):
                val = board[r][c]
                key = f"?_{r}_{c}" if val == "?" else val
                new_keys.add(key)

        # 2. KIỂM TRA SỰ THAY ĐỔI:
        # Nếu đổi chế độ (làm thay đổi số lượng dấu ? hoặc các con số) -> Đập đi xây lại
        if new_keys != set(board_tiles.keys()):
            board_tiles.clear()
            grid.controls.clear()

        # 3. TRƯỜNG HỢP VẼ MỚI: (Lúc mới mở app, hoặc lúc vừa đổi chế độ xong)
        if not board_tiles:
            for r in range(3):
                for c in range(3):
                    num = board[r][c]
                    top_pos = r * (TILE_SIZE + TILE_SPACING)
                    left_pos = c * (TILE_SIZE + TILE_SPACING)

                    is_hidden_question = (num == "?") and (current_env == "fully_observable")
                    is_zero = (num == 0) or is_hidden_question

                    cell_text = ""
                    if num == "?":
                        cell_text = "?" if current_env == "partially_observable" else ""
                    elif num != 0:
                        cell_text = str(num)

                    tile = ft.Container(
                        content=ft.Text(
                            cell_text,
                            size=24,
                            color="yellow" if num == "?" else ("white" if not is_zero else "transparent"),
                            weight=ft.FontWeight.BOLD
                        ),
                        width=TILE_SIZE, height=TILE_SIZE,
                        bgcolor="grey800" if num == "?" else ("grey" if is_zero else "blue"),
                        border_radius=10,
                        alignment=ft.alignment.center,
                        top=top_pos,
                        left=left_pos,
                        animate_position=300  # Giữ hiệu ứng trượt 300ms
                    )

                    key = f"?_{r}_{c}" if num == "?" else num
                    board_tiles[key] = tile
                    grid.controls.append(tile)

            # Cập nhật an toàn (tránh lỗi khi page chưa kịp add lúc khởi động)
            try:
                page.update()
            except Exception:
                pass
            return

        # 4. TRƯỜNG HỢP ĐI TỚI BƯỚC TIẾP THEO: Bật hiệu ứng trượt bay nhảy
        for r in range(3):
            for c in range(3):
                num = board[r][c]
                new_top = r * (TILE_SIZE + TILE_SPACING)
                new_left = c * (TILE_SIZE + TILE_SPACING)

                is_hidden_question = (num == "?") and (current_env == "fully_observable")
                is_zero = (num == 0) or is_hidden_question

                cell_text = ""
                if num == "?":
                    cell_text = "?" if current_env == "partially_observable" else ""
                elif num != 0:
                    cell_text = str(num)

                key = f"?_{r}_{c}" if num == "?" else num

                if key in board_tiles:
                    tile = board_tiles[key]
                    tile.top = new_top
                    tile.left = new_left
                    tile.bgcolor = "grey800" if num == "?" else ("grey" if is_zero else "blue")

                    text_control = tile.content
                    text_control.value = cell_text
                    text_control.color = "yellow" if num == "?" else ("white" if not is_zero else "transparent")

                try:
                    page.update()
                except Exception:
                    pass

    def update_board_from_inputs(e):
        """Tự động đọc các ô nhập liệu START và ép bảng chính vẽ lại ngay lập tức"""
        try:
            new_start = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

            # 1. Trường hợp biến start_inputs của bạn là danh sách phẳng 9 phần tử
            if len(start_inputs) == 9 and not isinstance(start_inputs[0], list):
                for i in range(9):
                    r, c = i // 3, i % 3
                    val = start_inputs[i].value.strip()
                    new_start[r][c] = "?" if val == "?" else (int(val) if val.isdigit() else 0)

            # 2. Trường hợp biến start_inputs của bạn là danh sách 2 chiều 3x3
            else:
                for r in range(3):
                    for c in range(3):
                        val = start_inputs[r][c].value.strip()
                        new_start[r][c] = "?" if val == "?" else (int(val) if val.isdigit() else 0)

            # Gọi hàm draw_board cập nhật giao diện chính ngay và luôn
            draw_board(new_start)
        except Exception:
            # Dùng try-except để tránh app bị crash khi người dùng đang xóa trống ô để gõ số mới
            pass

    def update_path_display():
        if not solution[0]:
            steps_path_view.value = "0 / 0"
            page.update()
            return

        # 1. Cập nhật Text số bước trên UI (Dùng đúng biến steps_path_view của bạn)
        steps_path_view.value = f"{current_step[0]} / {len(solution[0]) - 1}"

        # 2. 🔥 KIỂM TRA CHẠM ĐÍCH: Nếu đi đến bước cuối cùng, tự động nhả nút Pause về nút Play
        if current_step[0] >= len(solution[0]) - 1:
            running[0] = False  # Tắt trạng thái đang chạy tự động
            play_btn.icon = "play_arrow"
            play_btn.tooltip = "Chạy tự động"

        page.update()

    path_output = ft.TextField(
        label="Nhật ký cấu trúc dữ liệu (Logs)",
        multiline=True,
        min_lines=15,
        max_lines=15,
        read_only=True,
        value="Nhật ký chạy của hàm được chọn sẽ hiển thị trực quan tại đây...",
        text_style=ft.TextStyle(font_family="monospace", size=12),
    )

    belief_select_container = ft.Column(visible=False, spacing=5)

    visual_path_output = ft.TextField(
        label="Chi tiết ma trận đường đi & Hướng dịch chuyển ô trống",
        multiline=True,
        min_lines=15,
        max_lines=15,
        read_only=True,
        value="Sau khi giải xong, sơ đồ dịch chuyển sẽ hiển thị tại đây...",
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
            text += "=" * 25 + "\n"
        return text

    def solve_click(e):
        board_tiles.clear()
        custom_start = []
        custom_goal = []

        try:
            # 1. Đọc ma trận START từ các ô Textbox trên UI
            for r in range(3):
                row = []
                for c in range(3):
                    val = start_inputs[r][c].value.strip()
                    if val == "?":
                        row.append("?")  # Nếu là dấu ? thì giữ nguyên chuỗi
                    else:
                        row.append(int(val))  # Nếu là số thì ép kiểu int
                custom_start.append(row)

            # 2. Đọc ma trận GOAL từ UI tương tự
            for r in range(3):
                row = []
                for c in range(3):
                    val = goal_inputs[r][c].value.strip()
                    if val == "?":
                        row.append("?")
                    else:
                        row.append(int(val))
                custom_goal.append(row)

        except ValueError:
            info.value = "Vui lòng chỉ nhập số từ 0-8 hoặc dấu '?'"
            page.update()
            return

        info.value = "⏳ Đang tính toán dữ liệu, vui lòng đợi trong giây lát..."
        page.update()

        if mode_dropdown.value == "pop":
            path, bfs_log = bfs_check_on_pop(custom_start, custom_goal)
        elif mode_dropdown.value == "push":
            path, bfs_log = bfs_check_on_push_and_reached(custom_start, custom_goal)
        elif mode_dropdown.value == "dfs":
            path, bfs_log = dfs(custom_start, custom_goal)
        elif mode_dropdown.value == "iddfs":
            path, bfs_log = iddfs(custom_start, custom_goal)
        elif mode_dropdown.value == "ucs":
            path, bfs_log = ucs(custom_start, custom_goal)
        elif mode_dropdown.value == "greedy":
            path, bfs_log = greedy(custom_start, custom_goal)
        elif mode_dropdown.value == "a_star":
            path, bfs_log = a_star(custom_start, custom_goal)
        elif mode_dropdown.value == "ida_star":
            path, bfs_log = ida_star(custom_start, custom_goal)
        elif mode_dropdown.value == "hillcliming_simple":
            path, bfs_log = simple_hill_climbing(custom_start, custom_goal)
        elif mode_dropdown.value == "hillcliming_steepest":
            path, bfs_log = steepest_ascent_hill_climbing(custom_start, custom_goal)
        elif mode_dropdown.value == "hillcliming_random":
            path, bfs_log = random_hill_climbing(custom_start, custom_goal)
        elif mode_dropdown.value == "beam_search":
            try:
                # Ép kiểu độ rộng beam về số nguyên (int)
                b_width = int(beam_width_input.value)
                if b_width <= 0:
                    raise ValueError
                path, bfs_log = beam_search(custom_start, custom_goal, beam_width=b_width)
            except ValueError:
                path = None
                bfs_log = "❌ LỖI CẤU HÌNH: Độ rộng Beam (k) phải là một số nguyên dương (> 0)!"
        elif mode_dropdown.value == "hillcliming_restart":
            try:
                # Ép kiểu số lần khởi chạy lại về số nguyên (int)
                r_max = int(restart_max_input.value)
                if r_max <= 0:
                    raise ValueError
                path, bfs_log = random_restart_hill_climbing(custom_start, custom_goal, max_restart=r_max)
            except ValueError:
                path = None
                bfs_log = "❌ LỖI CẤU HÌNH: Số lần Restart tối đa phải là một số nguyên dương (> 0)!"
        elif mode_dropdown.value == "simulated_annealing":
            try:
                init_t = float(sa_temp_input.value)
                cool_r = float(sa_cooling_input.value)
                if init_t <= 0 or not (0 < cool_r < 1):
                    raise ValueError
                path, bfs_log = simulated_annealing(custom_start, custom_goal, initial_temp=init_t, cooling_rate=cool_r)
            except ValueError:
                path = None
                bfs_log = "❌ LỖI CẤU HÌNH: Vui lòng nhập Nhiệt độ SA > 0 và Tốc độ giảm nhiệt trong khoảng (0, 1)!"

        elif mode_dropdown.value == "solve_missing_start":
            path, bfs_log, paths_list = solve_missing_start(custom_start, custom_goal)
            page.session.set("all_belief_paths", paths_list)

        elif mode_dropdown.value == "solve_missing_goal":
            path, bfs_log, paths_list = solve_missing_goal(custom_start, custom_goal)
            page.session.set("all_belief_paths", paths_list)

        elif mode_dropdown.value == "solve_missing_both":
            path, bfs_log, paths_list = solve_missing_both(custom_start, custom_goal)
            page.session.set("all_belief_paths", paths_list)
        elif mode_dropdown.value == "and_or":
            path, bfs_log = and_or_graph_search(custom_start, custom_goal)
        elif mode_dropdown.value == "backtracking":
            path, bfs_log = backtracking_search(custom_start, custom_goal)
        elif mode_dropdown.value == "csp_domain":
            path, bfs_log = csp_domain_search(custom_start, custom_goal)

        # --- KHỐI 1: HIỂN THỊ KẾT QUẢ GIẢI (DÙNG CHUNG CHO TẤT CẢ THUẬT TOÁN) ---
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
            solution[0] = []
            update_path_display()
            visual_path_output.value = ""
        page.update()

        # --- KHỐI 2: CHỈ TỰ ĐỘNG SINH DROPDOWN KHI CHỌN ĐÚNG CÁC CHẾ ĐỘ KHUYẾT ---
        # Kiểm tra xem chế độ hiện tại có phải là 1 trong 3 chế độ khuyết hay không
        is_missing_mode = mode_dropdown.value in ["solve_missing_start", "solve_missing_goal", "solve_missing_both"]

        if is_missing_mode and ('paths_list' in locals()) and len(paths_list) >= 1:
            belief_select_container.controls.clear()

            # Tự động cá nhân hóa tiêu đề hướng dẫn theo từng loại khuyết
            title_text = "Chọn cấu hình xuất phát để xem mô phỏng:"
            if mode_dropdown.value == "solve_missing_goal":
                title_text = "Chọn cấu hình trạng thái đích tìm được:"
            elif mode_dropdown.value == "solve_missing_both":
                title_text = "Chọn cặp cấu hình (Xuất phát ➔ Đích) phù hợp:"

            belief_select_container.controls.append(
                ft.Text(title_text, weight=ft.FontWeight.BOLD, color="blue200")
            )

            dropdown_options = []
            for idx, p in enumerate(paths_list):
                # Tạo nhãn hiển thị ma trận trực quan cho từng chế độ khuyết
                if mode_dropdown.value == "solve_missing_start":
                    flatten_state = [num for row in p[0] for num in row]
                    label = f"Cấu hình Start {idx + 1}: {flatten_state}"
                elif mode_dropdown.value == "solve_missing_goal":
                    flatten_state = [num for row in p[-1] for num in row]
                    label = f"Cấu hình Goal {idx + 1}: {flatten_state}"
                else:  # solve_missing_both
                    flatten_start = [num for row in p[0] for num in row]
                    flatten_goal = [num for row in p[-1] for num in row]
                    label = f"Cặp {idx + 1}: {flatten_start} ➔ {flatten_goal}"

                dropdown_options.append(ft.dropdown.Option(key=str(idx), text=label))

            def on_belief_path_selected(ev):
                selected_idx = int(ev.control.value)
                all_paths = page.session.get("all_belief_paths")
                if all_paths:
                    solution[0] = all_paths[selected_idx]
                    current_step[0] = 0
                    draw_board(solution[0][0])
                    info.value = f"Đang xem mô phỏng cấu hình {selected_idx + 1}. Tổng số bước đi: {len(solution[0]) - 1} bước."
                    update_path_display()

                    v_text_sel = generate_visual_path_text(solution[0])
                    if len(v_text_sel) > 30000:
                        visual_path_output.value = v_text_sel[
                                                       :30000] + "\n... [Đường đi quá dài, đã thu gọn text sơ đồ] ..."
                    else:
                        visual_path_output.value = v_text_sel
                    page.update()

            belief_dropdown = ft.Dropdown(
                options=dropdown_options,
                value="0",  # Mặc định chọn cấu hình đầu tiên
                on_change=on_belief_path_selected,
                width=380
            )
            belief_select_container.controls.append(belief_dropdown)
            belief_select_container.visible = True
        else:
            # Nếu KHÔNG PHẢI chế độ khuyết (hoặc thuật toán thường không có paths_list) -> Ẩn ngay lập tức
            belief_select_container.visible = False

    def next_click(e):
        if solution[0] and current_step[0] < len(solution[0]) - 1:
            current_step[0] += 1
            draw_board(solution[0][current_step[0]])
            update_path_display()  # Logic bên trong hàm này sẽ tự chuyển nút thành PLAY khi chạm đích

    def prev_click(e):
        if not solution[0] or current_step[0] <= 0: return
        current_step[0] -= 1
        draw_board(solution[0][current_step[0]])
        update_path_display()
        page.update()

    def play_click(e):
        # Nếu chưa bấm "Giải" (chưa có đường đi), bấm Play sẽ không có tác dụng
        if not solution[0]:
            info.value = "⚠️ Vui lòng bấm nút 'Giải' để tìm đường đi trước khi bấm Play!"
            info.color = "orange"
            page.update()
            return

        # TRƯỜNG HỢP 1: App đang chạy tự động -> Bấm vào để TẠM DỪNG
        if running[0]:
            running[0] = False
            play_btn.icon = "play_arrow"  # Sửa thành chuỗi "play_arrow" viết thường
            play_btn.tooltip = "Chạy tự động"
            info.value = "⏸ Đã tạm dừng mô phỏng."
            info.color = "yellow"
            page.update()

        # TRƯỜNG HỢP 2: App đang dừng -> Bấm vào để CHẠY TỰ ĐỘNG
        else:
            # Nếu đang ở bước cuối cùng mà cố bấm Play -> Reset về bước đầu tiên để phát lại từ đầu
            if current_step[0] >= len(solution[0]) - 1:
                current_step[0] = 0
                draw_board(solution[0][0])

            running[0] = True
            play_btn.icon = "pause"  # Đổi ngay sang icon Tạm dừng
            play_btn.tooltip = "Tạm dừng"
            info.value = "▶ Đang tự động chạy mô phỏng đường đi..."
            info.color = "green"
            page.update()

            # Tạo một luồng (Thread) chạy ngầm để tăng bước đi theo thời gian, tránh treo UI
            def run_animation():
                import time
                # Vòng lặp chạy khi trạng thái running là True và chưa đi hết đường đi
                while running[0] and current_step[0] < len(solution[0]) - 1:
                    time.sleep(0.5)  # Tốc độ chuyển bước: 0.5 giây / 1 bước

                    # Kiểm tra an toàn: nếu trong lúc ngủ 0.5s mà người dùng bấm dừng thì thoát luôn
                    if not running[0]:
                        break

                    current_step[0] += 1
                    draw_board(solution[0][current_step[0]])  # Vẽ lại bàn cờ ở bước mới
                    update_path_display()  # Cập nhật chữ số bước "X / Y" và tự nhả nút về PLAY khi hết bước

            import threading
            threading.Thread(target=run_animation, daemon=True).start()

    solve_btn = ft.ElevatedButton("Giải 8 - Puzzle", on_click=solve_click, width=160, height=40,

                                  style=ft.ButtonStyle(color="white", bgcolor="green"))
    play_btn = ft.IconButton(
        icon="play_arrow",  # Truyền trực tiếp String, bất chấp mọi phiên bản Flet
        tooltip="Chạy tự động",
        icon_size=32,
        on_click=play_click
    )

    next_btn = ft.IconButton(
        icon="navigate_next",  # Sử dụng chuỗi chữ viết thường
        tooltip="Bước tiếp theo",
        on_click=next_click
    )

    prev_btn = ft.IconButton(
        icon="navigate_before",  # Sử dụng chuỗi chữ viết thường
        tooltip="Bước trước đó",
        on_click=prev_click
    )

    matrix_inputs_container = ft.Row([
        ft.Column([ft.Text("Mảng START (0=_)", size=12, weight=ft.FontWeight.BOLD, color="blue300"),
                   create_input_matrix(START, start_inputs, "START")],
                  horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Container(width=40),
        ft.Column([ft.Text("Mảng GOAL (0=_)", size=12, weight=ft.FontWeight.BOLD, color="orange300"),
                   create_input_matrix(GOAL, goal_inputs, "GOAL")], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # --- LAYOUT CỘT BÊN PHẢI (ĐÃ THÊM BỘ CHỌN MÔI TRƯỜNG CHỐNG CHE KHUẤT) ---
    right_column = ft.Column([
        ft.Text("Thông tin thực thi và Kết quả phân tích đường đi", size=18, weight=ft.FontWeight.BOLD, color="orange"),

        # Nhét bộ chọn môi trường vào đây (Nằm ở đầu cột bên phải)
        ft.Container(
            content=ft.Column([
                ft.Text("Chế độ quan sát môi trường:", weight=ft.FontWeight.BOLD, color="orange300", size=13),
                env_radio
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, "grey800"),
            border_radius=8,
            margin=ft.margin.only(bottom=5)
        ),

        # Khung chứa ma trận nhập liệu (Sẽ tự khuyết khi bấm Giải)
        ft.Container(content=matrix_inputs_container, padding=10, border=ft.border.all(1, "grey800"), border_radius=8,
                     margin=ft.margin.only(bottom=10), alignment=ft.alignment.center),
        belief_select_container,
        path_output,
        visual_path_output
    ], expand=True, scroll=ft.ScrollMode.AUTO)

    # --- LAYOUT CỘT BÊN TRÁI ---
    left_column = ft.Column([
        ft.Container(content=ft.Column([
            ft.Text("Cấu hình phiên bản thuật toán:", weight=ft.FontWeight.BOLD, color="blue300"),
            mode_dropdown,
            sa_config_container,
            beam_config_container,
            restart_config_container
        ]), padding=10, border=ft.border.all(1, "grey700"), border_radius=8),

        ft.Container(content=grid, margin=ft.margin.only(top=5, bottom=5)),
        ft.Container(content=steps_path_view, margin=ft.margin.only(top=5, bottom=5)),
        ft.Row([prev_btn, play_btn, next_btn], alignment=ft.MainAxisAlignment.CENTER),
        solve_btn,
        info
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=390,
        scroll=ft.ScrollMode.AUTO)

    page.add(ft.Container(padding=20,
                          content=ft.Row([left_column, ft.VerticalDivider(width=20, color="grey700"), right_column],
                                         vertical_alignment=ft.CrossAxisAlignment.START, expand=True), expand=True))

    # Vẽ bàn cờ mặc định ngay khi mở chương trình
    draw_board(START)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
