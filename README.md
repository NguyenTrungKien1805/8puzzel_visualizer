# 8 Puzzle Algorithm Visualizer

Ứng dụng trực quan hóa thuật toán tìm kiếm trên bài toán 8 Puzzle bằng Python + Flet.

Dự án hỗ trợ mô phỏng hoạt động của nhiều thuật toán AI/Search khác nhau như:

* BFS
* DFS
* IDDFS
* UCS
* Greedy Best First Search
* A*
* IDA*

Kèm:

* Giao diện trực quan
* Animation từng bước
* Log cấu trúc dữ liệu
* Frontier / Reached
* Phân tích đường đi
* Hướng di chuyển của ô trống

---

# Demo giao diện

## Board Puzzle + Điều khiển

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3ce55096-1ebb-4b01-af0c-97783b9f8270" />

---

# Công nghệ sử dụng

| Thành phần       | Công nghệ               |
| ---------------- | ----------------------- |
| Ngôn ngữ         | Python                  |
| GUI Framework    | Flet                    |
| Cấu trúc dữ liệu | deque, heapq            |
| AI Search        | BFS, DFS, UCS, A*, IDA* |
| Heuristic        | Manhattan Distance      |

---

# Thuật toán được hỗ trợ

| Thuật toán | Mô tả                              |
| ---------- | ---------------------------------- |
| BFS        | Tìm kiếm theo chiều rộng           |
| DFS        | Tìm kiếm theo chiều sâu            |
| IDDFS      | DFS tăng dần độ sâu                |
| UCS        | Uniform Cost Search                |
| Greedy     | Tham lam theo heuristic            |
| A*         | Tối ưu bằng g(n)+h(n)              |
| IDA*       | A* kết hợp DFS Iterative Deepening |

---

# Heuristic sử dụng

Dự án dùng:

## Manhattan Distance

[
h(n)=\sum |x_1-x_2|+|y_1-y_2|
]

h(n)=\sum |x_1-x_2|+|y_1-y_2|

---

# Công thức A*

[
f(n)=g(n)+h(n)
]

f(n)=g(n)+h(n)

Trong đó:

| Thành phần | Ý nghĩa                  |
| ---------- | ------------------------ |
| g(n)       | Chi phí thực tế từ Start |
| h(n)       | Heuristic Manhattan      |
| f(n)       | Tổng chi phí dự đoán     |

---

# IDA*

IDA* hoạt động bằng:

* DFS
* Threshold
* Heuristic Manhattan
* Iterative Deepening

Node sẽ bị cắt nếu:

[
f(n) > threshold
]

f(n)>threshold

---

# Cấu trúc dự án

```text
8puzzle_visualizer/
│
├── main.py
├── README.md
└── requirements.txt
```

---

# Cài đặt

## 1. Clone project

```bash
git clone https://github.com/your-username/8puzzle_visualizer.git
```

---

## 2. Di chuyển vào thư mục

```bash
cd 8puzzle_visualizer
```

---

## 3. Cài thư viện

## [Flet Official Website](https://flet.dev?utm_source=chatgpt.com)

```bash
pip install flet=0.22.1
```

---

# Chạy chương trình

```bash
python main.py
```

---

# Giao diện chính

## Khu vực bên trái

| Thành phần   | Chức năng        |
| ------------ | ---------------- |
| Dropdown     | Chọn thuật toán  |
| Board Puzzle | Hiển thị ma trận |
| Prev         | Quay lui         |
| Next         | Sang bước tiếp   |
| Play         | Chạy animation   |
| Solve        | Giải bài toán    |

---

## Khu vực bên phải

| Thành phần  | Chức năng          |
| ----------- | ------------------ |
| Search Logs | Nhật ký thuật toán |
| Visual Path | Đường đi chi tiết  |

---

# Chức năng nổi bật

## 1. Hiển thị Frontier

Ví dụ:

```text
FRONTIER:
[1 2 3 4 5 6 7 0 8]
[1 2 3 4 5 6 0 7 8]
```

---

## 2. Hiển thị Reached

```text
REACHED:
[1 2 3 4 0 6 7 5 8]
```

---

## 3. Animation tự động

* Play
* Pause
* Next
* Prev

---

## 4. Log cực chi tiết

Hiển thị:

* g(n)
* h(n)
* f(n)
* threshold
* frontier
* reached
* generated children

---

# Ví dụ log A*

```text
STEP 4 | (g: 2, h: 3, f: 5)

1 2 3
4 5 6
0 7 8

CÁC NODE CON:
+ Sinh ra ...
```

---

# Ví dụ log IDA*

```text
[CUT-OFF] f = 7 vượt threshold = 5
```

---

# Kiến thức AI/Search được minh họa

Dự án phù hợp để học:

* Artificial Intelligence
* Search Algorithms
* State Space Search
* Heuristic Search
* Informed Search
* Uninformed Search
* Graph Search
* Tree Search

---

# So sánh thuật toán

| Thuật toán | Tối ưu | Heuristic | Bộ nhớ     |
| ---------- | ------ | --------- | ---------- |
| BFS        | Có     | Không     | Cao        |
| DFS        | Không  | Không     | Thấp       |
| IDDFS      | Có     | Không     | Thấp       |
| UCS        | Có     | Không     | Cao        |
| Greedy     | Không  | Có        | Trung bình |
| A*         | Có     | Có        | Cao        |
| IDA*       | Có     | Có        | Thấp       |

---

# Ý tưởng hoạt động

## BFS

Dùng Queue:

```text
FIFO
```

---

## DFS

Dùng Stack:

```text
LIFO
```

---

## UCS

Ưu tiên:

* cost nhỏ nhất

---

## Greedy

Ưu tiên:

* heuristic nhỏ nhất

[
f(n)=h(n)
]

f(n)=h(n)

---

## A*

Ưu tiên:

* tổng chi phí nhỏ nhất

[
f(n)=g(n)+h(n)
]

f(n)=g(n)+h(n)

---

## IDA*

* DFS
* Threshold
* Iterative Deepening





