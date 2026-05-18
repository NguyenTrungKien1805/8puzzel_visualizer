# 🧩 8-Puzzle BFS Visualizer (Dual Mode)

Ứng dụng trực quan hóa thuật toán **Tìm kiếm theo chiều rộng (Breadth-First Search - BFS)** để giải bài toán **8-Puzzle**. Chương trình được xây dựng giao diện trực quan (GUI) bằng thư viện **Flet (Flutter for Python)**, cho phép so sánh hai cơ chế kiểm tra trạng thái đích (Goal Test) phổ biến trong trí tuệ nhân tạo.

---

## 📸 Tổng Quan Giao Diện
Ứng dụng được chia làm 2 khu vực chức năng chính:
* **Cột bên trái:** Nơi lựa chọn phiên bản thuật toán, hiển thị bàn cờ 8-puzzle động dưới dạng lưới $3 \times 3$ và các nút điều hướng (`Prev` / `Next`) để xem từng bước dịch chuyển của ô trống.
* **Cột bên phải:** Khung nhật ký (Log) hiển thị chi tiết cấu trúc dữ liệu theo từng bước thực thi bao gồm: **NODE hiện tại**, trạng thái hàng đợi **FRONTIER** và tập các nút đã duyệt **REACHED**.

---

## ⚙️ Các Chế Độ Thuật Toán (Dual Mode)

Dự án này cài đặt và trực quan hóa sự khác biệt cốt lõi giữa hai cách tiếp cận BFS:

### 1. Hàm 1: Check khi POP + Add Reached khi POP
* **Cơ chế:** Trạng thái đích (`GOAL`) chỉ được kiểm tra khi lấy một Node ra khỏi hàng đợi (`queue.popleft()`). Tập `REACHED` cũng chỉ nạp thêm phần tử tại thời điểm Node đó được xử lý.
* **Đặc điểm:** Tuân thủ đúng lý thuyết BFS tổng quát cho đồ thị. Cần kiểm tra điều kiện `in_frontier` để tránh nạp trùng các phần tử đang chờ xử lý vào hàng đợi.

### 2. Hàm 2: Check khi SINH (PUSH) + Add Reached NGAY
* **Cơ chế:** Trạng thái đích được kiểm tra ngay khi các nút con vừa được sinh ra (trước khi đưa vào `queue.append()`). Đồng thời, nút con cũng được thêm ngay vào tập `REACHED`.
* **Đặc điểm:** Tối ưu hóa riêng cho thuật toán BFS với chi phí đồng nhất (Step cost = 1). Giúp thuật toán kết thúc sớm hơn (dừng ngay ở bước sinh ra kết quả thay vì đợi đến lượt pop), giảm thiểu kích thước bộ nhớ của `FRONTIER`.

---

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Yêu cầu hệ thống
* Máy tính đã cài đặt **Python 3.7** trở lên.

### 2. Cài đặt thư viện cần thiết
Mở Terminal/PowerShell tại thư mục dự án (kích hoạt môi trường ảo `.venv` nếu có) và chạy lệnh cài đặt thư viện `flet`:
```bash
pip install flet
