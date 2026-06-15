# 8-Puzzle Visualizer using Artificial Intelligence Search Algorithms

## 1. Giới thiệu

8-Puzzle là một bài toán kinh điển trong lĩnh vực Trí tuệ nhân tạo (Artificial Intelligence - AI). Bài toán bao gồm một bàn cờ kích thước 3×3 chứa 8 ô số từ 1 đến 8 và một ô trống (0). Mục tiêu là di chuyển các ô số bằng cách hoán đổi với ô trống để đưa trạng thái ban đầu về trạng thái đích.

Dự án này xây dựng một hệ thống trực quan hóa (Visualizer) giúp mô phỏng quá trình giải bài toán 8-Puzzle bằng nhiều thuật toán tìm kiếm khác nhau. Chương trình được phát triển bằng Python và Flet, cho phép người dùng theo dõi từng bước hoạt động của các thuật toán AI.

---

## 2. Mục tiêu

* Mô phỏng trực quan bài toán 8-Puzzle.
* So sánh hiệu quả của các thuật toán tìm kiếm AI.
* Hiển thị quá trình mở rộng trạng thái.
* Hiển thị Frontier, Reached, Cost, Heuristic và đường đi lời giải.
* Hỗ trợ nhập trạng thái đầu và trạng thái đích tùy chỉnh.
* Hỗ trợ ghi log chi tiết cho từng thuật toán.

---

## 3. Công nghệ sử dụng

### Ngôn ngữ lập trình

* Python 3.x

### Thư viện

* Flet (GUI)
* collections
* heapq
* copy
* random
* math
* asyncio

---

## 4. Mô tả bài toán

### Trạng thái

Mỗi trạng thái được biểu diễn bởi ma trận 3×3:

1 2 3
4 0 6
7 5 8

Trong đó:

* 0 đại diện cho ô trống.
* Các ô số có thể di chuyển lên, xuống, trái hoặc phải nếu hợp lệ.

### Trạng thái đích

1 2 3
4 5 6
7 8 0

### Toán tử

Ô trống có thể di chuyển:

* Up
* Down
* Left
* Right

### Hàm chi phí

Mỗi bước di chuyển có chi phí:

Cost = 1

---

## 5. Heuristic sử dụng

### Manhattan Distance

Tổng khoảng cách Manhattan của tất cả các ô đến vị trí đích.

h(n) = Σ(|x1 - x2| + |y1 - y2|)

Ưu điểm:

* Admissible
* Consistent
* Phù hợp với A*, Greedy và IDA*

---

## 6. Các thuật toán được cài đặt

### Hàm 1

Breadth First Search (Check Goal on Pop)

Đặc điểm:

* Kiểm tra đích khi lấy node khỏi Frontier.
* Thêm node vào Reached khi Pop.
* Luôn tìm được lời giải tối ưu theo số bước.

---

### Hàm 2

Breadth First Search (Check Goal on Generate)

Đặc điểm:

* Kiểm tra đích ngay khi sinh node.
* Có thể giảm số lượng node mở rộng.

---

### Hàm 3

Depth First Search (DFS)

Đặc điểm:

* Sử dụng Stack.
* Đi sâu trước.
* Không đảm bảo tối ưu.

---

### Hàm 4

Depth Limited Search (DLS)

Đặc điểm:

* DFS có giới hạn độ sâu.
* Tránh vòng lặp vô hạn.

---

### Hàm 5

Iterative Deepening DFS (IDDFS)

Đặc điểm:

* Kết hợp BFS và DFS.
* Tăng dần độ sâu.
* Tìm lời giải tối ưu theo độ sâu.

---

### Hàm 6

Uniform Cost Search (UCS)

Đặc điểm:

* Mở rộng node có chi phí nhỏ nhất.
* Sử dụng Priority Queue.
* Tối ưu khi chi phí không âm.

---

### Hàm 7

Greedy Best First Search

Đặc điểm:

* Chọn node có heuristic nhỏ nhất.
* Nhanh nhưng không đảm bảo tối ưu.

f(n) = h(n)

---

### Hàm 8

A* Search

Đặc điểm:

* Kết hợp Cost và Heuristic.
* Tối ưu và đầy đủ.

f(n) = g(n) + h(n)

---

### Hàm 9

Iterative Deepening A* (IDA*)

Đặc điểm:

* Kết hợp DFS và A*.
* Tiết kiệm bộ nhớ.

---

### Hàm 10

Hill Climbing

Đặc điểm:

* Luôn chọn trạng thái tốt nhất lân cận.
* Có thể mắc kẹt tại Local Maximum.

---

### Hàm 11

Steepest-Ascent Hill Climbing

Đặc điểm:

* Chọn trạng thái có heuristic tốt nhất trong toàn bộ lân cận.

---

### Hàm 12

Stochastic Hill Climbing

Đặc điểm:

* Chọn ngẫu nhiên trong các trạng thái tốt.

---

### Hàm 13

Beam Search

Đặc điểm:

* Chỉ giữ lại k trạng thái tốt nhất.
* Giảm sử dụng bộ nhớ.

---

### Hàm 14

Local Beam Search

Đặc điểm:

* Nhiều trạng thái được tìm kiếm song song.

---

### Hàm 15

Simulated Annealing

Đặc điểm:

* Cho phép chấp nhận trạng thái xấu trong giai đoạn đầu.
* Giúp thoát khỏi Local Optimum.

---

### Hàm 16

Belief State Search

Đặc điểm:

* Tìm kiếm trên tập trạng thái niềm tin.
* Thường dùng trong môi trường không hoàn toàn quan sát được.

---

### Hàm 17

AND-OR Graph Search

Đặc điểm:

* Cài đặt theo mã giả trong giáo trình AI.
* Gồm:

  * OR-SEARCH
  * AND-SEARCH
* Tránh chu trình bằng Path Checking.

---

### Hàm 18

Constraint Satisfaction Problem (CSP)

Đặc điểm:

* Backtracking Search.
* Constraint:

  * Không lặp trạng thái.
* Tìm lời giải bằng quay lui.

---

### Hàm 19

CSP with Domain Search

Đặc điểm:

* Mô hình hóa:

  * Variable = Current State
  * Domain = Successor States
  * Constraint = No Repeated State
* Domain được sắp xếp theo Manhattan Distance.

---

## 7. Chức năng giao diện

### Nhập trạng thái đầu

Người dùng có thể nhập trực tiếp:

Start State

### Nhập trạng thái đích

Người dùng có thể nhập trực tiếp:

Goal State

### Chọn thuật toán

Dropdown cho phép lựa chọn thuật toán cần chạy.

### Giải bài toán

Nút Solve:

* Chạy thuật toán.
* Tính toán đường đi.
* Sinh log chi tiết.

### Trực quan hóa

Hiển thị:

* Trạng thái hiện tại.
* Đường đi lời giải.
* Frontier.
* Reached.
* Chi phí.
* Heuristic.

---

## 8. Cấu trúc chương trình

Các thành phần chính:

* State Representation
* Successor Function
* Goal Test
* Heuristic Function
* Search Algorithms
* Visualization Module
* Logging System

---

## 9. Kết quả

Chương trình cho phép:

* So sánh hiệu suất các thuật toán.
* Quan sát quá trình tìm kiếm.
* Hiểu rõ cách hoạt động của các thuật toán AI cổ điển.
* Nghiên cứu sự khác biệt giữa Uninformed Search và Informed Search.

---

## 10. Kết luận

Dự án đã xây dựng thành công hệ thống trực quan hóa bài toán 8-Puzzle bằng nhiều thuật toán tìm kiếm trí tuệ nhân tạo khác nhau.

Thông qua việc quan sát Frontier, Reached, Heuristic và đường đi lời giải, người dùng có thể hiểu rõ hơn về nguyên lý hoạt động, ưu điểm và hạn chế của từng thuật toán.

Dự án là công cụ học tập và nghiên cứu hiệu quả cho các môn học liên quan đến Trí tuệ nhân tạo, Tìm kiếm Heuristic và Giải quyết bài toán bằng AI.

# 11. Hướng dẫn cài đặt

## Yêu cầu hệ thống

* Python 3.10 trở lên
* Windows 10/11
* Kết nối Internet để cài đặt thư viện

## Cài đặt thư viện

```bash
pip install flet==0.22.1
```

Hoặc:

```bash
pip install -r requirements.txt
```

## Chạy chương trình

```bash
python 8puzzelVisualizer.py
```

Sau khi chạy, giao diện chính của chương trình sẽ xuất hiện.

---

# 12. Hướng dẫn sử dụng

## Bước 1: Khởi động chương trình

Chạy file:

```bash
python 8puzzelVisualizer.py
```

Giao diện chính sẽ hiển thị.

### Hình 1. Giao diện chính

[Chèn ảnh giao diện chính tại đây]

---

## Bước 2: Nhập trạng thái đầu (Start State)

Người dùng nhập trạng thái ban đầu của bàn cờ 8-Puzzle.

Ví dụ:

| 1 | 2 | 3 |
| - | - | - |
| 4 | 0 | 6 |
| 7 | 5 | 8 |

Trong đó:

* Các số từ 0 đến 8 chỉ được xuất hiện đúng một lần.
* Số 0 đại diện cho ô trống.

### Hình 2. Nhập Start State

[Chèn ảnh nhập trạng thái đầu]

---

## Bước 3: Nhập trạng thái đích (Goal State)

Ví dụ:

| 1 | 2 | 3 |
| - | - | - |
| 4 | 5 | 6 |
| 7 | 8 | 0 |

### Hình 3. Nhập Goal State

[Chèn ảnh nhập trạng thái đích]

---

## Bước 4: Chọn thuật toán

Từ danh sách thuật toán, chọn thuật toán muốn thực hiện.

Ví dụ:

* BFS
* DFS
* UCS
* Greedy Search
* A*
* IDA*
* Hill Climbing
* Beam Search
* Simulated Annealing
* CSP Search
* AND-OR Graph Search

### Hình 4. Chọn thuật toán

[Chèn ảnh dropdown thuật toán]

---

## Bước 5: Nhấn Solve

Nhấn nút:

```text
SOLVE
```

Chương trình sẽ:

1. Thực hiện tìm kiếm.
2. Sinh đường đi lời giải.
3. Tạo log quá trình tìm kiếm.
4. Hiển thị số bước thực hiện.

### Hình 5. Nút Solve

[Chèn ảnh nút Solve]

---

## Bước 6: Quan sát kết quả

Sau khi giải xong, chương trình hiển thị:

* Đường đi từ Start đến Goal.
* Các bước dịch chuyển.
* Số lượng bước.
* Log thuật toán.

### Hình 6. Kết quả tìm kiếm

[Chèn ảnh kết quả]

---

# 13. Mô tả giao diện

## Khu vực nhập dữ liệu

Chức năng:

* Nhập Start State.
* Nhập Goal State.
* Kiểm tra dữ liệu hợp lệ.

### Hình 7. Khu vực nhập dữ liệu

[Chèn ảnh]

---

## Khu vực chọn thuật toán

Cho phép lựa chọn thuật toán AI muốn thực hiện.

### Hình 8. Khu vực chọn thuật toán

[Chèn ảnh]

---

## Khu vực hiển thị bàn cờ

Hiển thị trạng thái hiện tại của 8-Puzzle.

### Hình 9. Board Visualizer

[Chèn ảnh]

---

## Khu vực hiển thị lời giải

Hiển thị:

* Bước hiện tại.
* Tổng số bước.
* Trạng thái tương ứng.

### Hình 10. Solution Path

[Chèn ảnh]

---

## Khu vực Log

Hiển thị chi tiết quá trình tìm kiếm:

* Current Node
* Frontier
* Reached
* Cost
* Heuristic
* Goal Test

### Hình 11. Search Log

[Chèn ảnh]

---

# 14. Ví dụ thực nghiệm

## Input

Start State:

1 2 3
4 0 6
7 5 8

Goal State:

1 2 3
4 5 6
7 8 0

Thuật toán:

A* Search

---

## Output

Path:

Bước 0

1 2 3
4 0 6
7 5 8

↓

Bước 1

1 2 3
4 5 6
7 0 8

↓

Bước 2

1 2 3
4 5 6
7 8 0

---

Số bước:

2

### Hình 12. Kết quả A*

[Chèn ảnh]

---

# 15. Đánh giá kết quả

| Thuật toán          | Tối ưu | Đầy đủ | Bộ nhớ     |
| ------------------- | ------ | ------ | ---------- |
| BFS                 | Có     | Có     | Cao        |
| DFS                 | Không  | Không  | Thấp       |
| UCS                 | Có     | Có     | Cao        |
| Greedy              | Không  | Không  | Thấp       |
| A*                  | Có     | Có     | Trung bình |
| IDA*                | Có     | Có     | Thấp       |
| Hill Climbing       | Không  | Không  | Rất thấp   |
| Beam Search         | Không  | Không  | Thấp       |
| Simulated Annealing | Không  | Không  | Rất thấp   |

---
<<<<<<< HEAD
=======

# 16. Hướng phát triển

* Tích hợp Pattern Database Heuristic.
* Hỗ trợ 15-Puzzle.
* Xuất log ra file TXT/PDF.
* So sánh thời gian chạy giữa các thuật toán.
* Sinh biểu đồ thống kê hiệu năng.
* Hỗ trợ Dark Mode / Light Mode.
* Tích hợp thuật toán học tăng cường (Reinforcement Learning).
>>>>>>> 616cd22a54c38a25ff1adf8a508d9ee9c12fca77
