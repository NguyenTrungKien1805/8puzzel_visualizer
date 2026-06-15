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

# 16. Hướng phát triển

* Tích hợp Pattern Database Heuristic.
* Hỗ trợ 15-Puzzle.
* Xuất log ra file TXT/PDF.
* So sánh thời gian chạy giữa các thuật toán.
* Sinh biểu đồ thống kê hiệu năng.
* Hỗ trợ Dark Mode / Light Mode.
* Tích hợp thuật toán học tăng cường (Reinforcement Learning).
